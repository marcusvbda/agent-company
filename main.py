class Message:
    def __init__(self, sender: str, recipient: str, task: str):
        self.sender = sender
        self.recipient = recipient
        self.task = task
class Agent:
    def __init__(self, name: str):
        self.name = name
        
    def execute(self, task: str) -> str:
        return f"{self.name} is executing: {task}"
    
    def delegate(self, agent: "Agent", message: Message) -> str:
        return agent.execute(message.task)
    

manager = Agent("Manager")
writer = Agent("Writer")

message_writer = Message(
    manager.name,
    writer.name,
    "Write an Instagram post about Python"
)

result_writer = manager.delegate(writer, message_writer)
print(result_writer)