#!/usr/bin/python3
"""Defines the BaseModel class."""
import uuid
from datetime import datetime

import models


class BaseModel:
    """Represents the BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        self.id = str(
            uuid.UUID(
                bytes_le=uuid.uuid4().bytes_le, is_safe=uuid.SafeUUID.safe
            )
        )
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if not kwargs:
            models.storage.new(self)

        else:
            tform = "%Y-%m-%dT%H:%M:%S.%f"
            for k, v in kwargs.items():
                self.__dict__[k] = (
                    datetime.strptime(v, tform)
                    if k in ["created_at", "updated_at"]
                    else v
                )

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance.
        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        rdict = self.__dict__.copy()
        rdict["created_at"] = self.created_at.isoformat()
        rdict["updated_at"] = self.updated_at.isoformat()
        rdict["__class__"] = self.__class__.__name__

        return rdict

    def __str__(self):
        """Return the print/str representation of the BaseModel instance."""
        clname = self.__class__.__name__
        return f"[{clname}] ({self.id}) {self.__dict__}"
