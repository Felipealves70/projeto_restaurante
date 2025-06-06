from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta, date
from tkinter import messagebox
import controllers.reserva_controller as ctrl_res
import controllers.cliente_controller as ctrl_cli
from models.relatorio import exportar_csv
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


def limpar_conteudo(conteudo_frame):
    for widget in conteudo_frame.winfo_children():
        widget.destroy()


def gerar_horarios():
    inicio = datetime.strptime("17:00", "%H:%M")
    fim = datetime.strptime("22:00", "%H:%M")
    horarios = []
    atual = inicio
    while atual <= fim:
        horarios.append(atual.strftime("%H:%M"))
        atual += timedelta(minutes=30)
    return horarios


def formatar_telefone(entry):
    telefone = entry.get()
    numeros = ''.join(filter(str.isdigit, telefone))[:11]

    telefone_formatado = ""
    if len(numeros) >= 2:
        telefone_formatado = f"({numeros[:2]})"
        if len(numeros) >= 7:
            telefone_formatado += f"{numeros[2:7]}-{numeros[7:]}"
        elif len(numeros) > 2:
            telefone_formatado += numeros[2:]
    else:
        telefone_formatado = numeros

    entry.delete(0, ctk.END)
    entry.insert(0, telefone_formatado)


def abrir_nova_reserva(conteudo_frame):
    limpar_conteudo(conteudo_frame)

    # Frame central
    frame_interno = ctk.CTkFrame(conteudo_frame, corner_radius=10)
    frame_interno.place(relx=0.5, y=50, anchor="n")

    # Widgets no frame interno
    ctk.CTkLabel(frame_interno, text="Nome do Cliente").grid(
        row=0, column=0, padx=20, pady=20)
    nome_entry = ctk.CTkEntry(frame_interno, width=200, height=35)
    nome_entry.grid(row=0, column=1, padx=20, pady=20)

    ctk.CTkLabel(frame_interno, text="Telefone").grid(
        row=0, column=2, padx=20, pady=20)
    telefone_entry = ctk.CTkEntry(frame_interno, width=200, height=35)
    telefone_entry.grid(row=0, column=3, padx=20, pady=20)
    telefone_entry.bind(
        "<KeyRelease>", lambda event: formatar_telefone(telefone_entry))

    ctk.CTkLabel(frame_interno, text="E-mail").grid(row=1,
                                                    column=0, padx=20, pady=20)
    email_entry = ctk.CTkEntry(frame_interno, width=200, height=35)
    email_entry.grid(row=1, column=1, padx=20, pady=20)

    ctk.CTkLabel(frame_interno, text="Data").grid(
        row=1, column=2, padx=20, pady=20)
    data_entry = DateEntry(frame_interno, width=30, height=35, date_pattern="dd-mm-yyyy",
                           locale="pt_BR", mindate=date.today())
    data_entry.grid(row=1, column=3, padx=20, pady=20)

    ctk.CTkLabel(frame_interno, text="Horário").grid(
        row=2, column=0, padx=20, pady=20)
    horario_combo = ctk.CTkComboBox(
        frame_interno, width=200, height=35,  values=gerar_horarios())
    horario_combo.grid(row=2, column=1, padx=20, pady=20)

    ctk.CTkLabel(frame_interno, text="Mesa").grid(
        row=2, column=2, padx=20, pady=20)
    mesa_combo = ctk.CTkComboBox(
        frame_interno, width=200, height=35, values=ctrl_res.get_mesas_para_combobox())
    mesa_combo.grid(row=2, column=3, padx=20, pady=20)

    def confirmar():
        nome = nome_entry.get()
        telefone = telefone_entry.get()
        email = email_entry.get()
        data = data_entry.get_date().strftime("%d-%m-%Y")
        horario = horario_combo.get()
        mesa = mesa_combo.get()

        if not (nome and telefone and email and data and horario and mesa):
            messagebox.showwarning(
                "Campos vazios", "Preencha todos os campos!")
            return

        if ctrl_res.processar_reserva(nome, telefone, email, data, horario, mesa):
            messagebox.showinfo("Reserva", "Reserva realizada com sucesso!")
            abrir_nova_reserva(conteudo_frame)
        else:
            messagebox.showerror("Erro", "Mesa indisponível nesse horário.")

    ctk.CTkButton(frame_interno, text="Confirmar", command=confirmar).grid(
        row=3, column=0, columnspan=4, pady=20)


