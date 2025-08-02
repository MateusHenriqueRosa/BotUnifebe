from openpyxl import Workbook
from botcity.web import WebBot, By

class AtividadesPendentes:
    def __init__(self, web_bot: WebBot):
        self.web_bot = web_bot
        self.web_bot.start_browser()


    def main(self):
        self.web_bot.maximize_window()
        self.web_bot.browse("https://virtual.unifebe.edu.br/avea/login/index.php")
        self.web_bot.wait(8000)

        login = self.web_bot.find_element(selector='//*[@id="username"]', by=By.XPATH)
        login.send_keys("")
        senha = self.web_bot.find_element(selector='//*[@id="password"]', by=By.XPATH)
        senha.send_keys("")

        self.web_bot.wait(1000)

        btn_acessar = self.web_bot.find_element(
            selector='//*[@id="loginbtn"]', by=By.XPATH
        )
        btn_acessar.click()

        self.web_bot.wait(6000)

        ver_mais = self.web_bot.find_element(
            selector='//*[@id="snap-pm-updates"]/section[1]/snap-feed/a/small',
            by=By.XPATH,
        )
        ver_mais.click()

        self.web_bot.wait(4000)

        self.web_bot.scroll_down(1)
        self.web_bot.wait(2000)

        atividades = self.web_bot.find_elements(
            selector='//*[@id="snap-personal-menu-feed-deadlines"]/div[contains(@class, "feeditem")]',
            by=By.XPATH
        )

        atividades_coletadas = []

        for i, atividade in enumerate(atividades):
            titulo = atividade.find_element(By.TAG_NAME, 'h3').text
            data_entrega = atividade.find_element(By.TAG_NAME, 'time').text
            status = atividade.find_element(By.CLASS_NAME, 'snap-completion-meta').text
            link = atividade.find_element(By.TAG_NAME, 'a').get_attribute('href')

            atividades_coletadas.append({
            "Título": titulo.split(" está marcado(a) para esta data")[0],
            "Data de Entrega": data_entrega,
            "Status": status,
            "Link": link
            })

        self.__salvar_atividades_em_excel(atividades_coletadas)
        self.web_bot.wait(5000)
        self.web_bot.stop_browser()

    def __salvar_atividades_em_excel(self, atividades_coletadas):
        workbook = Workbook()
        planilha = workbook.active
        planilha.title = "Atividades"

        planilha.append(["Título", "Data de Entrega", "Status", "Link"])

        for atividade in atividades_coletadas:
            planilha.append([
                atividade["Título"],
                atividade["Data de Entrega"],
                atividade["Status"],
                atividade["Link"]
            ])

        workbook.save("atividades.xlsx")