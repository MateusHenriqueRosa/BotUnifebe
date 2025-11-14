import os

import pdfplumber
from openpyxl import Workbook
from botcity.web import WebBot
from botcity.core import DesktopBot

from src.utils import Utils
from src.baixa_boletim import BaixaBoletim


class NotasBoletim(BaixaBoletim):
    def __init__(self, web_bot: WebBot, utils: Utils, desktop_bot: DesktopBot):
        super().__init__(web_bot, utils, desktop_bot)

    def main(self):
        if self.baixa_boletim():
            boletim = self.__ler_pdf_boletim()
            self.extrair_tabelas_pdf(os.path.join(self.utils.caminho_projeto, boletim))
        else:
            print("Deu ruim ao baixar o boletim.")

    def __ler_pdf_boletim(self):
        arquivos = self.utils.busca_arquivos_projeto(".pdf")
        if not arquivos:
            print("Nenhum arquivo PDF encontrado.")
            return  # criar um raise de erro aqui
        return arquivos

    def extrair_tabelas_pdf(self, caminho_pdf):
        notas_coletadas = []
        with pdfplumber.open(caminho_pdf) as pdf:
            page = pdf.pages[0]
            tabela = page.extract_tables()
            linhas = tabela[0]
            for texto in linhas[1:]:

                notas_a1 = "0,0"
                notas_a2 = "0,0"
                notas_a3 = "0,0"

                materia = texto[0]
                if texto[2].__contains__(" "):
                    notas_a1 = texto[2].split(" ")[0]

                if texto[3].__contains__(" "):
                    notas_a2 = texto[3].split(" ")[0]

                if texto[4].__contains__(" "):
                    notas_a3 = texto[4].split(" ")[0]

                nota_total = str(
                    float(notas_a1.replace(",", "."))
                    + float(notas_a2.replace(",", "."))
                    + float(notas_a3.replace(",", "."))
                )

                notas_coletadas.append(
                    {
                        "Matéria": materia,
                        "Nota A1": notas_a1,
                        "Nota A2": notas_a2,
                        "Nota A3": notas_a3,
                        "Nota Total": nota_total,
                        "Nota Faltante": (
                            str(round(18.0 - float(nota_total), 2))
                            if float(nota_total) < 18.0
                            else "--"
                        ),
                        "Aprovação": (
                            "Aprovado" if float(nota_total) >= 18.0 else "Reprovado"
                        ),
                    }
                )
        self.__salvar_notas_em_excel(notas_coletadas)
        return

    def __salvar_notas_em_excel(self, notas_coletadas):
        workbook = Workbook()
        planilha = workbook.active
        planilha.title = "NotasBoletim"

        planilha.append(
            [
                "Matéria",
                "Notas A1",
                "Notas A2",
                "Notas A3",
                "Nota Total",
                "Nota Faltante",
                "Aprovação",
            ]
        )

        for linha in notas_coletadas:
            planilha.append(
                [
                    linha["Matéria"],
                    linha["Nota A1"],
                    linha["Nota A2"],
                    linha["Nota A3"],
                    linha["Nota Total"],
                    linha["Nota Faltante"],
                    linha["Aprovação"],
                ]
            )

        workbook.save("notas_boletim.xlsx")
