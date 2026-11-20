import unittest

from classes.message import Message

class TestMessage(unittest.TestCase):
    
    def test_message_create_successfully(self):
        sender_name = "Writer"
        recipient_name = "Editor"
        task_description = "Write an Instagram post about Python"
        message = Message(sender_name, recipient_name, task_description)
        self.assertEqual(message.sender, sender_name)
        self.assertEqual(message.recipient, recipient_name)
        self.assertEqual(message.task, task_description)
                

if __name__ == "__main__":
    unittest.main()