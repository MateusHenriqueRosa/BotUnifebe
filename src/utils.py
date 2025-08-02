import os


class Utils:
    def __init__(self):
        self.caminho_projeto = os.path.abspath('.')
        self.pasta_downloads = os.path.join(self.caminho_projeto, "downloads")


    def busca_arquivos_projeto(self):
        arquivos = [planilha for planilha in os.listdir(self.caminho_projeto) if planilha.endswith('.xlsx')]
        return arquivos