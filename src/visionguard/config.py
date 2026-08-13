"""Validated application configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from visionguard.exceptions import ConfigurationError


class StrictModel(BaseModel):
    """Base model that rejects unknown configuration properties."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class ApplicationConfig(StrictModel):
    name: str = "VisionGuard"
    version: str = "1.0.0"
    theme: str = "dark"
    data_directory: Path = Path("data")
    reports_directory: Path = Path("reports")
    database_path: Path = Path("data/visionguard.db")
    log_path: Path = Path("data/visionguard.log")


class CameraConfig(StrictModel):
    index: int = Field(default=0, ge=0)
    width: int = Field(default=1280, ge=320)
    height: int = Field(default=720, ge=240)
    target_fps: int = Field(default=30, ge=1, le=240)
    mirror: bool = True
    inference_width: int = Field(default=960, ge=320)
    inference_height: int = Field(default=540, ge=240)


class FaceConfig(StrictModel):
    max_faces: int = Field(default=1, ge=1, le=4)
    min_detection_confidence: float = Field(default=0.6, ge=0.0, le=1.0)
    min_tracking_confidence: float = Field(default=0.6, ge=0.0, le=1.0)
    refine_landmarks: bool = True


class BlinkConfig(StrictModel):
    calibration_seconds: float = Field(default=5.0, gt=0.0)
    close_ratio: float = Field(default=0.72, gt=0.0, lt=1.0)
    reopen_ratio: float = Field(default=0.82, gt=0.0, le=1.2)
    minimum_blink_ms: int = Field(default=70, ge=20)
    maximum_blink_ms: int = Field(default=500, ge=100)
    prolonged_closure_ms: int = Field(default=700, ge=200)
    missing_face_reset_ms: int = Field(default=1000, ge=100)


class PerclosConfig(StrictModel):
    window_seconds: float = Field(default=60.0, gt=1.0)
    closure_ratio: float = Field(default=0.8, gt=0.0, le=1.0)
    warning_threshold: float = Field(default=0.25, ge=0.0, le=1.0)
    minimum_valid_seconds: float = Field(default=20.0, ge=0.0)


class DistanceConfig(StrictModel):
    enabled: bool = True
    reference_distance_cm: float = Field(default=60.0, gt=0.0)
    warning_distance_cm: float = Field(default=40.0, gt=0.0)
    maximum_yaw_degrees: float = Field(default=20.0, gt=0.0)


class HeadPoseConfig(StrictModel):
    enabled: bool = True
    pitch_warning_degrees: float = Field(default=20.0, gt=0.0)
    yaw_warning_degrees: float = Field(default=25.0, gt=0.0)
    roll_warning_degrees: float = Field(default=15.0, gt=0.0)
    warning_duration_seconds: float = Field(default=5.0, gt=0.0)


class LightingConfig(StrictModel):
    dark_luminance_threshold: float = Field(default=55.0, ge=0.0, le=255.0)
    bright_luminance_threshold: float = Field(
        default=210.0,
        ge=0.0,
        le=255.0,
    )
    low_contrast_threshold: float = Field(default=18.0, ge=0.0)
    imbalance_threshold: float = Field(default=35.0, ge=0.0)


class MonitoringConfig(StrictModel):
    break_interval_minutes: int = Field(default=20, ge=1)
    break_duration_seconds: int = Field(default=20, ge=1)
    sample_interval_seconds: float = Field(default=1.0, gt=0.0)
    warning_cooldown_seconds: float = Field(default=10.0, ge=0.0)
    save_screenshots: bool = False


class PrivacyConfig(StrictModel):
    store_raw_frames: bool = False
    store_landmarks: bool = False
    store_user_name: bool = True


class ReportConfig(StrictModel):
    include_charts: bool = True
    include_screenshot: bool = False
    disclaimer: str


class Settings(StrictModel):
    application: ApplicationConfig
    camera: CameraConfig
    face: FaceConfig
    blink: BlinkConfig
    perclos: PerclosConfig
    distance: DistanceConfig
    head_pose: HeadPoseConfig
    lighting: LightingConfig
    monitoring: MonitoringConfig
    privacy: PrivacyConfig
    reports: ReportConfig


def load_settings(path: str | Path = "configs/default.yaml") -> Settings:
    """Load and validate the YAML configuration file."""

    config_path = Path(path)

    if not config_path.exists():
        raise ConfigurationError(
            f"Configuration file was not found: {config_path.resolve()}"
        )

    try:
        with config_path.open("r", encoding="utf-8") as file:
            raw_config: dict[str, Any] = yaml.safe_load(file) or {}
        settings = Settings.model_validate(raw_config)
    except OSError as exc:
        raise ConfigurationError(
            f"Unable to read configuration: {exc}"
        ) from exc
    except yaml.YAMLError as exc:
        raise ConfigurationError(
            f"Invalid YAML in {config_path}: {exc}"
        ) from exc
    except ValidationError as exc:
        raise ConfigurationError(
            f"Configuration validation failed:\n{exc}"
        ) from exc

    settings.application.data_directory.mkdir(parents=True, exist_ok=True)
    settings.application.reports_directory.mkdir(parents=True, exist_ok=True)

    return settings