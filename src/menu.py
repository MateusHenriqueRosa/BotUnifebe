import os
from tkinter import Tk
from tkinter import Button, Frame, Label, messagebox, filedialog, ttk

import pandas as pd

from .utils import Utils
from .atividades_pendentes import AtividadesPendentes



class MenuPrincipal:
    def __init__(self, tkinter: Tk, atividades_pendentes: AtividadesPendentes, utils: Utils):
        self.atividades_pendentes = atividades_pendentes
        self.utils = utils
        self.root = tkinter
        self.root.title("Sistema de Automação")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')


    def __limpa_elementos(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        
    def carrega_menu_principal(self):
        self.__limpa_elementos()
        
        main_frame = Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = Label(
            main_frame, 
            text="Automação Unifebe", 
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=(0, 40))
        
        # Subtítulo
        subtitle_label = Label(
            main_frame, 
            text="Escolha uma automação para executar:", 
            font=('Arial', 12),
            bg='#f0f0f0',
            fg='#666666'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame para os botões
        buttons_frame = Frame(main_frame, bg='#f0f0f0')
        buttons_frame.pack(expand=True)
        
        # Botão 1 - Automação Atividades Pendentes
        btn1 = Button(
            buttons_frame,
            text="📓 Atividades Pendentes",
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=25,
            height=2,
            cursor='hand2',
            command=lambda: self.__executar_automacao("Atividades Pendentes")
        )
        btn1.pack(pady=10)
        
        # Botão 2 - Automação Notas Faltantes
        btn2 = Button(
            buttons_frame,
            text="📅 Notas Faltantes",
            font=('Arial', 14, 'bold'),
            bg='#2196F3',
            fg='white',
            width=25,
            height=2,
            cursor='hand2',
            command=lambda: self.__executar_automacao("Notas Faltantes")
        )
        btn2.pack(pady=10)
        
        # Botão 3 - Automação Quantidade de Faltas
        btn3 = Button(
            buttons_frame,
            text="🏖️ Quantidade de Faltas",
            font=('Arial', 14, 'bold'),
            bg='#FF9800',
            fg='white',
            width=25,
            height=2,
            cursor='hand2',
            command=lambda: self.__executar_automacao("Quantidade de Faltas")
        )
        btn3.pack(pady=10)

        self.root.mainloop()


    def __executar_automacao(self, tipo):
        self.__mostra_carregamento(f"Executando automação de {tipo}...")
        
        self.root.after(2000, lambda: self.__coleta_dados(tipo))

    
    def __mostra_carregamento(self, message):
        self.__limpa_elementos()
        
        main_frame = Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both')
        
        # Mensagem de loading
        loading_label = Label(
            main_frame,
            text=message,
            font=('Arial', 16),
            bg='#f0f0f0',
            fg='#333333'
        )
        loading_label.pack(expand=True)
        
        # Barra de progresso
        progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        progress.pack(pady=20)
        progress.start()

    
    def __coleta_dados(self, tipo):
        
        if tipo == "Atividades Pendentes":
            self.atividades_pendentes.main()
            excel = self.utils.busca_arquivos_projeto()
            self.dataframe_atividade = pd.read_excel(excel[0])
            for arquivo in self.utils.busca_arquivos_projeto():
                os.remove(os.path.join(self.utils.caminho_projeto, arquivo))
        
        elif tipo == "Notas Faltantes":
            ...
        
        elif tipo == "Quantidade de Faltas":
            ...
        
        messagebox.showinfo(
            "Automação Concluída", 
            f"Automação de {tipo} executada com sucesso!\n"
        )
        
        self.__mostrar_consulta()

    
    def __mostrar_consulta(self):
        """Exibe a tela de consulta com grid e botões de exportação"""
        self.__limpa_elementos()
        
        # Frame principal
        main_frame = Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Cabeçalho
        header_frame = Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Título
        title_label = Label(
            header_frame,
            text="Dados Coletados",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(side='left')
        
        # Botão voltar
        btn_voltar = Button(
            header_frame,
            text="← Voltar ao Menu",
            font=('Arial', 10),
            bg='#666666',
            fg='white',
            cursor='hand2',
            command=self.carrega_menu_principal
        )
        btn_voltar.pack(side='right')
        
        # Frame para botões de exportação
        export_frame = Frame(main_frame, bg='#f0f0f0')
        export_frame.pack(fill='x', pady=(0, 10))
        
        # Informações
        info_label = Label(
            export_frame,
            text="Ola Mundo",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        info_label.pack(side='left')
        
        # Botões de exportação
        btn_xlsx = Button(
            export_frame,
            text="📊 Baixar XLSX",
            font=('Arial', 10, 'bold'),
            bg='#1B5E20',
            fg='white',
            cursor='hand2',
            command=self.exportar_xlsx
        )
        btn_xlsx.pack(side='right', padx=(5, 0))
        
        btn_csv = Button(
            export_frame,
            text="📄 Baixar CSV",
            font=('Arial', 10, 'bold'),
            bg='#0D47A1',
            fg='white',
            cursor='hand2',
            command=self.exportar_csv
        )
        btn_csv.pack(side='right', padx=(5, 0))
        
        # Frame para o grid
        grid_frame = Frame(main_frame)
        grid_frame.pack(fill='both', expand=True)

        if hasattr(self, 'dataframe_atividade') and not self.dataframe_atividade.empty:

            colunas = self.dataframe_atividade.columns.tolist()

            # Criar treeview
            self.tree = ttk.Treeview(grid_frame, columns=colunas, show='headings', height=15)
            
            # Configurar cabeçalhos
            for col in colunas:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, minwidth=80)
            
            # Adicionar dados
            for index, row in self.dataframe_atividade.iterrows():
                valores = [str(row[col]) if not pd.isna(row[col]) else '' for col in colunas]
                self.tree.insert('', 'end', values=valores)
            
            # Scrollbars
            scrollbar_y = ttk.Scrollbar(grid_frame, orient='vertical', command=self.tree.yview)
            scrollbar_x = ttk.Scrollbar(grid_frame, orient='horizontal', command=self.tree.xview)
            self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            
            # Pack components (scrollbars primeiro para ficarem colados)
            scrollbar_y.pack(side='right', fill='y')
            scrollbar_x.pack(side='bottom', fill='x')
            self.tree.pack(side='left', fill='both', expand=True)
            
        else:
            # Mensagem quando não há dados
            no_data_label = Label(
                grid_frame,
                text="Nenhum dado coletado ainda.\nExecute uma automação para ver os resultados aqui.",
                font=('Arial', 12),
                bg='#f0f0f0',
                fg='#666666',
                justify='center'
            )
            no_data_label.pack(expand=True)
    

    def exportar_xlsx(self):
        if not hasattr(self, 'dataframe_atividade') and self.dataframe_atividade.empty:
            messagebox.showwarning("Aviso", "Não há dados para exportar!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Salvar como Excel"
            )
            
            if filename:
                self.dataframe_atividade.to_excel(filename, index=False)
                messagebox.showinfo("Sucesso", f"Arquivo salvo como:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar XLSX:\n{str(e)}")
    

    def exportar_csv(self):
        if not hasattr(self, 'dataframe_atividade') and self.dataframe_atividade.empty:
            messagebox.showwarning("Aviso", "Não há dados para exportar!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Salvar como CSV"
            )
            
            if filename:
                self.dataframe_atividade.to_csv(filename, index=False, encoding='utf-8-sig')
                messagebox.showinfo("Sucesso", f"Arquivo salvo como:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar CSV:\n{str(e)}")