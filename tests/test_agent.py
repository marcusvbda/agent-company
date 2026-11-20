import unittest

from classes.agent import Agent

class TestAgent(unittest.TestCase):
    
    def test_message_create_successfully(self):
        agent_name = "lorem ipsum"
        agent = Agent(agent_name)
        self.assertEqual(agent.name, agent_name)
                

if __name__ == "__main__":
    unittest.main()