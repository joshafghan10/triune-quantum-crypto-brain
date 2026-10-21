from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from .brains import DecisionBrain, MetaBrain, PerceptionBrain, ResearchBrain
from .config import CONFIG
from .message_bus import MessageBus
from .quantum import QuantumAdapter


class DemoSimulator:
    def __init__(self):
        self.bus = MessageBus(limit=CONFIG.message_limit)
        self.quantum = QuantumAdapter()
        self.perception = PerceptionBrain(CONFIG.perception_name, self.bus, self.quantum)
        self.research = ResearchBrain(CONFIG.research_name, self.bus, self.quantum)
        self.decision = DecisionBrain(CONFIG.decision_name, self.bus, self.quantum)
        self.meta = MetaBrain(CONFIG.meta_name, self.bus, self.quantum)
        self.step = 0

    async def run(self):
        while True:
            await self.perception.tick(self.step)
            await self.research.tick(self.step)
            await self.decision.tick(self.step)
            await self.meta.tick(self.step, self.bus)
            self.step += 1
            await asyncio.sleep(CONFIG.tick_seconds)

    def snapshot(self) -> dict:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "brains": [
                {
                    "name": self.perception.name,
                    "state": self.perception.state,
                    "confidence": self.perception.confidence,
                    "throughput": self.perception.throughput,
                    "last_update": self.perception.last_update,
                },
                {
                    "name": self.research.name,
                    "state": self.research.state,
                    "confidence": self.research.confidence,
                    "throughput": self.research.throughput,
                    "last_update": self.research.last_update,
                },
                {
                    "name": self.decision.name,
                    "state": self.decision.state,
                    "confidence": self.decision.confidence,
                    "throughput": self.decision.throughput,
                    "last_update": self.decision.last_update,
                },
                {
                    "name": self.meta.name,
                    "state": self.meta.state,
                    "confidence": self.meta.confidence,
                    "throughput": self.meta.throughput,
                    "last_update": self.meta.last_update,
                },
            ],
            "message_count": len(self.bus.history),
            "recent_messages": [
                {
                    "message_id": msg.message_id,
                    "sender": msg.sender,
                    "receiver": msg.receiver,
                    "type": msg.message_type,
                    "priority": msg.priority,
                    "timestamp": msg.timestamp,
                }
                for msg in list(self.bus.history)[-8:]
            ],
        }
