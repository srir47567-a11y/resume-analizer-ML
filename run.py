import os
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# If not running inside the project's .venv, re-execute with .venv Python
venv_python = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
if venv_python.exists() and Path(sys.executable).resolve() != venv_python.resolve():
    os.environ["VIRTUAL_ENV"] = str(PROJECT_ROOT / ".venv")
    try:
        result = subprocess.run([str(venv_python)] + sys.argv)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        # User pressed Ctrl+C to stop the server; exit cleanly
        sys.exit(0)

import uvicorn


def open_browser(url: str, delay: float = 1.2):
    """Open the web browser after a brief delay for the server to start."""
    def _target():
        time.sleep(delay)
        try:
            webbrowser.open(url)
        except Exception:
            pass

    threading.Thread(target=_target, daemon=True).start()


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    app_url = f"http://{host}:{port}"
    docs_url = f"http://{host}:{port}/docs"

    print("=" * 65)
    print("🚀 Starting SkillMatch ML Application...")
    print("=" * 65)
    print(f"  👉 Web Dashboard:     {app_url}")
    print(f"  👉 API Documentation: {docs_url}")
    print("=" * 65)
    print("Press Ctrl+C to stop the server.\n")

    # Automatically launch the web interface in the browser
    open_browser(app_url)

    # Start the FastAPI server cleanly
    try:
        uvicorn.run(
            "backend.app.main:app",
            host=host,
            port=port,
            reload=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