def abrir_edicao(conteudo_frame):
    limpar_conteudo(conteudo_frame)

    frame_interno = ctk.CTkFrame(conteudo_frame, corner_radius=10)
    frame_interno.place(relx=0.5, y=50, anchor="n")

    reservas = ctrl_res.get_reservas()
    reserva_dict = {}

    ctk.CTkLabel(frame_interno, text="Selecione a Reserva").grid(
        row=0, column=0, columnspan=4, padx=10, pady=(10, 5))

    # Frame CTK com a Treeview
    tree_frame = ctk.CTkFrame(frame_interno, fg_color="transparent")
    tree_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=5)

    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    background="#2b2b2b",
                    foreground="white",
                    rowheight=30,
                    fieldbackground="#2b2b2b",
                    font=('Arial', 12))

    style.configure("Treeview.Heading",
                    background="#1f1f1f",
                    foreground="white",
                    font=('Arial', 13, 'bold'))

    style.map('Treeview', background=[('selected', '#3a7ff6')])

    # Scrollbar
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(tree_frame, columns=("nome", "mesa", "data", "hora"),
                        show="headings", height=5, yscrollcommand=tree_scroll.set)
    tree.heading("nome", text="Cliente")
    tree.heading("mesa", text="Mesa")
    tree.heading("data", text="Data")
    tree.heading("hora", text="Hora")
    tree.column("nome", width=150)
    tree.column("mesa", width=80)
    tree.column("data", width=100)
    tree.column("hora", width=100)
    tree.pack()

    tree_scroll.config(command=tree.yview)

    for r in reservas:
        tree.insert("", "end", values=(r[1], f"Mesa {r[2]}", r[4], r[5]))
        reserva_dict[(r[1], f"Mesa {r[2]}", r[4], r[5])] = r[0]

    # Campos de edição
    ctk.CTkLabel(frame_interno, text="Data").grid(
        row=2, column=0, padx=10, pady=10)
    data_entry = DateEntry(frame_interno, width=30, height=35, date_pattern="dd-mm-yyyy",
                           locale="pt_BR", mindate=date.today())
    data_entry.grid(row=2, column=1, padx=10, pady=10)

    ctk.CTkLabel(frame_interno, text="Horário").grid(
        row=2, column=2, padx=10, pady=10)
    horario_combo = ctk.CTkComboBox(
        frame_interno, width=200, height=35, values=gerar_horarios())
    horario_combo.grid(row=2, column=3, padx=10, pady=10)

    ctk.CTkLabel(frame_interno, text="Mesa").grid(
        row=3, column=0, padx=10, pady=10)
    mesa_combo = ctk.CTkComboBox(
        frame_interno, width=200, height=35, values=ctrl_res.get_mesas_para_combobox())
    mesa_combo.grid(row=3, column=1, padx=10, pady=10)

    def preencher_campos_reserva(event):
        selecionado = tree.focus()
        if not selecionado:
            return
        valores = tree.item(selecionado)["values"]
        if len(valores) != 4:
            return
        nome, mesa, data, hora = valores
        data_entry.set_date(data)
        horario_combo.set(hora)
        mesa_combo.set(mesa)

    tree.bind("<<TreeviewSelect>>", preencher_campos_reserva)

    def atualizar():
        selecionado = tree.focus()
        if not selecionado:
            messagebox.showwarning(
                "Seleção inválida", "Selecione uma reserva.")
            return

        valores = tree.item(selecionado)["values"]
        if len(valores) != 4:
            return

        nome, mesa_antiga, data_antiga, hora_antiga = valores
        reserva_id = reserva_dict.get(
            (nome, mesa_antiga, data_antiga, hora_antiga))
        if not reserva_id:
            messagebox.showerror("Erro", "Reserva não encontrada.")
            return

        nova_data = data_entry.get_date().strftime("%d-%m-%Y")
        novo_horario = horario_combo.get()
        nova_mesa = mesa_combo.get()

        if ctrl_res.editar_reserva(reserva_id, nova_data, novo_horario, nova_mesa):
            messagebox.showinfo("Atualização", "Reserva atualizada!")
            abrir_edicao(conteudo_frame)
        else:
            messagebox.showerror("Erro", "Edição não realizada!")

    ctk.CTkButton(frame_interno, text="Atualizar", width=200, height=35,
                  command=atualizar).grid(row=4, column=0, columnspan=4, pady=20)


