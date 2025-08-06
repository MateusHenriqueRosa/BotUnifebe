import os

from botcity.web import WebBot, By


class BaixaBoletim:
    def __init__(self, web_bot: WebBot):
        self.web_bot = web_bot

    def main(self):
        self.web_bot.start_browser()
        self.web_bot.maximize_window()
        self.web_bot.browse("https://mentorweb.unifebe.edu.br/unifebeSecurityG5/")
        self.web_bot.wait(8000)

        login = self.web_bot.find_element(selector='//*[@id="j_username"]', by=By.XPATH)
        login.send_keys("")
        senha = self.web_bot.find_element(selector='//*[@id="senha"]', by=By.XPATH)
        senha.send_keys("")

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

        iframe_boletim = self.web_bot.find_element(
            selector='//*[@id="relatorio"]', by=By.XPATH
        )
        iframe_2 = self.web_bot.find_element(
            selector='//*[@id="iframeIntegracao"]', by=By.XPATH
        )

        self.web_bot.enter_iframe(iframe_2)
        self.web_bot.enter_iframe(iframe_boletim)

        self.web_bot.execute_javascript("abreJanelaPoupop()")
        
        self.web_bot.leave_iframe()
        self.web_bot.leave_iframe()

        self.web_bot.wait(5000)
        self.web_bot.stop_browser()

        return True
