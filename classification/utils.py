from pathlib import Path


def assess_file_compatability(file_path, filetype_compatibility):
    file_type = Path(file_path).suffix.lstrip(".")
    if file_type in [ft.name for ft in filetype_compatibility]:
        return True
    return False
