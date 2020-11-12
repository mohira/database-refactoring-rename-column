import psycopg2
import pytest
from psycopg2._psycopg import connection
from psycopg2.extras import DictCursor

from src.adaptor.postgre_customer_repository import PostgreCustomerRepository
from src.domain.f_name import FName
from src.use_case.register_customer_use_case import RegisterCustomerUseCase


class TestRegisterCustomerUseCase:
    @pytest.fixture
    def dummy_db_conn(self) -> connection:
        conn: connection = psycopg2.connect(
            host='localhost',
            port=5432,
            dbname='db-refactoring-dummy',
            cursor_factory=DictCursor
        )

        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS customer')

        init_table_sql = """CREATE TABLE customer
                (
                    customer_id CHAR(36) PRIMARY KEY,
                    fname       VARCHAR(40)
                );
        """
        cursor.execute(init_table_sql)

        yield conn

        cursor.execute('DROP TABLE customer')
        conn.close()

    def test_新規顧客を登録できる(self, dummy_db_conn: connection):
        repository = PostgreCustomerRepository(dummy_db_conn)
        use_case = RegisterCustomerUseCase(repository)

        use_case.do('Smith')

        customers = repository.find_all()

        assert customers[0].fname == FName('Smith')
