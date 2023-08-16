import ormsgpack
from nats.aio.client import Client
from nats.aio.msg import Msg

from stream_service.application.detection_service.service import DetectionService


class NatsHandler:
    def __init__(self, nc: Client, vc_service: DetectionService) -> None:
        self.nc = nc
        self.service = vc_service

    async def setup(self) -> None:
        js = self.nc.jetstream()

        js.subscribe(subject="event.detect", stream="events", cb=self.handle_detect)

    async def handle_detect(self, msg: Msg) -> None:
        message_id = msg.header["X-Message-ID"]
        image = await self.service.detect()

        js = self.nc.jetstream()
        await js.publish(
            stream="events",
            subject="stream.detect",
            payload=ormsgpack.packb(image.dict()),
            headers={"X-Message-ID": message_id}
        )
