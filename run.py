"""Application runner script."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import get_settings
from core.logging_config import setup_logging


def main():
    """Launch the Streamlit application."""
    import subprocess

    settings = get_settings()
    setup_logging(settings.app.log_level, settings.app.log_dir)

    issues = settings.validate()
    if issues:
        print("Configuration warnings:")
        for issue in issues:
            print(f"  - {issue}")

    app_path = Path(__file__).parent / "app" / "main.py"
    subprocess.run(
        ["streamlit", "run", str(app_path), "--server.headless", "true"],
        cwd=str(Path(__file__).parent),
    )


if __name__ == "__main__":
    main()
