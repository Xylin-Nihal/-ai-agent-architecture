# main.py
import asyncio
from core.event_bus import EventBus
from core.state_manager import StateManager
from core.goal_coordinator import GoalCoordinator, Goal
from modules.perception import PerceptionModule
from loguru import logger

logger.add("logs.txt")

async def main():
    event_bus = EventBus()
    state_manager = StateManager()
    goal_coordinator = GoalCoordinator(event_bus)

    # Initialize Perception Module
    perception = PerceptionModule("perception")

    # Subscribe Perception to handle "goal.perceive"
    event_bus.subscribe("perception", ["goal.perceive"], perception.handle_event)

    # Start event dispatching loop
    asyncio.create_task(event_bus.start_dispatcher())

    # Submit and broadcast a sample goal
    test_goal = Goal("goal-001", "perceive", {"input": "Look around"})
    goal_coordinator.submit_goal(test_goal)
    await goal_coordinator.broadcast_goals()

    await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
