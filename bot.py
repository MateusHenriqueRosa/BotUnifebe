from src.inicializador import InicializaObjetos
from src.menu import MenuPrincipal


class BotUnifebe:
    def __init__(self):
        self.inicializador = InicializaObjetos()

        menu_principal = MenuPrincipal(
            self.inicializador.tkinter,
            self.inicializador.atividades_pendentes,
            self.inicializador.utils,
        )
        
        menu_principal.carrega_menu_principal()


if __name__ == "__main__":
    BotUnifebe()
