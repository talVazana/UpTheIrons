"""
Blacksmith Knight - Development Environment Setup
==================================================

Run this script from the ROOT of the already-cloned repository.

Example:
    python setup_dev_environment.py

The script:
    - Checks required development tools
    - Installs missing tools using winget where possible
    - Checks Node/npm
    - Checks Python
    - Checks Git
    - Checks Firebase CLI
    - Creates/reuses Python virtual environment
    - Installs Python dependencies if requirements.txt exists
    - Installs Node dependencies if package.json exists
    - Checks Firebase configuration
    - Checks Firebase emulator availability
    - Runs basic validation
    - Does NOT start servers automatically
    - Does NOT modify source code
    - Does NOT overwrite configuration files
    - Can safely be run multiple times
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

VENV_DIR = PROJECT_ROOT / ".venv"

PYTHON_REQUIREMENTS = PROJECT_ROOT / "requirements.txt"
PYTHON_REQUIREMENTS_ALT = PROJECT_ROOT / "backend" / "requirements.txt"

PACKAGE_JSON = PROJECT_ROOT / "package.json"
FRONTEND_PACKAGE_JSON = PROJECT_ROOT / "frontend" / "package.json"

FIREBASE_JSON = PROJECT_ROOT / "firebase.json"

# Commands that can be checked directly.
TOOLS = {
    "git": ["git", "--version"],
    "node": ["node", "--version"],
    "npm": ["npm", "--version"],
    "python": [sys.executable, "--version"],
    "firebase": ["firebase", "--version"],
}


# ============================================================
# Output helpers
# ============================================================

def banner(text: str) -> None:
    print()
    print("=" * 70)
    print(text)
    print("=" * 70)


def info(text: str) -> None:
    print(f"[INFO] {text}")


def success(text: str) -> None:
    print(f"[ OK ] {text}")


def warning(text: str) -> None:
    print(f"[WARN] {text}")


def error(text: str) -> None:
    print(f"[ERROR] {text}")


def run_command(
    command: list[str],
    *,
    cwd: Path | None = None,
    check: bool = False,
    capture: bool = True,
) -> subprocess.CompletedProcess:
    """
    Run a command safely.
    """

    try:
        return subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            check=check,
            capture_output=capture,
            text=True,
            shell=False,
        )
    except FileNotFoundError:
        return subprocess.CompletedProcess(
            command,
            returncode=127,
            stdout="",
            stderr="Command not found",
        )


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


# ============================================================
# Windows / Administrator helpers
# ============================================================

def is_windows() -> bool:
    return platform.system().lower() == "windows"


def winget_available() -> bool:
    return command_exists("winget")


def run_winget_install(
    package_id: str,
    display_name: str,
) -> bool:
    """
    Install a package through winget.

    Uses --silent where possible, but allows winget to ask for
    confirmation if Windows/package policy requires it.
    """

    if not winget_available():
        warning(
            f"winget is not available. Cannot automatically install "
            f"{display_name}."
        )
        return False

    info(f"Installing {display_name} using winget...")

    command = [
        "winget",
        "install",
        "--id",
        package_id,
        "--exact",
        "--accept-source-agreements",
        "--accept-package-agreements",
    ]

    result = run_command(command, capture=False)

    if result.returncode == 0:
        success(f"{display_name} installed.")
        return True

    warning(
        f"winget could not install {display_name} "
        f"(exit code {result.returncode})."
    )

    return False


# ============================================================
# Tool detection
# ============================================================

def check_command(
    name: str,
    command: list[str],
) -> bool:

    result = run_command(command)

    if result.returncode == 0:
        version = (result.stdout or result.stderr).strip()
        success(f"{name}: {version}")
        return True

    warning(f"{name}: NOT AVAILABLE")
    return False


def refresh_path() -> None:
    """
    Windows installers sometimes modify PATH while the current
    Python process still has the old PATH.

    Refresh PATH from the Windows environment.
    """

    if not is_windows():
        return

    try:
        import ctypes

        # Ask Windows for the current environment.
        result = subprocess.run(
            ["cmd", "/c", "echo", "%PATH%"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            path = result.stdout.strip()

            if path:
                os.environ["PATH"] = path

    except Exception:
        pass


# ============================================================
# Install required tools
# ============================================================

def ensure_git() -> bool:

    if check_command("Git", ["git", "--version"]):
        return True

    if not is_windows():
        error("Git is missing and automatic installation is only configured for Windows.")
        return False

    return run_winget_install(
        "Git.Git",
        "Git",
    )


def ensure_node() -> bool:

    if check_command("Node.js", ["node", "--version"]):
        return True

    if not is_windows():
        error("Node.js is missing and automatic installation is only configured for Windows.")
        return False

    installed = run_winget_install(
        "OpenJS.NodeJS.LTS",
        "Node.js LTS",
    )

    if installed:
        refresh_path()

    return installed


def ensure_python() -> bool:

    # We are already running Python.
    version = sys.version.split()[0]

    success(f"Python: {version}")

    major = sys.version_info.major
    minor = sys.version_info.minor

    if major != 3 or minor < 11:
        warning(
            "Python 3.11+ is recommended for this project. "
            f"Current version: {version}"
        )

    return True


def ensure_firebase() -> bool:

    if check_command("Firebase CLI", ["firebase", "--version"]):
        return True

    if not is_windows():
        error(
            "Firebase CLI is missing. "
            "Install it with npm."
        )
        return False

    # Firebase CLI is distributed through npm.
    if not command_exists("npm"):
        error("npm is required to install Firebase CLI.")
        return False

    info("Firebase CLI is missing.")
    info("Installing Firebase CLI globally with npm...")

    result = run_command(
        ["npm", "install", "-g", "firebase-tools"],
        capture=False,
    )

    if result.returncode != 0:
        warning("Firebase CLI installation failed.")
        return False

    refresh_path()

    return check_command(
        "Firebase CLI",
        ["firebase", "--version"],
    )


# ============================================================
# Project discovery
# ============================================================

def locate_requirements() -> Path | None:

    candidates = [
        PYTHON_REQUIREMENTS,
        PYTHON_REQUIREMENTS_ALT,
    ]

    for path in candidates:
        if path.exists():
            return path

    return None


def locate_package_json() -> Path | None:

    candidates = [
        PACKAGE_JSON,
        FRONTEND_PACKAGE_JSON,
    ]

    for path in candidates:
        if path.exists():
            return path

    return None


def inspect_project() -> None:

    banner("PROJECT DISCOVERY")

    info(f"Project root: {PROJECT_ROOT}")

    if not (PROJECT_ROOT / ".git").exists():
        warning(
            "This directory does not appear to contain a .git folder."
        )
        warning(
            "Make sure you are running this script from the cloned repository."
        )
    else:
        success("Git repository detected.")

    if PACKAGE_JSON.exists():
        success("Root package.json detected.")

    if FRONTEND_PACKAGE_JSON.exists():
        success("Frontend package.json detected.")

    if PYTHON_REQUIREMENTS.exists():
        success("Root requirements.txt detected.")

    if PYTHON_REQUIREMENTS_ALT.exists():
        success("Backend requirements.txt detected.")

    if FIREBASE_JSON.exists():
        success("firebase.json detected.")
    else:
        warning(
            "firebase.json not found. Firebase emulator setup may not "
            "yet be configured in this repository."
        )


# ============================================================
# Python virtual environment
# ============================================================

def get_venv_python() -> Path:

    if is_windows():
        return VENV_DIR / "Scripts" / "python.exe"

    return VENV_DIR / "bin" / "python"


def create_python_venv() -> bool:

    banner("PYTHON VIRTUAL ENVIRONMENT")

    venv_python = get_venv_python()

    if venv_python.exists():
        success(f"Python virtual environment already exists: {VENV_DIR}")
        return True

    info(f"Creating virtual environment: {VENV_DIR}")

    result = run_command(
        [
            sys.executable,
            "-m",
            "venv",
            str(VENV_DIR),
        ],
        capture=False,
    )

    if result.returncode != 0:
        error("Failed to create Python virtual environment.")
        return False

    success("Python virtual environment created.")

    return True


def install_python_dependencies() -> bool:

    banner("PYTHON DEPENDENCIES")

    requirements = locate_requirements()

    if requirements is None:
        warning(
            "No requirements.txt found. "
            "Skipping Python dependency installation."
        )
        return True

    venv_python = get_venv_python()

    if not venv_python.exists():
        error("Virtual environment Python was not found.")
        return False

    info(f"Requirements file: {requirements}")

    # Upgrade pip first.
    info("Checking pip...")

    pip_result = run_command(
        [
            str(venv_python),
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
        ],
        cwd=PROJECT_ROOT,
        capture=False,
    )

    if pip_result.returncode != 0:
        warning("pip upgrade failed. Continuing with dependency installation.")

    info("Installing Python dependencies...")

    result = run_command(
        [
            str(venv_python),
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements),
        ],
        cwd=PROJECT_ROOT,
        capture=False,
    )

    if result.returncode != 0:
        error("Python dependency installation failed.")
        return False

    success("Python dependencies installed.")

    return True


# ============================================================
# Node dependencies
# ============================================================

def install_node_dependencies() -> bool:

    banner("NODE DEPENDENCIES")

    package_json = locate_package_json()

    if package_json is None:
        warning(
            "No package.json found. "
            "Skipping npm dependency installation."
        )
        return True

    project_dir = package_json.parent

    info(f"Node project: {project_dir}")

    node_modules = project_dir / "node_modules"

    if node_modules.exists():
        info("node_modules already exists.")
        info("Running npm install to synchronize dependencies.")

    else:
        info("node_modules not found.")
        info("Installing npm dependencies.")

    # Prefer npm ci when package-lock exists because it gives
    # deterministic installs.
    package_lock = project_dir / "package-lock.json"

    if package_lock.exists():
        command = ["npm", "ci"]
        info("package-lock.json detected → using npm ci.")
    else:
        command = ["npm", "install"]
        info("No package-lock.json detected → using npm install.")

    result = run_command(
        command,
        cwd=project_dir,
        capture=False,
    )

    if result.returncode != 0:
        error("Node dependency installation failed.")
        return False

    success("Node dependencies installed.")

    return True


# ============================================================
# Firebase checks
# ============================================================

def check_firebase_configuration() -> bool:

    banner("FIREBASE CONFIGURATION")

    if not FIREBASE_JSON.exists():
        warning(
            "firebase.json does not exist."
        )
        warning(
            "This is not necessarily an error if Firebase configuration "
            "has not yet been committed."
        )
        return True

    success("firebase.json exists.")

    result = run_command(
        ["firebase", "projects:list"],
        cwd=PROJECT_ROOT,
    )

    # projects:list can fail for authentication/network reasons.
    # That does NOT necessarily mean the emulator is broken.
    if result.returncode == 0:
        success("Firebase CLI can access Firebase configuration.")
    else:
        warning(
            "Firebase project listing was not available."
        )
        warning(
            "This can be normal if you are not logged into Firebase."
        )

    return True


def check_emulator_components() -> bool:

    banner("FIREBASE EMULATOR")

    if not command_exists("firebase"):
        warning("Firebase CLI unavailable.")
        return False

    result = run_command(
        ["firebase", "emulators:exec", "--help"],
        cwd=PROJECT_ROOT,
    )

    if result.returncode == 0:
        success("Firebase Emulator Suite command is available.")
        return True

    warning(
        "Firebase Emulator Suite command could not be verified."
    )

    return False


# ============================================================
# Optional project health checks
# ============================================================

def run_project_checks() -> None:

    banner("PROJECT HEALTH CHECK")

    # Backend structure
    backend_dir = PROJECT_ROOT / "backend"

    if backend_dir.exists():
        success("backend/ directory found.")
    else:
        warning("backend/ directory not found.")

    # Frontend structure
    frontend_dir = PROJECT_ROOT / "frontend"

    if frontend_dir.exists():
        success("frontend/ directory found.")
    else:
        warning("frontend/ directory not found.")

    # Next.js
    package_json = locate_package_json()

    if package_json:
        info("Node project detected.")

    # Python
    if locate_requirements():
        info("Python dependency definition detected.")

    # Tests
    test_dirs = [
        PROJECT_ROOT / "tests",
        PROJECT_ROOT / "backend" / "tests",
        PROJECT_ROOT / "frontend" / "tests",
    ]

    found_tests = False

    for test_dir in test_dirs:
        if test_dir.exists():
            success(f"Test directory found: {test_dir.relative_to(PROJECT_ROOT)}")
            found_tests = True

    if not found_tests:
        info("No standard test directory detected yet.")


# ============================================================
# Final report
# ============================================================

def final_report(
    git_ok: bool,
    node_ok: bool,
    python_ok: bool,
    firebase_ok: bool,
    python_deps_ok: bool,
    node_deps_ok: bool,
) -> int:

    banner("SETUP RESULT")

    checks = {
        "Git": git_ok,
        "Node.js": node_ok,
        "Python": python_ok,
        "Firebase CLI": firebase_ok,
        "Python dependencies": python_deps_ok,
        "Node dependencies": node_deps_ok,
    }

    failed = []

    for name, result in checks.items():

        if result:
            print(f"  [ OK ] {name}")
        else:
            print(f"  [FAIL] {name}")
            failed.append(name)

    print()

    if failed:
        warning("Development environment is NOT fully ready.")

        print()
        print("Items requiring attention:")

        for item in failed:
            print(f"  - {item}")

        print()
        warning(
            "The script is safe to run again after fixing the problem."
        )

        return 1

    success("Development environment is ready.")

    print()
    print("Next steps:")
    print()
    print("  1. Activate the Python virtual environment:")
    print()
    print("       .venv\\Scripts\\activate")
    print()
    print("  2. Start the Firebase emulator when required.")
    print()
    print("  3. Start the FastAPI backend.")
    print()
    print("  4. Start the Next.js frontend.")
    print()
    print("  5. Run the project's tests.")
    print()

    return 0


# ============================================================
# Main
# ============================================================

def main() -> int:

    banner("BLACKSMITH KNIGHT")
    print("Development Environment Setup")
    print()
    print(f"Repository: {PROJECT_ROOT}")
    print()

    if not is_windows():
        warning(
            "This setup script is primarily designed for Windows."
        )

    inspect_project()

    banner("REQUIRED DEVELOPMENT TOOLS")

    git_ok = ensure_git()

    refresh_path()

    node_ok = ensure_node()

    refresh_path()

    python_ok = ensure_python()

    refresh_path()

    firebase_ok = ensure_firebase()

    refresh_path()

    # Re-check commands after possible installations.
    git_ok = check_command(
        "Git",
        ["git", "--version"],
    ) or git_ok

    node_ok = check_command(
        "Node.js",
        ["node", "--version"],
    ) or node_ok

    npm_ok = check_command(
        "npm",
        ["npm", "--version"],
    )

    firebase_ok = check_command(
        "Firebase CLI",
        ["firebase", "--version"],
    ) or firebase_ok

    if not npm_ok:
        error("npm is required for the Next.js/Firebase environment.")

    # Python environment.
    venv_ok = create_python_venv()

    if venv_ok:
        python_deps_ok = install_python_dependencies()
    else:
        python_deps_ok = False

    # Node environment.
    if node_ok and npm_ok:
        node_deps_ok = install_node_dependencies()
    else:
        node_deps_ok = False

    # Firebase.
    if firebase_ok:
        check_firebase_configuration()
        check_emulator_components()

    run_project_checks()

    return final_report(
        git_ok=git_ok,
        node_ok=node_ok and npm_ok,
        python_ok=python_ok and venv_ok,
        firebase_ok=firebase_ok,
        python_deps_ok=python_deps_ok,
        node_deps_ok=node_deps_ok,
    )


if __name__ == "__main__":
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        print()
        warning("Setup cancelled by user.")
        sys.exit(2)

    except Exception as exc:
        print()
        error("Unexpected error:")
        print(f"       {exc}")
        print()
        warning(
            "No project source files were intentionally modified."
        )
        sys.exit(3)