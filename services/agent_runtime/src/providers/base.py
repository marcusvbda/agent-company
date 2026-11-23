import asyncio
import os
from pathlib import Path
from typing import Literal

Effort = Literal["low", "medium", "high", "xhigh", "max"]

WORKSPACES_DIR = Path(
    os.getenv("AGENT_WORKSPACES", Path.home() / "agent-company" / "workspaces")
)

SYSTEM_PROMPT = (
    "You are an autonomous agent. Your current directory is your workspace: "
    "create and edit files there. You can search and fetch the web. "
    "Do the task with your tools, then reply with a short plain-text summary."
)


class BaseProvider:
    def __init__(
        self,
        name: str,
        workspace: str | Path | None = None,
        model: str | None = None,
        effort: Effort | None = None,
        system_prompt: str = SYSTEM_PROMPT,
    ):
        self.name = name
        self.workspace = Path(workspace or WORKSPACES_DIR / name).resolve()
        self.model = model  # None = the account's default model
        self.effort = effort  # None = the model's default effort
        self.system_prompt = system_prompt

    async def execute(self, prompt: str) -> str:
        raise NotImplementedError

    async def _run_cli(
        self, args: list[str], prompt: str, env: dict[str, str] | None = None
    ) -> tuple[int, bytes, bytes]:
        """Run a provider's CLI inside the workspace, prompt on stdin."""
        self.workspace.mkdir(parents=True, exist_ok=True)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.workspace,
            env=env,
        )
        stdout, stderr = await process.communicate(prompt.encode())
        return process.returncode, stdout, stderr
