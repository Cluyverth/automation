from datetime import datetime
from typing import List
import pandas as pd
from data.db import DatabaseManager

class SimpleAnalysis:
    def __init__(self, service_name: str):
        self.db_manager = DatabaseManager(service_name)

    def analyze(self, initial_date: str, final_date: str, agents: List[str]) -> pd.DataFrame:
        # Validar e formatar as datas
        try:
            initial_date = datetime.strptime(initial_date, "%Y-%m-%d").date()
            final_date = datetime.strptime(final_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Datas devem estar no formato AAAA-MM-DD")

        # Formatar a lista de agentes cobradores para a query
        agents_str = ', '.join(f"'{agent}'" for agent in agents)

        # Construir a query
        query = f"""
            SELECT
                *
            FROM Parcela
                AND Agente IN ({agents_str})
                AND DataVencimento BETWEEN '{initial_date}' AND '{final_date}'
        """

        # Executar a query e retornar os resultados como DataFrame
        df = self.db_manager.execute_query_in_chunks(query)
        
        return df