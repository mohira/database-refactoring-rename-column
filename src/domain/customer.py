from __future__ import annotations

from dataclasses import dataclass

from psycopg2.extras import DictRow

from src.domain.customer_id import CustomerId
from src.domain.f_name import FName


@dataclass(frozen=True)
class Customer:
    id: CustomerId
    fname: FName

    @classmethod
    def from_repository(cls, row: DictRow) -> Customer:
        customer_id = row['customer_id']
        fname = FName(row['fname'])

        return Customer(CustomerId(customer_id), fname)
