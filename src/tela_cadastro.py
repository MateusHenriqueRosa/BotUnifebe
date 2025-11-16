# src/tela_cadastro.py
from tkinter import Toplevel, Frame, Label, Entry, Button, messagebox
from src.usuario import criar_usuario, buscar_usuario_por_username
import re

class TelaCadastro:
    def __init__(self, root):
        self.root = Toplevel(root)
        self.root.title("Cadastro - Automação Unifebe")

        largura_janela = 420
        altura_janela = 360
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        self.root.configure(bg="#f0f0f0")

        self.frame = Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        self.frame.pack(expand=True, fill="both")

        Label(self.frame, text="Cadastro de Usuário", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=(0,10))

        Label(self.frame, text="Nome de usuário", bg="#f0f0f0").pack(anchor="w")
        self.entry_username = Entry(self.frame, width=35)
        self.entry_username.pack(pady=(0,8))

        Label(self.frame, text="E-mail (opcional)", bg="#f0f0f0").pack(anchor="w")
        self.entry_email = Entry(self.frame, width=35)
        self.entry_email.pack(pady=(0,8))

        Label(self.frame, text="Senha", bg="#f0f0f0").pack(anchor="w")
        self.entry_password = Entry(self.frame, show="*", width=35)
        self.entry_password.pack(pady=(0,8))

        Label(self.frame, text="Confirmar senha", bg="#f0f0f0").pack(anchor="w")
        self.entry_password_conf = Entry(self.frame, show="*", width=35)
        self.entry_password_conf.pack(pady=(0,12))

        btn_cadastrar = Button(
            self.frame, text="Cadastrar", width=20, bg="#4CAF50", fg="white", cursor="hand2",
            command=self.__cadastrar
        )
        btn_cadastrar.pack(pady=(8,0))

    def __validar_email(self, email: str) -> bool:
        if not email:
            return True
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return re.match(pattern, email) is not None

    def __cadastrar(self):
        username = self.entry_username.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get()
        password_conf = self.entry_password_conf.get()

        if not username or not password:
            messagebox.showwarning("Aviso", "Usuário e senha são obrigatórios.")
            return

        if password != password_conf:
            messagebox.showwarning("Aviso", "As senhas não conferem.")
            return

        if not self.__validar_email(email):
            messagebox.showwarning("Aviso", "E-mail inválido.")
            return

        existing = buscar_usuario_por_username(username)
        if existing:
            messagebox.showerror("Erro", "Nome de usuário já existe. Escolha outro.")
            return

        try:
            user = criar_usuario(username, email if email else None, password)
            messagebox.showinfo("Sucesso", f"Usuário '{user['username']}' cadastrado com sucesso.")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar usuário:\n{e}")
