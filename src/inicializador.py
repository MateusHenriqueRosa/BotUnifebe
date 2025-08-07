import tkinter as tk

from botcity.web import WebBot, Browser
from botcity.core import DesktopBot

from src.utils import Utils
from src.baixa_boletim import BaixaBoletim
from src.quantidade_faltas import QuantidadeDeFaltas
from src.atividades_pendentes import AtividadesPendentes


class InicializaObjetos:
    def __init__(self):
        self.web_bot = self.__inicializa_web_bot()
        self.tkinter = self.__inicializa_tkinter()
        self.utils = Utils()
        self.desktop_bot = DesktopBot()
        self.atividades_pendentes = AtividadesPendentes(self.web_bot, self.utils)
        self.baixa_boletim = BaixaBoletim(self.web_bot, self.utils, self.desktop_bot)
        self.quantidade_faltas = QuantidadeDeFaltas(self.utils, self.baixa_boletim)


    def __inicializa_web_bot(self):
        self.web_bot = WebBot()
        self.web_bot.headless = False
        self.web_bot.browser = Browser.EDGE
        self.web_bot.driver_path = r"drivers\msedgedriver.exe"
        return self.web_bot
    

    def __inicializa_tkinter(self):
        self.tkinter = tk.Tk()
        self.tkinter.title("Automatiza Unifebe")
        self.tkinter.geometry("800x600")
        self.tkinter.configure(bg='#f0f0f0')
        return self.tkinter