import os


class Utils:
    def __init__(self):
        self.caminho_projeto = os.path.abspath('.')


    def busca_arquivos_projeto(self, extensao: str):
        arquivos = [planilha for planilha in os.listdir(self.caminho_projeto) if planilha.endswith(extensao)]
        return arquivos
    
    
    def limpa_caracteres_especiais(self, texto: str):
        caracteres_especiais = ["\n", "\t", "\r"]
        for caracter in caracteres_especiais:
            texto = texto.replace(caracter, "")
        return texto
