from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from psycopg2.extras import DictRow

from src.domain.customer import Customer


@dataclass(frozen=True)
class CustomerCollection:
    values: List[Customer] = field(default_factory=list)

    def add(self, customer: Customer) -> CustomerCollection:
        return CustomerCollection(self.values + [customer])

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, index: int) -> Customer:
        return self.values[index]

    @classmethod
    def from_repository(cls, rows: List[DictRow]) -> CustomerCollection:
        customer_collection = CustomerCollection()

        for row in rows:
            customer = Customer.from_repository(row)

            customer_collection = customer_collection.add(customer)

        return customer_collection
