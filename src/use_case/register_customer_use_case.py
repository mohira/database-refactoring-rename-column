import uuid
from dataclasses import dataclass

from src.domain.customer import Customer
from src.domain.customer_id import CustomerId
from src.domain.f_name import FName
from src.port.customer_repository import CustomerRepository


@dataclass
class RegisterCustomerUseCase:
    customer_repository: CustomerRepository

    def do(self, fname: str) -> None:
        # MEMO: UseCase内でドメインオブジェクトを組み立てるパターン
        customer_id = CustomerId(str(uuid.uuid4()))
        fname = FName(fname)

        customer = Customer(customer_id, fname)

        self.customer_repository.insert(customer)
