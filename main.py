from analysis.base_analysis import SimpleAnalysis

def main():
    # Defina os parâmetros iniciais
    service_name = "db_cobranca"

    # Instancie a classe SimpleAnalysis
    analysis_cobranca = SimpleAnalysis(service_name)

    # Defina novos parâmetros para outra query
    new_initial_date = "2024-06-01"
    new_final_date = "2024-06-10"
    new_agents = ["1", "2"]

    # Chame o método de análise novamente com novos parâmetros
    result2 = analysis_cobranca.analyze(new_initial_date, new_final_date, new_agents)
    print("Making .XLSX File:")
    file_path = 'meu_arquivo.xlsx'

    # Converter o DataFrame para Excel
    result2.to_excel(file_path, index=False)

if __name__ == "__main__":
    main()
