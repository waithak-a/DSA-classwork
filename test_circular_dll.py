import unittest
import io
import sys

from circular_dll import CircularDoublyLinkedList  # This assumes the main code is in circular_dll.py

class TestCircularDoublyLinkedList(unittest.TestCase):

    def setUp(self):
        self.list = CircularDoublyLinkedList()

        # Flexibly map method aliases for insertion
        if hasattr(self.list, "insert_at_end"):
            self.list.insert_end = self.list.insert_at_end
        elif hasattr(self.list, "add_node"):
            self.list.insert_end = self.list.add_node
        else:
            self.list.insert_end = None

        # Flexibly map method for insertion at beginning
        if hasattr(self.list, "insert_at_beginning"):
            self.list.insert_start = self.list.insert_at_beginning
        else:
            self.list.insert_start = None

        # Flexibly map method for removal
        if hasattr(self.list, "remove_by_value"):
            self.list.remove_value = self.list.remove_by_value
        else:
            self.list.remove_value = None

        # Flexibly map display methods
        self.list.display_forward = getattr(self.list, "show_list_forward", lambda: None)
        self.list.display_backward = getattr(self.list, "show_list_backward", lambda: None)

    def capture_output(self, func):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        func()
        sys.stdout = sys.__stdout__
        return captured_output.getvalue().strip()

    def test_insertion_end(self):
        self.assertIsNotNone(self.list.insert_end, "Insert method not found.")
        self.list.insert_end(10)
        self.list.insert_end(20)
        self.list.insert_end(30)
        output = self.capture_output(self.list.display_forward)
        self.assertIn("10", output)
        self.assertIn("30", output)

    def test_insertion_start(self):
        if self.list.insert_start is None:
            self.skipTest("No method found for inserting at beginning.")
        self.list.insert_start(5)
        output = self.capture_output(self.list.display_forward)
        self.assertIn("5", output)

    def test_removal(self):
        self.assertIsNotNone(self.list.remove_value, "Remove method not found.")
        self.list.insert_end(10)
        self.list.insert_end(20)
        self.list.insert_end(30)
        self.list.remove_value(20)
        output = self.capture_output(self.list.display_forward)
        self.assertNotIn("20", output)
        self.assertIn("10", output)

    def test_backward_display(self):
        self.list.insert_end(1)
        self.list.insert_end(2)
        self.list.insert_end(3)
        output = self.capture_output(self.list.display_backward)
        self.assertTrue("3" in output and "1" in output)

    def test_remove_nonexistent_value(self):
        self.list.insert_end(1)
        output = self.capture_output(lambda: self.list.remove_value(99))
        self.assertIn("not found", output.lower())

    def test_empty_list_display(self):
        output = self.capture_output(self.list.display_forward)
        self.assertIn("empty", output.lower())

if __name__ == '__main__':
    unittest.main()
