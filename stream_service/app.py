import asyncio
import logging

from nats.aio.client import Client

from stream_service.application.detection_service.service import DetectionService
from stream_service.config import Config
from stream_service.exceptions import DisposeException, StartServerException
from stream_service.infra.nats.main import setup_nats
from stream_service.infra.video_capture.adapter import VideoCaptureAdapter
from stream_service.presentation.nats.main import NatsHandler

logger = logging.getLogger(__name__)


class Application:
    def __init__(self, nc: Client, handler: NatsHandler) -> None:
        self.nc = nc
        self.handler = handler

    @classmethod
    async def from_config(cls, config: Config) -> "Application":
        logger.info(f"Initializing Application from config: {config}")

        logger.info("Initializing Video Capture Adapter")
        vc_adapter = VideoCaptureAdapter(config.video_capture)

        logger.info("Initializing Detection Service")
        detection_service = DetectionService(vc_adapter, config.detection)

        logger.info("Initializing NATS")
        nc = await setup_nats(config.nats)

        logger.info("Initializing NatsHandler")
        handler = NatsHandler(nc, detection_service)

        return Application(
            nc, handler
        )

    async def start(self) -> None:
        logger.info("Service is starting")

        try:
            await self.handler.setup()
            await asyncio.Future()
        except asyncio.CancelledError:
            logger.info("HTTP server has been interrupted")
        except BaseException as unexpected_error:
            logger.exception("HTTP server failed to start")

            raise StartServerException from unexpected_error

    async def dispose(self) -> None:
        logger.info("Application is shutting down...")

        dispose_errors: list[str] = []

        # TODO: закрыть все соединения\освободить все ресурсы

        if len(dispose_errors) != 0:
            logger.error("Application has shut down with errors")
            raise DisposeException(
                "Application has shut down with errors, see logs above"
            )

        logger.info("Application has successfully shut down")
