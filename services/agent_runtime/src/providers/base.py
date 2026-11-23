import asyncio


class BaseProvider:
    def __init__(self, name: str):
        self.name = name

    async def execute(self, command: str, args: str, prompt: str) -> str:
        process = await asyncio.create_subprocess_exec(
            command,
            args,
            prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(stderr.decode())

        return stdout.decode().strip()
