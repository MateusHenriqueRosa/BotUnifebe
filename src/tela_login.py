from tkinter import Tk, Frame, Label, Entry, Button, messagebox


class TelaLogin:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Login - Automação Unifebe")

        largura_janela = 400
        altura_janela = 300
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        self.root.configure(bg="#f0f0f0")

        self.login_frame = Frame(self.root, bg="#f0f0f0", padx=40, pady=20)
        self.login_frame.pack(expand=True)

    def criar_widgets(self, sucesso_login):
        self.sucesso_login = sucesso_login

        label_titulo = Label(
            self.login_frame,
            text="Acessar o Sistema",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        )
        label_titulo.pack(pady=(0, 20))

        label_usuario = Label(
            self.login_frame, text="Usuário", font=("Arial", 12), bg="#f0f0f0"
        )
        label_usuario.pack(anchor="w")
        self.entry_usuario = Entry(self.login_frame, font=("Arial", 12), width=30)
        self.entry_usuario.pack(pady=(5, 10))

        label_senha = Label(
            self.login_frame, text="Senha", font=("Arial", 12), bg="#f0f0f0"
        )
        label_senha.pack(anchor="w")
        self.entry_senha = Entry(
            self.login_frame, show="*", font=("Arial", 12), width=30
        )
        self.entry_senha.pack(pady=(5, 20))

        btn_entrar = Button(
            self.login_frame,
            text="Entrar",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            cursor="hand2",
            width=15,
            command=self.__verificar_login,
        )
        btn_entrar.pack()

    def __verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        # substituir essa parte para uma base de dados, provavelmente sqlite
        if usuario == "1" and senha == "1":
            self.__destruir_tela_login()
            self.sucesso_login()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")

    def __destruir_tela_login(self):
        self.login_frame.destroy()
