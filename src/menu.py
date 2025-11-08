import os
from tkinter import Tk
from tkinter import Button, Frame, Label, messagebox, filedialog, ttk

import pandas as pd

from .utils import Utils
from .notas_boletim import NotasBoletim
from .quantidade_faltas import QuantidadeDeFaltas
from .atividades_pendentes import AtividadesPendentes


class MenuPrincipal:
    def __init__(self, tkinter: Tk, atividades_pendentes: AtividadesPendentes, quantidade_faltas: QuantidadeDeFaltas, notas_boletim: NotasBoletim, utils: Utils):
        self.quantidade_faltas = quantidade_faltas
        self.notas_boletim = notas_boletim
        self.atividades_pendentes = atividades_pendentes
        self.utils = utils
        self.root = tkinter
        
        self.root.title("Sistema de Automação")
        largura_janela = 800
        altura_janela = 600
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.root.geometry(f'{largura_janela}x{altura_janela}+{pos_x}+{pos_y}')

        # Variáveis para armazenar dados de cada automação
        self.dataframe_atividades_pendentes = None
        self.dataframe_notas_boletim = None
        self.dataframe_quantidade_faltas = None
        self.tipo_automacao_atual = None

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

    def __executar_automacao(self, tipo):
        self.tipo_automacao_atual = tipo
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
            excel = self.utils.busca_arquivos_projeto(".xlsx")
            if excel:
                self.dataframe_atividades_pendentes = pd.read_excel(excel)
                os.remove(os.path.join(self.utils.caminho_projeto, excel))

        elif tipo == "Notas Faltantes":
            pdf = self.utils.busca_arquivos_projeto(".pdf")
            if not pdf:
                self.notas_boletim.main()
            else:
                resposta = messagebox.askquestion(
                    "Boletim desatualizado",
                    "Deseja atualizar Boletim? (Caso sim roda a automação)"
                )
                if resposta == "yes":
                    if pdf:
                        os.remove(os.path.join(self.utils.caminho_projeto, pdf))
                    self.notas_boletim.main()
                else:
                    self.notas_boletim.extrair_tabelas_pdf(os.path.join(self.utils.caminho_projeto, pdf))

            excel = self.utils.busca_arquivos_projeto(".xlsx")
            if excel:
                self.dataframe_notas_boletim = pd.read_excel(excel)
                os.remove(os.path.join(self.utils.caminho_projeto, excel))

        elif tipo == "Quantidade de Faltas":
            pdf = self.utils.busca_arquivos_projeto(".pdf")
            if not pdf:
                self.quantidade_faltas.main()
            else:
                resposta = messagebox.askquestion(
                    "Boletim desatualizado",
                    "Deseja atualizar Boletim? (Caso sim roda a automação)"
                )
                if resposta == "yes":
                    if pdf:
                        os.remove(os.path.join(self.utils.caminho_projeto, pdf))
                    self.quantidade_faltas.main()
                else:
                    self.quantidade_faltas.extrair_tabelas_pdf(os.path.join(self.utils.caminho_projeto, pdf))

            excel = self.utils.busca_arquivos_projeto(".xlsx")
            if excel:
                self.dataframe_quantidade_faltas = pd.read_excel(excel)
                os.remove(os.path.join(self.utils.caminho_projeto, excel))

        self.__mostrar_consulta_especifica(tipo)

    def __mostrar_consulta_especifica(self, tipo):
        """Exibe a tela de consulta específica baseada no tipo de automação"""
        self.__limpa_elementos()

        # Frame principal
        main_frame = Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Cabeçalho
        header_frame = Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=(0, 10))

        # Título específico para cada tipo
        title_label = Label(
            header_frame,
            text=f"Consulta - {tipo}",
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

        # Obter o dataframe correto baseado no tipo
        dataframe_atual = self.__get_dataframe_por_tipo(tipo)

        # Informações específicas
        if dataframe_atual is not None and not dataframe_atual.empty:
            info_text = f"Total de registros: {len(dataframe_atual)} | Tipo: {tipo}"
        else:
            info_text = f"Nenhum dado encontrado para {tipo}"

        info_label = Label(
            export_frame,
            text=info_text,
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#666666'
        )
        info_label.pack(side='left')

        # Botões de exportação (só aparecem se há dados)
        if dataframe_atual is not None and not dataframe_atual.empty:
            btn_xlsx = Button(
                export_frame,
                text="📊 Baixar XLSX",
                font=('Arial', 10, 'bold'),
                bg='#1B5E20',
                fg='white',
                cursor='hand2',
                command=lambda: self.exportar_xlsx(tipo)
            )
            btn_xlsx.pack(side='right', padx=(5, 0))

            btn_csv = Button(
                export_frame,
                text="📄 Baixar CSV",
                font=('Arial', 10, 'bold'),
                bg='#0D47A1',
                fg='white',
                cursor='hand2',
                command=lambda: self.exportar_csv(tipo)
            )
            btn_csv.pack(side='right', padx=(5, 0))

        # Frame para o grid
        grid_frame = Frame(main_frame)
        grid_frame.pack(fill='both', expand=True)

        if dataframe_atual is not None and not dataframe_atual.empty:
            colunas = dataframe_atual.columns.tolist()

            # Criar treeview com altura maior
            self.tree = ttk.Treeview(
                grid_frame, columns=colunas, show='headings', height=15)

            # Configurar estilo para aumentar altura das linhas
            style = ttk.Style()
            style.configure("Treeview", rowheight=40)

            # Configurar cabeçalhos
            for col in colunas:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150, minwidth=100)

            # Adicionar dados (tratando quebras de linha)
            for index, row in dataframe_atual.iterrows():
                valores = []
                for col in colunas:
                    if not pd.isna(row[col]):
                        # Substituir \n por espaço para evitar problemas de visualização
                        valor = str(row[col]).replace(
                            '\n', ' ').replace('\r', ' ')
                    else:
                        valor = ''
                    valores.append(valor)
                self.tree.insert('', 'end', values=valores)

            # Scrollbars
            scrollbar_y = ttk.Scrollbar(
                grid_frame, orient='vertical', command=self.tree.yview)
            scrollbar_x = ttk.Scrollbar(
                grid_frame, orient='horizontal', command=self.tree.xview)
            self.tree.configure(yscrollcommand=scrollbar_y.set,
                                xscrollcommand=scrollbar_x.set)

            # Pack components
            scrollbar_y.pack(side='right', fill='y')
            scrollbar_x.pack(side='bottom', fill='x')
            self.tree.pack(side='left', fill='both', expand=True)

        else:
            # Mensagem quando não há dados
            no_data_label = Label(
                grid_frame,
                text=f"Nenhum dado coletado para {tipo}.\nExecute a automação novamente se necessário.",
                font=('Arial', 12),
                bg='#f0f0f0',
                fg='#666666',
                justify='center'
            )
            no_data_label.pack(expand=True)

        # Frame para botões de ação no final (SEMPRE APARECEM)
        action_frame = Frame(main_frame, bg='#f0f0f0')
        action_frame.pack(fill='x', pady=(10, 0))

        # Frame vazio à esquerda para empurrar botões para a direita
        spacer_frame = Frame(action_frame, bg='#f0f0f0')
        spacer_frame.pack(side='left', expand=True)

        # Botão Extrair Atividade
        btn_extrair = Button(
            action_frame,
            text="📤 Extrair Atividade",
            font=('Arial', 11, 'bold'),
            bg='#9C27B0',
            fg='white',
            cursor='hand2',
            padx=15,
            pady=8,
            command=lambda: self.__extrair_atividade(tipo)
        )
        btn_extrair.pack(side='right', padx=(5, 0))

        # Botão Resolver com IA
        btn_resolver_ia = Button(
            action_frame,
            text="🤖 Resolver com IA",
            font=('Arial', 11, 'bold'),
            bg='#E91E63',
            fg='white',
            cursor='hand2',
            padx=15,
            pady=8,
            command=lambda: self.__resolver_com_ia(tipo)
        )
        btn_resolver_ia.pack(side='right', padx=(5, 0))

    def __get_dataframe_por_tipo(self, tipo):
        tipo = tipo.strip().lower()
        if tipo == "atividades pendentes":
            return self.dataframe_atividades_pendentes
        elif tipo == "notas faltantes":
            return self.dataframe_notas_boletim
        elif tipo == "quantidade de faltas":
            return self.dataframe_quantidade_faltas


    def exportar_xlsx(self, tipo):
        dataframe_atual = self.__get_dataframe_por_tipo(tipo)

        if dataframe_atual is None or dataframe_atual.empty:
            messagebox.showwarning(
                "Aviso", f"Não há dados de {tipo} para exportar!")
            return

        try:
            filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title=f"Salvar {tipo} como Excel",
            initialfile=f"{tipo.replace(' ', '_').lower()}.xlsx"
        )

            if filename:
                dataframe_atual.to_excel(filename, index=False)
                messagebox.showinfo(
                    "Sucesso", f"Arquivo salvo como:\n{filename}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar XLSX:\n{str(e)}")

    def exportar_csv(self, tipo):
        dataframe_atual = self.__get_dataframe_por_tipo(tipo)

        if dataframe_atual is None or dataframe_atual.empty:
            messagebox.showwarning(
                "Aviso", f"Não há dados de {tipo} para exportar!")
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title=f"Salvar {tipo} como CSV",
                initialfile=f"{tipo.replace(' ', '_').lower()}.csv"
            )

            if filename:
                dataframe_atual.to_csv(
                    filename, index=False, encoding='utf-8-sig')
                messagebox.showinfo(
                    "Sucesso", f"Arquivo salvo como:\n{filename}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar CSV:\n{str(e)}")

    def __obter_linha_selecionada(self):
        """Obtém os dados da linha selecionada na TreeView"""
        if not hasattr(self, 'tree'):
            messagebox.showwarning(
                "Aviso", "Nenhuma tabela está sendo exibida no momento.")
            return None

        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning(
                "Aviso", "Por favor, selecione uma linha na tabela.")
            return None

        # Pegar o primeiro item selecionado
        item = selected_items[0]
        valores = self.tree.item(item, 'values')
        colunas = self.tree['columns']

        # Criar dicionário com coluna: valor
        dados_linha = {}
        for i, coluna in enumerate(colunas):
            dados_linha[coluna] = valores[i] if i < len(valores) else ''

        return dados_linha

    def __resolver_com_ia(self, tipo):
        """Função para resolver atividade com IA baseada na linha selecionada"""
        dados_linha = self.__obter_linha_selecionada()

        if dados_linha is None:
            return

        # Aqui você implementará a lógica de resolução com IA
        # Por enquanto, mostro os dados selecionados
        dados_texto = "\n".join(
            [f"{col}: {valor}" for col, valor in dados_linha.items()])

        messagebox.showinfo(
            f"Resolver com IA - {tipo}",
            f"Dados selecionados para resolução com IA:\n\n{dados_texto}\n\n"
            f"Funcionalidade de IA será implementada aqui."
        )

    def __extrair_atividade(self, tipo):
        """Função para extrair atividade baseada na linha selecionada"""
        dados_linha = self.__obter_linha_selecionada()

        if dados_linha is None:
            return

        # Aqui você implementará a lógica de extração
        # Por enquanto, mostro os dados selecionados
        dados_texto = "\n".join(
            [f"{col}: {valor}" for col, valor in dados_linha.items()])

        messagebox.showinfo(
            f"Extrair Atividade - {tipo}",
            f"Dados selecionados para extração:\n\n{dados_texto}\n\n"
            f"Funcionalidade de extração será implementada aqui."
        )
