import asyncio
from collections.abc import Awaitable, Callable

from ..model.agent import Agent
from ..model.run import Run
from ..providers.claude_provider import ClaudeProvider
from ..schemas.orchestrator import Decision, Delegation, RunEvent

MAX_STEPS = 6

SYSTEM_PROMPT = """\
You are the Orchestrator of a digital company. You receive a request from the \
user and the roster of specialist agents. Decide which agents should do the \
work, delegate it, combine their results and deliver the final answer.

- Delegate only what a specialist is suited for. If no specialist fits, do the \
work yourself (your current directory is your workspace; you can create files \
and search the web).
- Agents cannot see the user's request nor each other's work: every delegated \
prompt must be self-contained and include any context or earlier results the \
agent needs.
- Agents in the same "delegate" list run in parallel. If one task depends on \
another's result, delegate it in a later turn.

Reply with ONLY one JSON object, nothing else:
  {"delegate": [{"agent_id": "<id from the roster>", "prompt": "<task>"}]}
  {"final": "<the finished deliverable for the user>"}"""

orchestrator = Agent(
    "Orchestrator", ClaudeProvider("orchestrator", system_prompt=SYSTEM_PROMPT)
)

Emit = Callable[[RunEvent], Awaitable[None]]


def _parse(reply: str) -> Decision | None:
    try:
        return Decision.model_validate_json(
            reply[reply.index("{") : reply.rindex("}") + 1]
        )
    except ValueError:  # no JSON, or JSON that is not a valid Decision
        return None


async def _delegate(agents: dict[str, Agent], task: Delegation, emit: Emit) -> str:
    agent = agents.get(task.agent_id)
    if agent is None:
        result = "ERROR: unknown agent_id"
        await emit(RunEvent(type="agent_replied", content=result))
        return f"[unknown agent] task: {task.prompt}\nresult: {result}"

    await emit(RunEvent(type="delegated", agent=agent.name, content=task.prompt))
    await emit(RunEvent(type="agent_working", agent=agent.name))
    try:
        result = await agent.provider.execute(task.prompt)
    except RuntimeError as e:
        result = f"ERROR: {e}"
    await emit(
        RunEvent(
            type="agent_replied",
            agent=agent.name,
            content=result,
            workspace=agent.provider.workspace,
        )
    )
    return f"[{agent.name}] task: {task.prompt}\nresult: {result}"


async def run_orchestrator(request: str, agents: list[Agent], emit: Emit) -> None:
    by_id = {a.id: a for a in agents}
    roster = (
        "\n".join(f"- id={a.id} | {a.name} | {a.instructions}" for a in agents)
        or "(no agents yet)"
    )

    transcript: list[str] = []
    for _ in range(MAX_STEPS):
        await emit(RunEvent(type="orchestrator_thinking"))
        reply = await orchestrator.provider.execute(
            f"USER REQUEST:\n{request}\n\nAGENTS:\n{roster}\n\n"
            f"WORK SO FAR:\n{chr(10).join(transcript) or '(nothing yet)'}\n\n"
            "Reply with the JSON for your next move."
        )
        decision = _parse(reply)
        if decision is None or not decision.delegate:
            final = decision.final if decision and decision.final else reply
            await emit(RunEvent(type="final", content=final))
            return
        transcript += await asyncio.gather(
            *(_delegate(by_id, t, emit) for t in decision.delegate)
        )

    raise RuntimeError(f"Orchestrator did not finish in {MAX_STEPS} steps")


async def execute_run(run: Run, agents: list[Agent]) -> None:
    await run.publish(RunEvent(type="run_started", content=run.prompt))
    try:
        await run_orchestrator(run.prompt, agents, run.publish)
    except Exception as e:
        await run.publish(RunEvent(type="error", content=str(e)))
