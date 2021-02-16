#!/usr/bin/env python3

import logging

from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class GenericInfoProvider(ABC):

    def __init__(self):
        self.has_changed = False

    def __setattr__(self, name, value):
        if name == "has_changed":
            super().__setattr__(name, value)
        else:
            if getattr(self, name, None) != value:
                self.has_changed = True
            super().__setattr__(name, value)

    @abstractmethod
    def update(self):
        changed = self.has_changed
        self.has_changed = False
        return changed

    @abstractmethod
    def to_json(self):
        pass