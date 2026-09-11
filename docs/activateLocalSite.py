import subprocess
import os

def launch_service(name, cmd, cwd):
    print(f"Starting {name}...")
    subprocess.Popen(
        cmd,
        cwd=cwd,
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

def run_sync(name, cmd, cwd):
    print(f"Running {name}...")
    result = subprocess.run(cmd, cwd=cwd, shell=True)
    if result.returncode != 0:
        print(f"Failed to run {name}")

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    frontend_dir = os.path.join(root_dir, 'frontend')
    backend_dir = os.path.join(root_dir, 'backend')

    print("Activating Blacksmith Knight Local Environment...")

    # Frontend setup
    if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
        print("Node modules missing. Installing frontend dependencies...")
        run_sync("npm install", "npm install", frontend_dir)
    
    if not os.path.exists(os.path.join(frontend_dir, ".next")):
        print("Next.js build missing. Building frontend...")
        run_sync("npm run build", "npm run build", frontend_dir)

    # Backend setup
    venv_python = os.path.join(backend_dir, ".venv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        print("Backend virtual environment missing. Creating...")
        run_sync("python -m venv .venv", "python -m venv .venv", backend_dir)
        print("Installing backend dependencies...")
        run_sync("pip install", f"{venv_python} -m pip install -r requirements.txt", backend_dir)

    # 1. Firebase Emulator
    launch_service("Firebase", "cmd /k firebase emulators:start --only firestore", root_dir)

    # 2. Backend
    launch_service("Backend", "cmd /k .\\.venv\\Scripts\\uvicorn app.main:app --reload --port 8000", backend_dir)

    # 3. Frontend
    launch_service("Frontend", "cmd /k npm run dev", frontend_dir)

    print("All services launched in new console windows.")

if __name__ == '__main__':
    main()
