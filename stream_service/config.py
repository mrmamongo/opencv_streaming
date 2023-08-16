from pathlib import Path

from pydantic import BaseSettings, Field


class DetectionConfig(BaseSettings):
    classnames: list[str] = Field(default_factory=list)
    threshold: int = 55
    nms_threshold: int = 45

    weights_path: Path
    config_path: Path

    input_size: tuple[int, int] = (320, 320)
    input_scale: float = 1.0 / 127.5
    input_mean: tuple[float, float, float] = (127.5, 127.5, 127.5)
    input_swap_rb: bool = True


class VCConfig(BaseSettings):
    link: str


class NatsConfig(BaseSettings):
    hosts: list[str] = ['nats://localhost:4222']


class Config(BaseSettings):
    nats: NatsConfig = NatsConfig()
    video_capture: VCConfig = VCConfig()
    detection: DetectionConfig = DetectionConfig()
