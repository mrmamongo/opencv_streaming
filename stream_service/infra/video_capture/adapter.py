import threading

import cv2
from cv2.typing import MatLike

from stream_service.config import VCConfig


class VideoCaptureAdapter:
    def __init__(self, vc_config: VCConfig) -> None:
        self.lock = threading.RLock()
        self.capture = cv2.VideoCapture(vc_config.link)

    def read(self) -> tuple[bool, MatLike]:
        with self.lock:
            return self.capture.read()
