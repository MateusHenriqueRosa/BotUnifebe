import tkinter as tk
import logging

from botcity.web import WebBot, Browser
from botcity.core import DesktopBot

from src.atividades_pendentes import AtividadesPendentes
from src.quantidade_faltas import QuantidadeDeFaltas
from src.notas_boletim import NotasBoletim
from src.utils import Utils


class InicializaObjetos:
    def __init__(self):
        self.logger = self.__inialicaliza_logger()
        self.web_bot = self.__inicializa_web_bot()
        self.tkinter = tk.Tk()
        self.utils = Utils()
        self.desktop_bot = DesktopBot()
        self.atividades_pendentes = AtividadesPendentes(self.web_bot, self.utils)
        self.quantidade_faltas = QuantidadeDeFaltas(
            self.web_bot, self.utils, self.desktop_bot
        )
        self.notas_boletim = NotasBoletim(self.web_bot, self.utils, self.desktop_bot)

    def __inicializa_web_bot(self):
        self.web_bot = WebBot()
        self.web_bot.headless = False
        self.web_bot.browser = Browser.EDGE
        self.web_bot.driver_path = r"drivers\msedgedriver.exe"
        return self.web_bot

    def __inialicaliza_logger(self):
        logging.basicConfig(
            filename="log.txt",
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
