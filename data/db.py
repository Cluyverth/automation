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
        
        return pd.DataFrame(data, columns=columns)
    
    def execute_sql_file(
        self,
        file_path: str,
        connection: Optional[Union[sqlite3.Connection, pyodbc.Connection]] = None
        ) -> pd.DataFrame:
        query = FileHandler.read_sql_file(file_path)
        return self.execute_query_in_chunks(query, connection=connection)
        