def abrir_cancelamento(conteudo_frame):

    limpar_conteudo(conteudo_frame)

    # Frame central
    frame_interno = ctk.CTkFrame(conteudo_frame, corner_radius=10)
    frame_interno.place(relx=0.5, y=50, anchor="n")

    # Treeview
    tree_frame = ctk.CTkFrame(frame_interno)
    tree_frame.grid(row=0, column=0, padx=20, pady=20)

    tree = ttk.Treeview(tree_frame, columns=(
        "nome", "mesa", "data", "hora"), show="headings", height=8)
    tree.heading("nome", text="Nome")
    tree.heading("mesa", text="Mesa")
    tree.heading("data", text="Data")
    tree.heading("hora", text="Hora")
    tree.column("nome", width=150)
    tree.column("mesa", width=80)
    tree.column("data", width=100)
    tree.column("hora", width=100)
    tree.pack()

    # Estilo escuro
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#2b2b2b",
                    foreground="white",
                    rowheight=30,
                    fieldbackground="#2b2b2b",
                    font=('Arial', 12))
    style.configure("Treeview.Heading",
                    background="#1f1f1f",
                    foreground="white",
                    font=('Arial', 13, 'bold'))
    style.map('Treeview', background=[('selected', '#3a7ff6')])

    # Dicionário de reservas
    reservas = ctrl_res.get_reservas()
    reserva_dict = {}
    for r in reservas:
        reserva_dict[str(r[0])] = r
        tree.insert("", "end", iid=str(r[0]), values=(
            r[1], f"Mesa {r[2]}", r[4], r[5]))

    def cancelar():
        item = tree.selection()
        if not item:
            messagebox.showwarning(
                "Atenção", "Selecione uma reserva para cancelar.")
            return

        reserva_id = int(item[0])
        ctrl_res.excluir_reserva(reserva_id)
        messagebox.showinfo("Cancelamento", "Reserva cancelada!")
        abrir_cancelamento(conteudo_frame)

    ctk.CTkButton(frame_interno, width=200, height=35, text="Cancelar Reserva",
                  command=cancelar).grid(row=1, column=0, pady=20)


def abrir_gerenciar_clientes(conteudo_frame):

    limpar_conteudo(conteudo_frame)

    frame_interno = ctk.CTkFrame(conteudo_frame, corner_radius=10)
    frame_interno.place(relx=0.5, y=50, anchor="n")

    clientes = ctrl_cli.get_clientes()
    cliente_dict = {str(c[0]): c for c in clientes}

    # Treeview Frame
    tree_frame = ctk.CTkFrame(frame_interno)
    tree_frame.grid(row=0, column=0, columnspan=5, pady=20)

    tree = ttk.Treeview(tree_frame, columns=(
        "nome", "telefone", "email"), show="headings", height=8)
    tree.heading("nome", text="Nome")
    tree.heading("telefone", text="Telefone")
    tree.heading("email", text="Email")
    tree.column("nome", width=200)
    tree.column("telefone", width=200)
    tree.column("email", width=200)
    tree.pack()

    # Estilo escuro para o Treeview
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#2b2b2b",
                    foreground="white",
                    rowheight=30,
                    fieldbackground="#2b2b2b",
                    font=('Arial', 12))
    style.configure("Treeview.Heading",
                    background="#1f1f1f",
                    foreground="white",
                    font=('Arial', 13, 'bold'))
    style.map('Treeview', background=[('selected', '#3a7ff6')])

    # Inserir dados na Treeview
    for c in clientes:
        tree.insert("", "end", iid=str(c[0]), values=(c[1], c[2], c[3]))

    # Campos de edição
    ctk.CTkLabel(frame_interno, text="Nome").grid(
        row=1, column=0, padx=20, pady=10)
    nome_entry = ctk.CTkEntry(frame_interno, width=200, height=35)
    nome_entry.grid(row=1, column=1)

    ctk.CTkLabel(frame_interno, text="Telefone").grid(row=1, column=2, padx=20)
    telefone_entry = ctk.CTkEntry(frame_interno, width=200, height=35)
    telefone_entry.grid(row=1, column=3)
    telefone_entry.bind(
        "<KeyRelease>", lambda event: formatar_telefone(telefone_entry))

    ctk.CTkLabel(frame_interno, text="E-mail").grid(row=2, column=0, padx=20)
    email_entry = ctk.CTkEntry(frame_interno, width=200, height=35)
    email_entry.grid(row=2, column=1, padx=20, pady=10)

    cliente_selecionado_id = [None]

    def on_select(event):
        selecionado = tree.selection()
        if selecionado:
            cid = selecionado[0]
            cliente_selecionado_id[0] = int(cid)
            c = cliente_dict[cid]
            nome_entry.delete(0, ctk.END)
            nome_entry.insert(0, c[1])
            telefone_entry.delete(0, ctk.END)
            telefone_entry.insert(0, c[2])
            email_entry.delete(0, ctk.END)
            email_entry.insert(0, c[3])

    tree.bind("<<TreeviewSelect>>", on_select)

    def atualizar():
        cid = cliente_selecionado_id[0]
        if cid is None:
            messagebox.showwarning(
                "Aviso", "Selecione um cliente para atualizar.")
            return
        ctrl_cli.editar_cliente(cid, nome_entry.get(),
                                telefone_entry.get(), email_entry.get())
        messagebox.showinfo("Atualizado", "Cliente atualizado com sucesso.")
        abrir_gerenciar_clientes(conteudo_frame)

    def excluir():
        cid = cliente_selecionado_id[0]
        if cid is None:
            messagebox.showwarning(
                "Aviso", "Selecione um cliente para excluir.")
            return
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este cliente?"):
            ctrl_cli.remover_cliente(cid)
            messagebox.showinfo("Excluído", "Cliente excluído com sucesso.")
            abrir_gerenciar_clientes(conteudo_frame)

    ctk.CTkButton(frame_interno, width=200, height=35, text="Atualizar Cliente",
                  command=atualizar).grid(row=3, column=0, padx=30, pady=10)
    ctk.CTkButton(frame_interno, width=200, height=35, text="Excluir Cliente",
                  command=excluir).grid(row=3, column=1, padx=30, pady=10)


