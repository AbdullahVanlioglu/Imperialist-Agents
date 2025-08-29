import asyncio
from imperialist_agents.core.config import Settings
from imperialist_agents.core.registry import Registries
from imperialist_agents.core.models import load_model
from imperialist_agents.core.planning import load_planner
from imperialist_agents.core.execution import Executor
from imperialist_agents.core.memory import load_memory
from imperialist_agents.skills.base import load_skills
from imperialist_agents.connectors.base import load_connectors


async def run_task(goal: str):
    cfg = Settings.load()
    regs = Registries()


# Load plugins from config
memory = load_memory(cfg.memory.impl)
model = load_model(cfg.runtime.model)
skills = load_skills(cfg.skills)
connectors = load_connectors(cfg.connectors)
executor = Executor(skills=skills, connectors=connectors, workspace_dir=cfg.runtime.workspace_dir)
planner = load_planner(cfg.planning.style, model=model, executor=executor, memory=memory, verifier_name=cfg.planning.verifier, max_steps=cfg.runtime.max_steps)


result = await planner.run(goal)
return result