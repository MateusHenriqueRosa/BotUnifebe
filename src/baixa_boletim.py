from botcity.web import WebBot, By
from botcity.core import DesktopBot

from src.utils import Utils


class BaixaBoletim:
    def __init__(self, web_bot: WebBot, utils: Utils, desktop_bot: DesktopBot):
        self.web_bot = web_bot
        self.utils = utils
        self.desktop_bot = desktop_bot

    def baixa_boletim(self):
        self.web_bot.start_browser()
        self.web_bot.maximize_window()
        self.web_bot.browse("https://mentorweb.unifebe.edu.br/unifebeSecurityG5/")
        self.web_bot.wait(8000)

        login = self.web_bot.find_element(selector='//*[@id="j_username"]', by=By.XPATH)
        login.send_keys(self.utils.USUARIO_UNIFEBE)
        senha = self.web_bot.find_element(selector='//*[@id="senha"]', by=By.XPATH)
        senha.send_keys(self.utils.SENHA_UNIFEBE)

        self.web_bot.wait(1000)

        btn_acessar = self.web_bot.find_element(
            selector='//*[@id="btnLogin"]', by=By.XPATH
        )
        btn_acessar.click()

        self.web_bot.wait(6000)

        for _ in range(5):
            self.web_bot.execute_javascript("fechouJanelaSemRedirecionar()")
            self.web_bot.wait(2000)

        btn_menu = self.web_bot.find_element(
            selector='//*[@id="toggleMenu"]', by=By.XPATH
        )
        btn_menu.click()
        self.web_bot.wait(1000)

        dropdown_aluno = self.web_bot.find_element(
            selector='//*[@id="formMenu:menu_0"]/a/i', by=By.XPATH
        )
        dropdown_aluno.click()
        self.web_bot.wait(1000)

        btn_boletim = self.web_bot.find_element(
            selector='//*[@id="formMenu:menu_0_9"]/a', by=By.XPATH
        )
        self.web_bot.execute_javascript(
            f"window.location.href = '{btn_boletim.get_attribute('href')}'",
        )
        self.web_bot.wait(2000)

        self.web_bot.hold_shift()
        self.web_bot.tab()
        self.web_bot.tab()
        self.web_bot.release_shift()
        self.web_bot.enter()

        self.web_bot.wait(2000)
        if not self.utils.busca_arquivos_projeto(".pdf"):
            self.desktop_bot.type_keys(["ctrl", "s"])

        self.web_bot.wait(5000)
        self.desktop_bot.type_keys(["ctrl", "w"])
        self.web_bot.stop_browser()

        return True
