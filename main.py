from classes.message import Message
from classes.agent import Agent

manager = Agent("Manager")
writer = Agent("Writer")

message_writer = Message(
    manager.name,
    writer.name,
    "Write an Instagram post about Python"
)

result_writer = manager.delegate(writer, message_writer)
print(result_writer)