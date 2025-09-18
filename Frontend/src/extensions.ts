import * as vscode from 'vscode';
import WebSocket from 'ws';

export function activate(context: vscode.ExtensionContext) {
    context.subscriptions.push(
        vscode.commands.registerCommand('code-assistant.openChat', () => {
            const panel = vscode.window.createWebviewPanel(
                'codeAssistantChat',
                'Code Assistant Chat',
                vscode.ViewColumn.One,
                { enableScripts: true }
            );

            panel.webview.html = getWebviewContent();

            let taggedFilePath: string | undefined;
            let fullContent: string = '';
            let chatHistory: { role: string, content: string }[] = [];

            // Chat history state is managed in the webview context using getState/setState

            // Listen for messages from the webview
            panel.webview.onDidReceiveMessage(async message => {
                if (message.command === 'init') {
                    const uri = await vscode.window.showOpenDialog({
                        canSelectMany: false,
                        openLabel: 'Tag this file'
                    });
                    if (uri && uri[0]) {
                        taggedFilePath = uri[0].fsPath;
                        const document = await vscode.workspace.openTextDocument(taggedFilePath);
                        fullContent = document.getText();
                        panel.webview.postMessage({ command: 'fileTagged', file: taggedFilePath });
                    }
                }
                if (message.command === 'edit') {
                    if (!taggedFilePath) {
                        panel.webview.postMessage({ command: 'error', text: 'No file tagged! Please tag a file first.' });
                        return;
                    }
                    const userInstruction = message.text;
                    chatHistory.push({ role: 'user', content: userInstruction });

                    const ws = new WebSocket('ws://127.0.0.1:8000/chat/ws');
                    ws.on('open', () => {
                        ws.send(JSON.stringify({
                            mode: "edit",
                            file_path: taggedFilePath,
                            user_instruction: userInstruction,
                            full_content: fullContent,
                            code_before_cursor: "",
                            code_after_cursor: "",
                            codebase_context: "",
                            chat_history: chatHistory
                        }));
                    });
                    ws.on('message', async (data) => {
                        const response = JSON.parse(data.toString());
                        const code = response.result;
                        const explanation = response.explanation || 'Code updated in the tagged file.';

                        // Overwrite the tagged file
                        const document = await vscode.workspace.openTextDocument(taggedFilePath!);
                        const edit = new vscode.WorkspaceEdit();
                        const fullRange = new vscode.Range(
                            document.positionAt(0),
                            document.positionAt(document.getText().length)
                        );
                        edit.replace(document.uri, fullRange, code);
                        await vscode.workspace.applyEdit(edit);
                        await document.save();

                        chatHistory.push({ role: 'assistant', content: explanation });
                        panel.webview.postMessage({ command: 'answer', text: explanation });
                        // setState is only available in the webview context (HTML/JS), not here
                        ws.close();
                    });
                    ws.on('error', (err) => {
                        panel.webview.postMessage({ command: 'error', text: 'WebSocket error: ' + err.message });
                    });
                }
                if (message.command === 'ask') {
                    const userInstruction = message.text;
                    chatHistory.push({ role: 'user', content: userInstruction });

                    const ws = new WebSocket('ws://127.0.0.1:8000/chat/ws');
                    ws.on('open', () => {
                        ws.send(JSON.stringify({
                            mode: "ask",
                            file_path: taggedFilePath || "",
                            user_instruction: userInstruction,
                            full_content: fullContent,
                            code_before_cursor: "",
                            code_after_cursor: "",
                            codebase_context: "",
                            chat_history: chatHistory
                        }));
                    });
                    ws.on('message', (data) => {
                        const response = JSON.parse(data.toString());
                        const answer = response.result;
                        chatHistory.push({ role: 'assistant', content: answer });
                        panel.webview.postMessage({ command: 'answer', text: answer });
                        // setState is only available in the webview context (HTML/JS), not here
                        ws.close();
                    });
                    ws.on('error', (err) => {
                        panel.webview.postMessage({ command: 'error', text: 'WebSocket error: ' + err.message });
                    });
                }
            });
        })
    );
}

function getWebviewContent() {
    return `
        <!DOCTYPE html>
        <html lang="en">
        <body>
            <button onclick="init()">Tag File</button>
            <div id="file"></div>
            <div id="chat" style="height:300px;overflow:auto;border:1px solid #ccc;margin-bottom:8px;"></div>
            <select id="mode">
                <option value="ask">Ask</option>
                <option value="edit">Edit</option>
            </select>
            <input id="input" type="text" placeholder="Type your message..." style="width:70%;" />
            <button onclick="send()">Send</button>
            <script>
                const vscode = acquireVsCodeApi();
                let chatHistory = vscode.getState()?.chatHistory || [];

                function init() {
                    vscode.postMessage({ command: 'init' });
                }
                function send() {
                    const input = document.getElementById('input');
                    const mode = document.getElementById('mode').value;
                    if (input.value.trim() === '') return;
                    addMessage('You', input.value);
                    vscode.postMessage({ command: mode, text: input.value });
                    input.value = '';
                }
                function addMessage(sender, text) {
                    const chat = document.getElementById('chat');
                    chat.innerHTML += '<div><b>' + sender + ':</b> ' + text + '</div>';
                    chat.scrollTop = chat.scrollHeight;
                    chatHistory.push({ sender, text });
                    vscode.setState({ chatHistory });
                }
                window.onload = () => {
                    chatHistory.forEach(msg => addMessage(msg.sender, msg.text));
                };
                window.addEventListener('message', event => {
                    const message = event.data;
                    if (message.command === 'answer') {
                        addMessage('Assistant', message.text);
                    }
                    if (message.command === 'error') {
                        addMessage('Error', message.text);
                    }
                    if (message.command === 'fileTagged') {
                        document.getElementById('file').innerText = 'Tagged file: ' + message.file;
                    }
                });
            </script>
        </body>
        </html>
    `;
}

export function deactivate() {}