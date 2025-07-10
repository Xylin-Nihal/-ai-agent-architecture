# core/goal_coordinator.py
from queue import PriorityQueue
from loguru import logger

class Goal:
    def __init__(self, goal_id, goal_type, payload=None, priority=1):
        self.id = goal_id
        self.type = goal_type
        self.payload = payload or {}
        self.priority = priority

class GoalCoordinator:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.active_goals = PriorityQueue()

    def submit_goal(self, goal):
        self.active_goals.put((goal.priority, goal))
        logger.info(f"Goal submitted: {goal.id} - {goal.type}")

    async def broadcast_goals(self):
        while not self.active_goals.empty():
            _, goal = self.active_goals.get()
            await self.event_bus.publish(f"goal.{goal.type}", goal)
            logger.info(f"Goal broadcasted: {goal.id} -> goal.{goal.type}")
