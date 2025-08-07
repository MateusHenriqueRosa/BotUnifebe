import os

import pdfplumber
from openpyxl import Workbook

from src.utils import Utils
from src.baixa_boletim import BaixaBoletim


class QuantidadeDeFaltas():
    def __init__(self, utils: Utils, baixa_boletim: BaixaBoletim):
        self.utils = utils
        self.baixa_boletim = baixa_boletim
        

    def main(self):
        if self.baixa_boletim.main():
            boletim = self.__ler_pdf_boletim()
            self.__extrair_tabelas_pdf(os.path.join(self.utils.caminho_projeto, boletim))
        else:
            print("Deu ruim ao baixar o boletim.")


    def __ler_pdf_boletim(self):
        arquivos = self.utils.busca_arquivos_projeto(".pdf")
        if not arquivos:
            print("Nenhum arquivo PDF encontrado.")
            return # criar um raise de erro aqui
        return arquivos[0]


    def __extrair_tabelas_pdf(self, caminho_pdf):
        faltas_coletadas = []
        with pdfplumber.open(caminho_pdf) as pdf:
            page = pdf.pages[0]
            tabela = page.extract_tables()
            linhas = tabela[0]
            for texto in linhas[1:]:

                materia = texto[0]
                faltas_a1 = texto[2]
                faltas_a2 = texto[3]
                faltas_a3 = texto[4]
                faltas_total = str(int(faltas_a1)+int(faltas_a2)+int(faltas_a3))

                faltas_coletadas.append({
                "Matéria": materia,
                "Faltas A1": faltas_a1,
                "Faltas A2": faltas_a2,
                "Faltas A3": faltas_a3,
                "Faltas Totais": faltas_total
                })
        self.__salvar_faltas_em_excel(faltas_coletadas)
        return
    

    def __salvar_faltas_em_excel(self, faltas_coletadas):
        workbook = Workbook()
        planilha = workbook.active
        planilha.title = "QtdFaltas"

        planilha.append(["Matéria", "Faltas A1", "Faltas A2", "Faltas A3", "Faltas Totais"])

        for linha in faltas_coletadas:
            planilha.append([
                linha["Matéria"],
                linha["Faltas A1"],
                linha["Faltas A2"],
                linha["Faltas A3"],
                linha["Faltas Totais"]
            ])

        workbook.save("quantidade_faltas.xlsx")
