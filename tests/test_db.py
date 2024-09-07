import unittest
import os
import pandas as pd
from data.db import DatabaseManager

class TestDataManager(unittest.TestCase):
    
    def setUp(self):
        self.service_name = 'db_test'
        self.db_manager = DatabaseManager(self.service_name, use_SQLite=True)
        self.connection = self.db_manager._create_connection()
        self.query = "SELECT * FROM test_table"
        self.chunk_size = 1000
        
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE test_table (
                col1 INTEGER,
                col2 TEXT
            )
        ''')
        cursor.executemany('''
            INSERT INTO test_table (col1, col2) VALUES (?, ?)
        ''', [
            (1, 'foo'),
            (2, 'bar'),
            (3, 'baz')
        ])
        self.connection.commit()


    def tearDown(self):
        if self.connection:
            self.connection.close()


    def test_execute_query_in_chunks(self):
        results = self.db_manager.execute_query_in_chunks(self.query, self.chunk_size, connection=self.connection)
        
        expected_df = pd.DataFrame([(1, 'foo'), (2, 'bar'), (3, 'baz')], columns=['col1', 'col2'])
        
        pd.testing.assert_frame_equal(results, expected_df)


    def test_execute_sql_file(self):    
        sql_content = self.query
        with open('test_query.sql', 'w') as f:
            f.write(sql_content)
        
        results = self.db_manager.execute_sql_file('test_query.sql', connection=self.connection)
    
        expected_df = pd.DataFrame([(1, 'foo'), (2, 'bar'), (3, 'baz')], columns=['col1', 'col2'])
        pd.testing.assert_frame_equal(results, expected_df)
        
        os.remove('test_query.sql')


if __name__ == '__main__':
    unittest.main()