import nats
from nats.aio.client import Client

from stream_service.config import NatsConfig


async def setup_nats(config: NatsConfig) -> Client:
    nc = await nats.connect(config.hosts)
    js = nc.jetstream()
    await js.add_stream(name="events", subject=["stream.*", "event.*"])

    return nc
