import pyodbc
import sqlite3
import pandas as pd
from config.settings import get_db_config, get_env_variable
from data.file_handler import FileHandler
from typing import Optional, Union

class DatabaseManager:
    
    def __init__(
        self, service_name: str,
        use_SQLite: bool = False
        ):
        
        self.use_SQLite = use_SQLite
        if use_SQLite:
            self.connection_string = ":memory:"
        else:
            db_config = get_db_config(service_name)
            self.connection_string = (
                f"Driver={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={db_config['server']};"
                f"DATABASE={db_config['database']};"
                f"Authentication=ActiveDirectoryInteractive;"
                f"UID={get_env_variable('DB_USER')}"
            )
    
    def _create_connection(self) -> Union[sqlite3.Connection, pyodbc.Connection]:
        
        if self.use_SQLite: 
            return sqlite3.connect(self.connection_string)
        else:
            return pyodbc.connect(self.connection_string)
        
    def execute_query_in_chunks(
        self, query: str,
        chunk_size: int = 1000,
        connection: Optional[Union[sqlite3.Connection, pyodbc.Connection]] = None
        ) -> pd.DataFrame:
        
        if not connection:
            connection = self._create_connection()
        
        cursor = connection.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        
        data = []
        while True:
            rows = cursor.fetchmany(chunk_size)
            if not rows:
                break
            data.extend(rows)
        
        if connection:
            connection.close()
        
        # Verificar se os dados estão no formato correto
        if data:
            num_data_columns = len(data[0])
        else:
            num_data_columns = 0
        
        num_columns = len(columns)
        
        if num_data_columns != num_columns:
            raise ValueError(f"Shape of passed values is ({len(data)}, {num_data_columns}), indices imply ({len(data)}, {num_columns})")
            
        # Converter as colunas e as linhas em um dicionário
        data_dict = {col: [] for col in columns}
        for row in data:
            for col, value in zip(columns, row):
                data_dict[col].append(value)
        
        # Find the lists max length
        max_length = max(len(column_values) for column_values in data_dict.values())
        
        # Fill NULL With None
        for column_name, column_values in data_dict.items():
            if len(column_values) < max_length:
                missing_length = max_length - len(column_values)
                data_dict[column_name] = column_values + [None] * missing_length
        
        try:
            df = pd.DataFrame(data_dict)
            print("DataFrame created:", df)
        except ValueError as e:
            print(f"Error creating DataFrame: {e}")
            print(f"Data shape: {len(data)}, {num_data_columns}")
            print(f"Columns: {columns}")
            raise
        
        return df
    
    def execute_sql_file(
        self,
        file_path: str,
        connection: Optional[Union[sqlite3.Connection, pyodbc.Connection]] = None
        ) -> pd.DataFrame:
        query = FileHandler.read_sql_file(file_path)
        return self.execute_query_in_chunks(query, connection=connection)
        
