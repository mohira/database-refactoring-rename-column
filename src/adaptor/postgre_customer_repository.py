from dataclasses import dataclass

from psycopg2._psycopg import connection

from src.domain.customer import Customer
from src.domain.customer_collection import CustomerCollection
from src.port.customer_repository import CustomerRepository


@dataclass
class PostgreCustomerRepository(CustomerRepository):
    conn: connection

    def insert(self, customer: Customer) -> None:
        with self.conn.cursor() as cursor:
            sql = 'INSERT INTO customer (customer_id, fname) VALUES ((%s), (%s))'

            cursor.execute(sql, (customer.id.value, customer.fname.value))

            self.conn.commit()

    def find_all(self) -> CustomerCollection:
        with self.conn.cursor() as cursor:
            sql = 'SELECT customer_id, fname FROM customer'

            cursor.execute(sql)

            rows = cursor.fetchall()

        return CustomerCollection.from_repository(rows)
