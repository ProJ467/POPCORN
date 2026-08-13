import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "projects.json"


def load_projects():
    """Return all stored project records."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data.get("projects", [])
            return data
    except (json.JSONDecodeError, OSError):
        return []


def save_projects(projects):
    """Persist project records."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump({"projects": projects}, file, indent=2)
        file.write("\n")


def create_project(title, owner, description=""):
    """Create a basic project record."""
    projects = load_projects()

    if not title or not owner:
        raise ValueError("Title and owner are required.")

    project = {
        "title": title,
        "owner": owner,
        "description": description,
    }
    projects.append(project)
    save_projects(projects)
    return project
