import asyncio

from .base import BaseProvider


class ClaudeProvider(BaseProvider):
    def __init__(self, name="claude"):
        super().__init__(name)

    async def execute(self, prompt: str) -> str:
        process = await asyncio.create_subprocess_exec(
            "claude",
            "--bare",
            "-p",
            prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(stderr.decode())

        return stdout.decode().strip()
