from abc import ABCMeta, abstractmethod

from src.domain.customer import Customer
from src.domain.customer_collection import CustomerCollection


class CustomerRepository(metaclass=ABCMeta):
    @abstractmethod
    def insert(self, customer: Customer) -> None:
        pass

    @abstractmethod
    def find_all(self) -> CustomerCollection:
        pass
