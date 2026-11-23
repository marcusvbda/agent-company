import asyncio

from ..model.agent import Agent
from ..model.sector import Sector
from ..providers.claude_provider import ClaudeProvider
from ..schemas.orchestrator import Decision, Delegation, OrchestratorResponse, Step

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


def _parse(reply: str) -> Decision | None:
    try:
        return Decision.model_validate_json(
            reply[reply.index("{") : reply.rindex("}") + 1]
        )
    except ValueError:  # no JSON, or JSON that is not a valid Decision
        return None


async def _delegate(agents: dict[str, Agent], task: Delegation) -> Step:
    agent = agents.get(task.agent_id)
    if agent is None:
        return Step(agent=None, task=task.prompt, result="ERROR: unknown agent_id")
    try:
        result = await agent.provider.execute(task.prompt)
    except RuntimeError as e:
        result = f"ERROR: {e}"
    return Step(
        agent=agent.name,
        workspace=agent.provider.workspace,
        task=task.prompt,
        result=result,
    )


async def run_orchestrator(request: str, sectors: list[Sector]) -> OrchestratorResponse:
    agents = {a.id: a for s in sectors for a in s.agents}
    roster = (
        "\n".join(
            f"- id={a.id} | {a.name} | sector: {s.name} | {a.instructions}"
            for s in sectors
            for a in s.agents
        )
        or "(no agents yet)"
    )

    steps: list[Step] = []
    for _ in range(MAX_STEPS):
        work = (
            "\n\n".join(
                f"[{s.agent}] task: {s.task}\nresult: {s.result}" for s in steps
            )
            or "(nothing yet)"
        )
        reply = await orchestrator.provider.execute(
            f"USER REQUEST:\n{request}\n\nAGENTS:\n{roster}\n\n"
            f"WORK SO FAR:\n{work}\n\nReply with the JSON for your next move."
        )
        decision = _parse(reply)
        if decision is None or not decision.delegate:
            # Not a delegation: whatever it said is the deliverable.
            final = decision.final if decision and decision.final else reply
            return OrchestratorResponse(result=final, steps=steps)
        steps += await asyncio.gather(
            *(_delegate(agents, t) for t in decision.delegate)
        )

    raise RuntimeError(f"Orchestrator did not finish in {MAX_STEPS} steps")
