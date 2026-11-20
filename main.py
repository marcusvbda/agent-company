from classes.agent import Agent
from classes.message import Message
from classes.runtime import AgentRuntime

manager = Agent("Manager")
writer = Agent("Writer")
designer = Agent("Designer")

runtime = AgentRuntime()

runtime.register(manager)
runtime.register(writer)
runtime.register(designer)

message = Message(
    manager.name,
    writer.name,
    "Write an Instagram post about Python"
)

result = runtime.send(message)

print(result)