import os

def infer_language(file_path, content=""):
    ext = os.path.splitext(file_path)[1].lower()
    mapping = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".cs": "C#",
        ".go": "Go",
        ".rb": "Ruby",
        ".php": "PHP",
        ".rs": "Rust",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".scala": "Scala",
        ".html": "HTML",
        ".css": "CSS",
        ".json": "JSON",
        ".md": "Markdown",
        ".sh": "Shell",
        ".bat": "Batch",
        ".yml": "YAML",
        ".yaml": "YAML",
    }
    return mapping.get(ext, "Unknown")
