from src.inicializador import InicializaObjetos
from src.atividades_pendentes import AtividadesPendentes


class BotUnifebe:
    def __init__(self):
        self.inicializador = InicializaObjetos()

        bot = AtividadesPendentes(self.inicializador.web_bot)
        bot.main()


if __name__ == "__main__":
    BotUnifebe()
