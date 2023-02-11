#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.
Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""

import contextlib
import os
import unittest

import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(cls):
        with contextlib.suppress(IOError):
            os.rename("file.json", "tmp")

    @classmethod
    def tearDown(cls):
        with contextlib.suppress(IOError):
            os.remove("file.json")
        with contextlib.suppress(IOError):
            os.rename("tmp", "file.json")
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        self.assertIn(f"BaseModel.{bm.id}", models.storage.all().keys())
        self.assertIn(bm, models.storage.all().values())
        self.assertIn(f"User.{us.id}", models.storage.all().keys())
        self.assertIn(us, models.storage.all().values())
        self.assertIn(f"State.{st.id}", models.storage.all().keys())
        self.assertIn(st, models.storage.all().values())
        self.assertIn(f"Place.{pl.id}", models.storage.all().keys())
        self.assertIn(pl, models.storage.all().values())
        self.assertIn(f"City.{cy.id}", models.storage.all().keys())
        self.assertIn(cy, models.storage.all().values())
        self.assertIn(f"Amenity.{am.id}", models.storage.all().keys())
        self.assertIn(am, models.storage.all().values())
        self.assertIn(f"Review.{rv.id}", models.storage.all().keys())
        self.assertIn(rv, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_with_None(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn(f"BaseModel.{bm.id}", save_text)
            self.assertIn(f"User.{us.id}", save_text)
            self.assertIn(f"State.{st.id}", save_text)
            self.assertIn(f"Place.{pl.id}", save_text)
            self.assertIn(f"City.{cy.id}", save_text)
            self.assertIn(f"Amenity.{am.id}", save_text)
            self.assertIn(f"Review.{rv.id}", save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn(f"BaseModel.{bm.id}", objs)
        self.assertIn(f"User.{us.id}", objs)
        self.assertIn(f"State.{st.id}", objs)
        self.assertIn(f"Place.{pl.id}", objs)
        self.assertIn(f"City.{cy.id}", objs)
        self.assertIn(f"Amenity.{am.id}", objs)
        self.assertIn(f"Review.{rv.id}", objs)

    def test_reload_no_file(self):
        self.assertRaises(FileNotFoundError, models.storage.reload())

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
