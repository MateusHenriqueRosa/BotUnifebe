import logging
import sys

from src.menu import MenuPrincipal
from src.tela_login import TelaLogin
from src.inicializador import InicializaObjetos


class BotUnifebe:
    def __init__(self):
        self.inicializador = InicializaObjetos()

        logging.info("Iniciando BotUnifebe")

        try:
            tela_login = TelaLogin(self.inicializador.tkinter)
            tela_login.criar_widgets(self.abrir_menu_principal)
            self.inicializador.tkinter.mainloop()

            logging.info("BotUnifebe finalizado")
            sys.exit(0)

        except Exception as erro:
            logging.error(f"Erro crítico na execução. ERRO: {erro}")
            sys.exit(0)

    def abrir_menu_principal(self):
        menu_principal = MenuPrincipal(
            self.inicializador.tkinter,
            self.inicializador.atividades_pendentes,
            self.inicializador.quantidade_faltas,
            self.inicializador.utils,
        )

        menu_principal.carrega_menu_principal()


if __name__ == "__main__":
    BotUnifebe()
