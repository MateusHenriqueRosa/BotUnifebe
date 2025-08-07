import os

import pdfplumber
import pandas as pd
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
            tabelas_extraidas = self.__extrair_tabelas_pdf(os.path.join(self.utils.caminho_projeto, boletim))
            notas_coletadas = self.__extrair_notas(tabelas_extraidas)
            faltas_coletadas = self.__extrair_faltas(tabelas_extraidas)
            print(f"Notas coletadas: {notas_coletadas}")
            print(f"Faltas coletadas: {faltas_coletadas}")
        else:
            print("Deu ruim ao baixar o boletim.")


    def __ler_pdf_boletim(self):
        arquivos = self.utils.busca_arquivos_projeto(".pdf")
        if not arquivos:
            print("Nenhum arquivo PDF encontrado.")
            return # criar um raise de erro aqui
        return arquivos[0]


    def __extrair_tabelas_pdf(self, caminho_pdf):
        with pdfplumber.open(caminho_pdf) as pdf:
            tabelas_extraidas = []
            for page in pdf.pages:
                # Definindo as coordenadas (x0, top, x1, bottom) para a área da tabela
                # Ajuste conforme necessário com base na estrutura do PDF.
                bbox = (30, 180, 770, 360) # Ajustado para incluir a coluna 'Disciplina' e o cabeçalho
                cropped_page = page.crop(bbox)
                settings = {
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                    "snap_tolerance": 3,
                    "join_tolerance": 3,
                    "edge_min_length": 3,
                    "min_words_horizontal": 1,
                    "min_words_vertical": 1,
                    "explicit_vertical_lines": [],
                    "explicit_horizontal_lines": [],
                    "intersection_tolerance": 3,
                    "text_tolerance": 3
                }
                tabelas = cropped_page.extract_tables(table_settings=settings)
                print(f"Tabelas extraídas da página {page.page_number}: {tabelas}")
                for tabela in tabelas:
                    tabelas_extraidas.append(tabela)
            return tabelas_extraidas
    
    def __extrair_notas(self, tabelas):
        notas = []
        for tabela in tabelas:
            if tabela:
                for linha in tabela:
                    # Supondo que as notas (MF) estejam no índice 5
                    if len(linha) > 8 and linha[0] and linha[8] is not None and linha[8].strip() != '': # Disciplina e MF
                        try:
                            disciplina = linha[0]
                            nota_final_str = linha[8].strip()
                            if nota_final_str:
                                nota_final = float(nota_final_str)
                                notas.append({"Disciplina": disciplina, "Nota Final": nota_final})
                            else:
                                print(f"Valor vazio para nota final na linha: {linha}")
                        except ValueError:
                            print(f"Erro ao converter nota final para float na linha: {linha}")
                            pass # Ignorar linhas que não contêm notas válidas
        return notas

    def __extrair_faltas(self, tabelas):
        faltas = []
        for tabela in tabelas:
            if tabela:
                for linha in tabela:
                    # Supondo que as faltas (T.F.) estejam no índice 6
                    if len(linha) > 6 and linha[0] and linha[6] is not None and linha[6].strip() != '':
                        try:
                            disciplina = linha[0]
                            total_faltas_str = linha[6].strip()
                            if total_faltas_str:
                                total_faltas = int(total_faltas_str)
                                faltas.append({"Disciplina": disciplina, "Total de Faltas": total_faltas})
                            else:
                                print(f"Valor vazio para total de faltas na linha: {linha}")
                        except ValueError:
                            print(f"Erro ao converter total de faltas para int na linha: {linha}")
                            pass # Ignorar linhas que não contêm faltas válidas
        return faltas

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