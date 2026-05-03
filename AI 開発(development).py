"""
This file previously contained VS Code settings JSON that were pasted
into a Python file by mistake.

Notes:
- `python.analysis.extraPaths` expects filesystem paths (folders) to
  add to Python's import search path, NOT shell commands like
  `pip install ...`.
- To install packages, run `pip` or `conda` in a terminal (see
  `requirements.txt` in this folder).

Example `.vscode/settings.json` entry:

{
    "python.analysis.extraPaths": [
        "./src",
        "./lib"
    ]
}

This small helper below checks whether the common packages are
installed and prints instructions to install any that are missing.
"""

REQUIRED_PACKAGES = {
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "scikit-learn": "sklearn",
    "tensorflow": "tensorflow",
}


def check_packages():
    """Check for required packages and print missing ones."""
    import importlib

    missing = []
    for pkg, import_name in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(import_name)
        except Exception:
            missing.append(pkg)

    if missing:
        print("Missing packages:", ", ".join(missing))
        print("Install them with: pip install " + " ".join(missing))
    else:
        print("All required packages are installed.")


if __name__ == "__main__":
    check_packages()
