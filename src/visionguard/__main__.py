"""Entry point for python -m visionguard or CLI script."""

from __future__ import annotations

import sys
from visionguard.application import VisionGuardApp
from visionguard.config import load_settings
from visionguard.logging_setup import configure_logging


def main() -> None:
    settings = load_settings()
    configure_logging(settings.application.log_path, verbose=True)

    app = VisionGuardApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()