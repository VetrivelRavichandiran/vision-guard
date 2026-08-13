"""Application context and lifecycle manager."""

from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication

from visionguard.capture.camera import CameraThread
from visionguard.config import load_settings
from visionguard.persistence.database import DatabaseManager
from visionguard.ui.main_window import MainWindow
from visionguard.vision.face_analyzer import FaceAnalyzer


class VisionGuardApp:
    """Orchestrates application startup, thread connections, and GUI loop."""

    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.settings = load_settings()
        self.db = DatabaseManager(self.settings.application.database_path)

        self.window = MainWindow(self.settings, self.db)
        self.camera_thread = CameraThread(self.settings.camera)
        self.analyzer = FaceAnalyzer(self.settings)

        # Wire Qt Signal-Slot Pipeline
        self.camera_thread.frame_captured.connect(self.analyzer.process_frame)
        self.analyzer.metrics_ready.connect(self.window.update_metrics)

    def run(self) -> int:
        self.window.show()
        self.camera_thread.start()

        exit_code = self.app.exec()

        self.camera_thread.stop()
        self.db.close()
        return exit_code