"""Application-specific exceptions for VisionGuard."""


class VisionGuardError(Exception):
    """Base exception for expected VisionGuard failures."""


class ConfigurationError(VisionGuardError):
    """Raised when configuration is missing or invalid."""


class CameraError(VisionGuardError):
    """Raised when camera initialization or capture fails."""


class FaceAnalysisError(VisionGuardError):
    """Raised when the face-analysis pipeline cannot initialize or process."""


class PersistenceError(VisionGuardError):
    """Raised when session data cannot be stored or loaded from SQLite."""


class ReportGenerationError(VisionGuardError):
    """Raised when a PDF report cannot be generated."""