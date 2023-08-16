import logging

import cv2.dnn
import numpy as np

from stream_service.application.detection_service.dto import Image
from stream_service.config import DetectionConfig
from stream_service.infra.video_capture.adapter import VideoCaptureAdapter

logger = logging.getLogger("DetectionService")


class DetectionService:
    def __init__(self, vc_adapter: VideoCaptureAdapter, config: DetectionConfig) -> None:
        self.vc_adapter = vc_adapter
        self.threshold = config.threshold
        self.nms_threshold = config.nms_threshold
        self.classnames = config.classnames
        self.detection_net = cv2.dnn.DetectionModel(str(config.weights_path.absolute()),
                                                    str(config.config_path.absolute()))
        self.detection_net.setInputSize(*config.input_size)
        self.detection_net.setInputScale([config.input_scale])
        self.detection_net.setInputMean(config.input_mean)
        self.detection_net.setInputSwapRB(config.input_swap_rb)

    async def detect(self) -> Image:
        success, img = self.vc_adapter.read()
        classids, confs, bbox = self.detection_net.detect(img, confThreshold=self.threshold)
        confs = np.array(confs, dtype=float).reshape(1, -1)[0]
        indices = cv2.dnn.NMSBoxes(bbox, confs, self.threshold, self.nms_threshold)

        objects = []
        for indice, box, classid, conf in zip(indices, bbox, classids, confs):
            x, y, w, h = box
            cv2.rectangle(img, (x, y), (x + w, h + y), color=(0, 255, 0), thickness=2)
            cv2.putText(img, self.classnames[classid].upper(), (x + 5, y - 1), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                        fontScale=0.8,
                        color=(0, 255, 0), thickness=2)
            objects.append(f"{self.classnames[classid]} - {round(conf * 100)}%")
            logger.info("".join(objects))

        return Image(objects=objects, img=img)
