from contextlib import contextmanager
from cryptography.fernet import Fernet
from datetime import datetime
import logging
import mysql.connector
from mysql.connector import Error
import os

logger = logging.getLogger(__name__)

class DB:
    
    symmetric_key: bytes
    host: bytes
    port: bytes
    user: bytes
    password: bytes
    database: bytes

    inited: bool = False
    conn: mysql.connector.MySQLConnection = None
    cursor: mysql.connector = None
    
    @classmethod
    def setCredentials(cls, symmetric_key: bytes, host: bytes, port: bytes, user: bytes, password: bytes, database: bytes):
        cls.symmetric_key = symmetric_key
        cls.host = host
        cls.port = port
        cls.user = user
        cls.password = password
        cls.database = database
        cls.inited = True
    
    @classmethod
    def accessCredentials(cls) -> tuple:
        cipher = Fernet(cls.symmetric_key)

        host = cipher.decrypt(cls.host).decode()
        port = cipher.decrypt(cls.port).decode()
        user = cipher.decrypt(cls.user).decode()
        password = cipher.decrypt(cls.password).decode()
        database = cipher.decrypt(cls.database).decode()

        return host, port, user, password, database

    @classmethod
    def connect(cls) -> None:
        """Establish a connection to the database."""
        host, port, user, password, database = cls.accessCredentials()
        
        try:
            cls.conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            cls.cursor = cls.conn.cursor()
            logger.info('Connected to the database.')
        except Error as error:
            raise Exception(f'DB.connect.error: {error}') from error
    
    @classmethod
    def close(cls) -> None:
        """Close the database connection."""
        try:
            if cls.cursor:
                cls.cursor.close()
            if cls.conn:
                cls.conn.close()
            logger.info('Connection closed.')
        except Error as error:
            logger.info(f'DB.close.error: {error}')
    
    @classmethod
    @contextmanager
    def get_connection(cls) -> mysql.connector:
        """Context manager for handling database connection."""
        cls.connect()
        try:
            yield cls.cursor
        finally:
            cls.close()

    @classmethod
    def create_table(cls, table_name: str, columns: dict) -> None:
        """
        Create a new table with specified columns.

        Example Usage:
        columns = {'id': 'INT PRIMARY KEY AUTO_INCREMENT', 'name': 'TEXT', 'age': 'INT'}
        DB.create_table('users', columns)
        """
        with cls.get_connection() as cursor:
            try:
                col_defs = ', '.join(f'{col} {datatype}' for col, datatype in columns.items())
                query = f'CREATE TABLE IF NOT EXISTS {table_name} ({col_defs})'
                cursor.execute(query)
                cls.conn.commit()
                logger.info(f'Table \'{table_name}\' created.')
            except Error as error:
                raise Exception(f'DB.create_table.error: {error}') from error

    @classmethod
    def add_row(cls, table_name: str, data: dict) -> None:
        """
        Insert a row into the table.

        Example Usage:
        data = {'name': 'Alice', 'age': 30}
        DB.add_row('users', data)
        """
        with cls.get_connection() as cursor:
            try:
                cols = ', '.join(data.keys())
                placeholders = ', '.join(['%s'] * len(data))
                query = f'INSERT INTO {table_name} ({cols}) VALUES ({placeholders})'
                cursor.execute(query, tuple(data.values()))
                cls.conn.commit()
                logger.info(f'Row added to \'{table_name}\'.')
            except Error as error:
                raise Exception(f'DB.add_row.error: {error}') from error

    @classmethod
    def get_rows(cls, table_name: str, conditions: dict = None) -> list:
        """
        Fetch rows from the table, with optional conditions.

        Example Usage:
        # Fetch all rows
        DB.get_rows('users')

        # Fetch rows with conditions
        conditions = {'age': 30}
        DB.get_rows('users', conditions)
        """
        with cls.get_connection() as cursor:
            try:
                query = f'SELECT * FROM {table_name}'
                if conditions:
                    cond_str = ' AND '.join(f'{col} = %s' for col in conditions.keys())
                    query += f' WHERE {cond_str}'
                    cursor.execute(query, tuple(conditions.values()))
                else:
                    cursor.execute(query)

                result = cursor.fetchall()
                return result
            except Error as error:
                logger.info(f'DB.get_rows.error: {error}')
                return None

    @classmethod
    def update_row(cls, table_name: str, updates: dict, conditions: dict) -> None:
        """
        Update rows in the table with specific conditions.

        Example Usage:
        updates = {'name': 'Bob'}
        conditions = {'id': 1}
        DB.update_row('users', updates, conditions)
        """
        with cls.get_connection() as cursor:
            try:
                update_str = ', '.join(f'{col} = %s' for col in updates.keys())
                cond_str = ' AND '.join(f'{col} = %s' for col in conditions.keys())
                query = f'UPDATE {table_name} SET {update_str} WHERE {cond_str}'
                cursor.execute(query, tuple(updates.values()) + tuple(conditions.values()))
                cls.conn.commit()
                logger.info(f'Row(s) updated in \'{table_name}\'.')
            except Error as error:
                raise Exception(f'DB.update_row.error: {error}') from error

    @classmethod
    def delete_row(cls, table_name: str, conditions: dict) -> None:
        """
        Delete rows from the table based on conditions.

        Example Usage:
        conditions = {'id': 1}
        DB.delete_row('users', conditions)
        """
        with cls.get_connection() as cursor:
            try:
                cond_str = ' AND '.join(f'{col} = %s' for col in conditions.keys())
                query = f'DELETE FROM {table_name} WHERE {cond_str}'
                cursor.execute(query, tuple(conditions.values()))
                cls.conn.commit()
                logger.info(f'Row(s) deleted from \'{table_name}\'.')
            except Error as error:
                raise Exception(f'DB.delete_row.error: {error}') from error
    
    @classmethod
    def get_row_as_dict(cls, table_name: str, conditions: dict = None) -> dict | None:
        """
        Fetch a single row from the table as a dictionary with column names.
        
        Example Usage:
        conditions = {'id': 1}
        DB.get_row_as_dict('users', conditions)
        """
        with cls.get_connection() as cursor:
            try:
                query = f'SELECT * FROM {table_name}'
                if conditions:
                    cond_str = ' AND '.join(f'{col} = %s' for col in conditions.keys())
                    query += f' WHERE {cond_str}'
                    cursor.execute(query, tuple(conditions.values()))
                else:
                    cursor.execute(query)

                result = cursor.fetchone()
                if result:
                    # Fetch column names
                    columns = [col[0] for col in cursor.description]
                    # Map column names to result values
                    return dict(zip(columns, result))
                return None
            except Error as error:
                logger.error(f'DB.get_row_as_dict.error: {error}')
                return None
    
    @classmethod
    def add_column(cls, table_name: str, column_name: str, column_datatype: str) -> None:
        """
        Add a new column to an existing table.

        Example Usage:
        DB.add_column('test', 'email', 'VARCHAR(255)')
        """
        with cls.get_connection() as cursor:
            try:
                query = f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_datatype}'
                cursor.execute(query)
                cls.conn.commit()
                logger.info(f'Column \'{column_name}\' added to \'{table_name}\' table.')
            except Error as error:
                raise Exception(f'DB.add_column.error: {error}') from error

# Example usage
if __name__ == '__main__':
    # Only mysql admin user acc has grant access for CREATE.
    Env = 'DEV'

    DB.setCredentials(
        symmetric_key=os.getenv(f'{Env}_DB_SYMMETRIC_KEY').encode(),
        host=os.getenv(f'{Env}_DB_HOST').encode(),
        port=os.getenv(f'{Env}_DB_PORT').encode(),
        user=os.getenv(f'{Env}_DB_USER').encode(),
        password=os.getenv(f'{Env}_DB_PASSWORD').encode(),
        database=os.getenv(f'{Env}_DB_DATABASE').encode()
    )

    # Test database operations
    try:
        # Create a test table
        DB.createTable('test', {'id': 'INT PRIMARY KEY AUTO_INCREMENT', 'name': 'TEXT', 'age': 'INT', 'created_at': 'DATETIME'})
        # Add a test row
        DB.addRow('test', {'name': 'Bob', 'age': 30, 'created_at': datetime.now()})
        # Fetch rows
        print(DB.getRows('test'))
    except Exception as e:
        print(f'Error: {e}')