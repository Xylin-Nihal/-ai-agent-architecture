# core/state_manager.py
import asyncio
from loguru import logger
from collections import defaultdict

class StateStore:
    def __init__(self):
        self.state = {}

    def get_subset(self, keys):
        return {k: self.state.get(k) for k in keys}

    def update(self, updates):
        self.state.update(updates)
        logger.info(f"State updated: {updates}")

class StateManager:
    def __init__(self):
        self.global_state = StateStore()
        self.locks = defaultdict(asyncio.Lock)
        self.version = 0

    async def get_state(self, module_id, keys):
        async with self.locks[module_id]:
            return self.global_state.get_subset(keys)

    async def update_state(self, module_id, updates):
        async with self.locks[module_id]:
            self.global_state.update(updates)
            self.version += 1
            logger.info(f"{module_id} updated state to version {self.version}")
