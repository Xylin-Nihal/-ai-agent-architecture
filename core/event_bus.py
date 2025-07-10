# core/event_bus.py
import asyncio
from collections import defaultdict
from loguru import logger
import time

class Event:
    def __init__(self, type, data, timestamp=None):
        self.type = type
        self.data = data
        self.timestamp = timestamp or time.time()

class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)  # {event_type: [(module_name, callback)]}
        self.event_queue = asyncio.Queue()
        self.dead_letter_queue = asyncio.Queue()

    async def publish(self, event_type, data):
        event = Event(event_type, data)
        await self.event_queue.put(event)
        logger.info(f"Event published: {event_type}")

    def subscribe(self, module_id, event_types, callback):
        for event_type in event_types:
            self.subscribers[event_type].append((module_id, callback))
        logger.info(f"{module_id} subscribed to {event_types}")

    async def start_dispatcher(self):
        while True:
            event = await self.event_queue.get()
            dispatched = False
            if event.type in self.subscribers:
                for _, callback in self.subscribers[event.type]:
                    asyncio.create_task(callback(event))
                    dispatched = True
            if not dispatched:
                await self.dead_letter_queue.put(event)
                logger.warning(f"Undeliverable event: {event.type}")
