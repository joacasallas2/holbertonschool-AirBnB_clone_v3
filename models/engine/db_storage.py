import unittest
from models import storage
from models.state import State
from models.city import City


class TestDBStorageGet(unittest.TestCase):
    """Test cases for the get method in DBStorage."""

    @unittest.skipIf(storage.__class__.__name__ != "DBStorage", "not testing db storage")
    def test_get_existing_object(self):
        """Test retrieving an existing object."""
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        retrieved_state = storage.get(State, new_state.id)
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.id, new_state.id)

    @unittest.skipIf(storage.__class__.__name__ != "DBStorage", "not testing db storage")
    def test_get_nonexistent_object(self):
        """Test retrieving a non-existent object."""
        retrieved_state = storage.get(State, "nonexistent_id")
        self.assertIsNone(retrieved_state)

    @unittest.skipIf(storage.__class__.__name__ != "DBStorage", "not testing db storage")
    def test_get_invalid_class(self):
        """Test passing an invalid class to get method."""
        retrieved_obj = storage.get("InvalidClass", "some_id")
        self.assertIsNone(retrieved_obj)


class TestFileStorageCount(unittest.TestCase):
    """Test cases for the count method in FileStorage."""

    @unittest.skipIf(storage.__class__.__name__ != "FileStorage", "not testing file storage")
    def test_count_all_objects(self):
        """Test counting all objects in storage."""
        initial_count = storage.count()
        new_state = State(name="Texas")
        storage.new(new_state)
        storage.save()
        self.assertEqual(storage.count(), initial_count + 1)

    @unittest.skipIf(storage.__class__.__name__ != "FileStorage", "not testing file storage")
    def test_count_specific_class(self):
        """Test counting objects of a specific class."""
        initial_count = storage.count(State)
        new_state = State(name="Florida")
        storage.new(new_state)
        storage.save()
        self.assertEqual(storage.count(State), initial_count + 1)

    @unittest.skipIf(storage.__class__.__name__ != "FileStorage", "not testing file storage")
    def test_count_nonexistent_class(self):
        """Test counting a class that has no instances."""
        self.assertEqual(storage.count("InvalidClass"), 0)

if __name__ == "__main__":
    unittest.main()
