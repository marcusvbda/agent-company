import json
import os

from .base import BaseProvider

DEFAULT_TOOLS = "Read,Write,Edit,Glob,Grep,WebFetch,WebSearch"


class ClaudeProvider(BaseProvider):
    def __init__(self, name="claude", tools: str = DEFAULT_TOOLS, **kwargs):
        super().__init__(name, **kwargs)
        self.tools = tools

    async def execute(self, prompt: str) -> str:
        args = [
            "claude",
            "-p",
            "--output-format",
            "json",
            "--system-prompt",
            self.system_prompt,
            "--restricted",
            "--tools",
            self.tools,
            "--allowedTools",
            self.tools,
            "--permission-mode",
            "dontAsk",
            "--setting-sources",
            "",
            "--disable-slash-commands",
            "--strict-mcp-config",
            "--no-session-persistence",
        ]
        if self.model:
            args += ["--model", self.model]
        if self.effort:
            args += ["--effort", self.effort]

        env = {
            k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"
        }  # force the account login, not an API key
        env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"

        returncode, stdout, stderr = await self._run_cli(args, prompt, env)

        try:
            result = json.loads(stdout)
        except json.JSONDecodeError:
            raise RuntimeError((stderr or stdout).decode().strip())

        if returncode != 0 or result.get("is_error"):
            raise RuntimeError(result.get("result") or stderr.decode().strip())

        return result["result"].strip()
