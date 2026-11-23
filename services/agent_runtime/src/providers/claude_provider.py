import asyncio
import json
import os
import tempfile

from .base import BaseProvider

SYSTEM_PROMPT = "You are a helpful assistant. Reply with plain text only."


class ClaudeProvider(BaseProvider):
    def __init__(self, name="claude", model: str | None = None):
        super().__init__(name)
        self.model = model

    async def execute(self, prompt: str) -> str:
        # Strip Claude Code down to a plain model call that still uses the
        # logged-in account: no tools, no settings/CLAUDE.md/MCP/skills, no
        # session saved, and an empty cwd so there is no project to inspect.
        args = [
            "claude",
            "-p",
            "--output-format", "json",
            "--system-prompt", SYSTEM_PROMPT,
            "--tools", "",
            "--setting-sources", "",
            "--disable-slash-commands",
            "--strict-mcp-config",
            "--no-session-persistence",
        ]
        if self.model:
            args += ["--model", self.model]

        env = {
            k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"
        }  # force the account login, not an API key
        env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"

        with tempfile.TemporaryDirectory() as empty_dir:
            process = await asyncio.create_subprocess_exec(
                *args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=empty_dir,
                env=env,
            )
            stdout, stderr = await process.communicate(prompt.encode())

        try:
            result = json.loads(stdout)
        except json.JSONDecodeError:
            raise RuntimeError((stderr or stdout).decode().strip())

        if process.returncode != 0 or result.get("is_error"):
            raise RuntimeError(result.get("result") or stderr.decode().strip())

        return result["result"].strip()
