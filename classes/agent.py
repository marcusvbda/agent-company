class Agent:
    def __init__(self, name: str):
        self.name = name
        
    def execute(self, task: str) -> str:
        return f"{self.name} is executing: {task}"
    
    def delegate(self, agent: "Agent", message: Message) -> str:
        return agent.execute(message.task)