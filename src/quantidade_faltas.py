from openpyxl import Workbook
import pandas as pd

from src.utils import Utils
from src.baixa_boletim import BaixaBoletim


class QuantidadeDeFaltas():
    def __init__(self, utils: Utils, baixa_boletim: BaixaBoletim):
        self.utils = utils
        self.baixa_boletim = baixa_boletim
        

    def main(self):
        if self.baixa_boletim.main():
            boletim = self.__ler_pdf_boletim()
        else:
            print("Deu ruim ao baixar o boletim.")


    def __ler_pdf_boletim(self):
        arquivos = self.utils.busca_arquivos_projeto(".pdf")
        if not arquivos:
            print("Nenhum arquivo PDF encontrado.")
            return # criar um raise de erro aqui
        return arquivos[0]


    def __salvar_faltas_em_excel(self, faltas_coletadas):
        workbook = Workbook()
        planilha = workbook.active
        planilha.title = "Atividades"

        planilha.append(["Título", "Data de Entrega", "Status", "Link"])

        for atividade in faltas_coletadas:
            planilha.append([
                atividade["Título"],
                atividade["Data de Entrega"],
                atividade["Status"],
                atividade["Link"]
            ])

        workbook.save("atividades.xlsx")