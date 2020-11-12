from pathlib import Path

import click
import psycopg2
from click import Context
from psycopg2._psycopg import connection
from psycopg2.extras import DictCursor

from src.adaptor.postgre_customer_repository import PostgreCustomerRepository
from src.use_case.register_customer_use_case import RegisterCustomerUseCase


@click.group()
def main():
    pass


@main.command()
def init():
    """テーブルを初期化する"""
    conn: connection = psycopg2.connect(
        host='localhost',
        port=5432,
        # user='',
        # password='',
        dbname='db-refactoring',
        cursor_factory=DictCursor
    )

    cursor = conn.cursor()

    p = Path(__file__).parent / 'init_table.sql'

    cursor.execute(p.read_text())

    conn.commit()

    conn.close()


@main.command()
def show():
    """登録されている顧客一覧を表示する"""
    conn: connection = psycopg2.connect(
        host='localhost',
        port=5432,
        # user='',
        # password='',
        dbname='db-refactoring',
        cursor_factory=DictCursor
    )

    cursor = conn.cursor()

    sql = 'SELECT * from customer order by customer_id'
    cursor.execute(sql)

    rows = cursor.fetchall()

    for row in rows:
        customer_id = row['customer_id']
        first_name = row['fname']

        msg_id = click.style(f'{customer_id}')
        msg_first_name = click.style(f'{first_name}', fg='green')
        msg = f'{msg_id}: {msg_first_name}'

        click.echo(msg)

    conn.close()


@main.command()
def register():
    """新しい顧客を登録する"""
    conn: connection = psycopg2.connect(
        host='localhost',
        port=5432,
        # user='',
        # password='',
        dbname='db-refactoring',
        cursor_factory=DictCursor
    )

    repository = PostgreCustomerRepository(conn)
    use_case = RegisterCustomerUseCase(repository)

    new_customer_name = input('New customer name > ')
    use_case.do(new_customer_name)


@main.command()
@click.pass_context
def rename(ctx: Context):
    """顧客の名前を変更する"""
    conn: connection = psycopg2.connect(
        host='localhost',
        port=5432,
        # user='',
        # password='',
        dbname='db-refactoring',
        cursor_factory=DictCursor
    )

    cursor = conn.cursor()

    ctx.invoke(show)

    target_customer_id = input('target customer id > ')
    new_name = input('new name > ')

    sql = 'UPDATE customer SET fname = (%s) WHERE customer_id = (%s)'

    cursor.execute(sql, (new_name, target_customer_id))

    conn.commit()

    conn.close()
