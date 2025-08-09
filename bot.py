from src.menu import MenuPrincipal
from src.tela_login import TelaLogin
from src.inicializador import InicializaObjetos


class BotUnifebe:
    def __init__(self):
        self.inicializador = InicializaObjetos()

        self.tela_login = TelaLogin(
            self.inicializador.tkinter,
            self.iniciar_menu_principal
        )
        self.inicializador.tkinter.mainloop()

    def iniciar_menu_principal(self):

        menu_principal = MenuPrincipal(
            self.inicializador.tkinter,
            self.inicializador.atividades_pendentes,
            self.inicializador.quantidade_faltas,
            self.inicializador.utils,
        )

        menu_principal.carrega_menu_principal()


if __name__ == "__main__":
    BotUnifebe()
