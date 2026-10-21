import asyncio
from collections import deque
from typing import Deque

from .config import CONFIG
from .models import NeuroSymbolicMessage


class MessageBus:
    def __init__(self, limit: int = CONFIG.message_limit):
        self.limit = limit
        self.history: Deque[NeuroSymbolicMessage] = deque(maxlen=limit)
        self.subscribers: list[asyncio.Queue] = []

    async def subscribe(self) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue()
        self.subscribers.append(queue)
        return queue

    async def publish(self, message: NeuroSymbolicMessage) -> None:
        self.history.append(message)
        for queue in list(self.subscribers):
            await queue.put(message)

    def latest(self, n: int = 20) -> list[NeuroSymbolicMessage]:
        return list(self.history)[-n:]
