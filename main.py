class Agent:
    def __init__(self, name):
        self.name = name
        
    def execute(self, task):
        return f"{self.name} is executing: {task}"
    
    def delegate(self, agent, task):
        return agent.execute(task)
    

manager = Agent("Manager")
writer = Agent("Writer")
designer = Agent("Designer")

resultWriter = manager.delegate(writer, "Write an Instagram post about Python")
resultDesigner = manager.delegate(designer, "Create an image to an Instagram post about Python")

print(resultWriter)
print(resultDesigner)