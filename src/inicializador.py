import tkinter as tk

from botcity.web import WebBot, Browser

from src.utils import Utils
from src.atividades_pendentes import AtividadesPendentes


class InicializaObjetos:
    def __init__(self):
        self.web_bot = self.__inicializa_web_bot()
        self.tkinter = self.__inicializa_tkinter()
        self.utils = Utils()
        self.atividades_pendentes = AtividadesPendentes(self.web_bot)


    def __inicializa_web_bot(self):
        self.web_bot = WebBot()
        self.web_bot.headless = False
        self.web_bot.browser = Browser.EDGE
        self.web_bot.driver_path = r"drivers\msedgedriver.exe"
        # self.web_bot.start_browser()
        return self.web_bot
    

    def __inicializa_tkinter(self):
        self.tkinter = tk.Tk()
        self.tkinter.title("Automatiza Unifebe")
        self.tkinter.geometry("800x600")
        self.tkinter.configure(bg='#f0f0f0')
        return self.tkinter