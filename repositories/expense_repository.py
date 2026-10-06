from abc import ABC, abstractmethod


class ExpenseRepository(ABC):

    @abstractmethod
    def save(self, expenses):
        pass

    @abstractmethod
    def load(self):
        pass