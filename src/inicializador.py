from botcity.web import WebBot, Browser


class InicializaObjetos:
    def __init__(self):
        self.web_bot = self.__inicializa_web_bot()


    def __inicializa_web_bot(self):
        self.web_bot = WebBot()
        self.web_bot.headless = False
        self.web_bot.browser = Browser.EDGE
        self.web_bot.driver_path = r"drivers\msedgedriver.exe"
        self.web_bot.start_browser()
        return self.web_bot