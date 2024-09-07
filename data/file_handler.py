import pandas as pd
import json

class FileHandler:
    @staticmethod
    def read_csv(file_path: str) -> pd.DataFrame:
        """
        Lê um arquivo CSV e retorna um DataFrame pandas.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise IOError(f"Erro ao ler o arquivo CSV {file_path}: {e}")
            
    @staticmethod
    def write_csv(data: pd.DataFrame, file_path: str) -> None:
        """
        Escreve um DataFrame pandas em um arquivo CSV.
        """
        try:
            data.to_csv(file_path, index=False)
        except Exception as e:
            raise IOError(f"Erro ao escrever no arquivo CSV {file_path}: {e}")
    
    @staticmethod
    def read_excel(file_path: str, sheet_name: str = None) -> pd.DataFrame:
        """
        Lê um arquivo Excel e retorna um DataFrame pandas.
        Se sheet_name for especificado, lê a planilha correspondente.
        """
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        except Exception as e:
            raise IOError(f"Erro ao ler o arquivo Excel {file_path}: {e}")
    
    @staticmethod
    def write_excel(data: pd.DataFrame, file_path: str, sheet_name: str = 'Sheet1') -> None:
        """
        Escreve um DataFrame pandas em um arquivo Excel, com uma planilha especificada.
        """
        try:
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                data.to_excel(writer, sheet_name=sheet_name, index=False)
        except Exception as e:
            raise IOError(f"Erro ao escrever no arquivo Excel {file_path}: {e}")
    
    @staticmethod
    def read_json(file_path: str) -> pd.DataFrame:
        """
        Lê um arquivo JSON e retorna um DataFrame pandas.
        """
        try:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
            return pd.json_normalize(json_data)
        except Exception as e:
            raise IOError(f"Erro ao ler o arquivo JSON {file_path}: {e}")
    
    @staticmethod
    def write_json(data: pd.DataFrame, file_path: str, orient: str = 'records') -> None:
        """
        Escreve um DataFrame pandas em um arquivo JSON.
        O parâmetro `orient` pode ser ajustado para alterar o formato do JSON.
        """
        try:
            with open(file_path, 'w') as file:
                json_data = data.to_json(orient=orient)
                file.write(json_data)
        except Exception as e:
            raise IOError(f"Erro ao escrever no arquivo JSON {file_path}: {e}")

    @staticmethod
    def read_sql_file(file_path: str) -> str:
        """
        Lê um arquivo .sql e retorna o conteúdo como string.
        """
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            raise IOError(f"Erro ao ler o arquivo SQL {file_path}: {e}")
