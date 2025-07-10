# modules/perception.py
from loguru import logger

class PerceptionModule:
    def __init__(self, module_id):
        self.module_id = module_id

    async def handle_event(self, event):
        logger.info(f"[{self.module_id}] Perceived Event: {event.type}")
        logger.info(f"[{self.module_id}] Payload: {event.data.payload}")
        
        # Simulate context processing (in real case, call vision/audio/text processors)
        perceived_context = {
            "summary": f"Processed input: {event.data.payload.get('input', '')}",
            "source": self.module_id
        }

        return perceived_context