def abrir_reservas(conteudo_frame):
    limpar_conteudo(conteudo_frame)

    # Frame central
    frame_interno = ctk.CTkFrame(conteudo_frame, corner_radius=10)
    frame_interno.place(relx=0.5, y=50, anchor="n")

    reservas = ctrl_res.get_reservas()
    for r in reservas:
        texto = f"{r[1]} - Mesa {r[2]} ({r[4]} {r[5]})"
        ctk.CTkLabel(frame_interno, text=texto,
                     anchor="w").pack(fill="x", padx=35, pady=15)


def janela_principal():
    root = ctk.CTk()
    root.title("Restaurante")
    root.geometry("900x450")

    # Layout principal: 2 colunas (menu à esquerda, conteúdo à direita)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    menu_lateral = ctk.CTkFrame(
        root, width=250, corner_radius=0, fg_color="#2e2e2e")
    menu_lateral.grid(row=0, column=0, sticky="ns")
    menu_lateral.grid_propagate(False)
    menu_lateral.grid_columnconfigure(0, weight=1)

    label = ctk.CTkLabel(menu_lateral, text="Menu", font=("Arial", 16))
    label.grid(row=1, column=0)

    # Função para carregar ícones com tamanho adequado
    def carregar_icone(caminho, tamanho=(20, 20)):
        if os.path.exists(caminho):
            return ctk.CTkImage(Image.open(caminho), size=tamanho)
        else:
            print(f"⚠️ Ícone não encontrado: {caminho}")
            return None

    # --- Lista com (texto do botão, função que será chamada) ---
    botoes_menu = [
        ("Nova Reserva", abrir_nova_reserva, "views/icons/add.png"),
        ("Ver Reservas", abrir_reservas, "views/icons/view.png"),
        ("Editar Reserva", abrir_edicao, "views/icons/edit.png"),
        ("Cancelar Reserva", abrir_cancelamento,
         "views/icons/cancel.png"),
        ("Gerenciar Clientes", abrir_gerenciar_clientes,
         "views/icons/group.png"),
        ("Exportar CSV", exportar_csv,
         "views/icons/csv.png"),
    ]

    # Criar botões dinamicamente
    for i, (texto, funcao, caminho_icone) in enumerate(botoes_menu, start=2):
        icone = carregar_icone(caminho_icone)
        botao = ctk.CTkButton(
            menu_lateral,
            height=40,
            text=texto,
            image=icone,
            compound="left",
            anchor="w",
            command=lambda f=funcao: f(conteudo_frame)
        )
        botao.grid(row=i, padx=15, column=0, pady=10, sticky="ew")

    conteudo_frame = ctk.CTkFrame(root, corner_radius=0)
    conteudo_frame.grid(row=0, column=1, sticky="nsew")

    # Exibe conteúdo inicial (ex: Nova Reserva)
    abrir_nova_reserva(conteudo_frame)

    root.mainloop()


if __name__ == "__main__":
    janela_principal()
