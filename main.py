class Agent:
    def __init__(self, name):
        self.name = name
        
    def execute(self, task):
        return f"{self.name} is executing: {task}"
    

manager = Agent("Manager")
result = manager.execute("Say hello, to my little friend")

print(result)