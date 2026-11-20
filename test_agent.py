import unittest

from main import Agent, Message

class TestAgent(unittest.TestCase):
    
    def test_execute_returns_expected_string(self):
        agent = Agent("Writer")
        result = agent.execute("Write a post")
        self.assertEqual(result, "Writer is executing: Write a post")

    def test_delegate_returns_result_from_recipient(self):
        manager = Agent("Manager")
        writer = Agent("Writer")
        message = Message(manager.name, writer.name, "Write an Instagram post about Python")
        result = manager.delegate(writer, message)
        self.assertEqual(result, "Writer is executing: Write an Instagram post about Python")

    def test_message_stores_fields(self):
        message = Message("Manager", "Writer", "Write a post")
        self.assertEqual(message.sender, "Manager")
        self.assertEqual(message.recipient, "Writer")
        self.assertEqual(message.task, "Write a post")


if __name__ == "__main__":
    unittest.main()