from PIL import Image, ImageTk
import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime, timedelta, date
from tkinter import messagebox
import controllers.reserva_controller as ctrl_res
import controllers.cliente_controller as ctrl_cli
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

    # Frame central
    frame_interno = ctk.CTkFrame(conteudo_frame, corner_radius=10)
    frame_interno.place(relx=0.5, y=50, anchor="n")

    reservas = ctrl_res.get_reservas()
    reserva_dict = {
        f"Mesa {r[2]} - {r[1]} ({r[4]} {r[5]})": r[0] for r in reservas}

    ctk.CTkLabel(frame_interno, text="Selecione a Reserva").grid(
        row=0, column=0, padx=10, pady=15)
    lista = ctk.CTkComboBox(frame_interno, width=300, height=35,
                            values=list(reserva_dict.keys()))
    lista.grid(row=0, column=1, padx=10, pady=30)

    ctk.CTkLabel(frame_interno, text="Data").grid(
        row=0, column=2, padx=10, pady=30)
    data_entry = DateEntry(frame_interno, width=30, height=35, date_pattern="dd-mm-yyyy",
                           locale="pt_BR", mindate=date.today())
    data_entry.grid(row=0, column=3, padx=10, pady=30)

    ctk.CTkLabel(frame_interno, text="Horário").grid(
        row=1, column=0, padx=10, pady=30)
    horario_combo = ctk.CTkComboBox(
        frame_interno, width=200, height=35, values=gerar_horarios())
    horario_combo.grid(row=1, column=1, padx=10, pady=30)

    ctk.CTkLabel(frame_interno, text="Mesa").grid(
        row=1, column=2, padx=10, pady=30)
    mesa_combo = ctk.CTkComboBox(
        frame_interno, width=200, height=35, values=ctrl_res.get_mesas_para_combobox())
    mesa_combo.grid(row=1, column=3, padx=10, pady=30)

    def preencher_campos_reserva():
        selecionado = lista.get()
        reserva_id = reserva_dict.get(selecionado)
        if reserva_id:
            for r in reservas:
                if r[0] == reserva_id:
                    data_entry.set_date(r[4])
                    horario_combo.set(r[5])
                    mesa_combo.set(f"Mesa {r[2]}")
                    break

    lista.configure(command=lambda _: preencher_campos_reserva())

    def atualizar():
        item = lista.get()
        if item not in reserva_dict:
            messagebox.showwarning(
                "Seleção inválida", "Por favor, selecione uma reserva válida.")
            return

        reserva_id = reserva_dict[item]
        data = data_entry.get_date().strftime("%d-%m-%Y")
        mesa_nome = mesa_combo.get()
        if ctrl_res.editar_reserva(
                reserva_id, data, horario_combo.get(), mesa_nome):
            messagebox.showinfo("Atualização", "Reserva atualizada!")
            abrir_edicao(conteudo_frame)
        else:
            messagebox.showerror("Erro", "Ediçao não realizada!")

    ctk.CTkButton(frame_interno, text="Atualizar", width=200, height=35,
                  command=atualizar).grid(row=2, column=0, padx=10, pady=30)


def abrir_cancelamento(conteudo_frame):
    limpar_conteudo(conteudo_frame)

    # Frame central
    frame_interno = ctk.CTkFrame(conteudo_frame, corner_radius=10)
    frame_interno.place(relx=0.5, y=50, anchor="n")

    reservas = ctrl_res.get_reservas()
    reserva_dict = {
        f"Mesa {r[2]} - {r[1]} ({r[4]} {r[5]})": r[0] for r in reservas}

    lista = ctk.CTkComboBox(frame_interno, width=350,
                            values=list(reserva_dict.keys()))
    lista.grid(row=0, column=0, padx=35, pady=30)

    def cancelar():
        item = lista.get()
        if item:
            reserva_id = reserva_dict[item]
            ctrl_res.excluir_reserva(reserva_id)
            messagebox.showinfo("Cancelamento", "Reserva cancelada!")
            abrir_cancelamento(conteudo_frame)

    ctk.CTkButton(frame_interno, width=200, height=35, text="Cancelar Reserva",
                  command=cancelar).grid(row=1, column=0, pady=20, padx=35)


def abrir_gerenciar_clientes(conteudo_frame):
    limpar_conteudo(conteudo_frame)

    # Frame central
    frame_interno = ctk.CTkFrame(conteudo_frame, corner_radius=10)
    frame_interno.place(relx=0.5, y=50, anchor="n")

    clientes = ctrl_cli.get_clientes()
    cliente_dict = {f"{c[1]} | Tel: {c[2]} | Email: {c[3]}": c[0]
                    for c in clientes}

    ctk.CTkLabel(frame_interno, text="Selecione um cliente").grid(
        row=0, column=0)
    lista = ctk.CTkComboBox(frame_interno, width=400,
                            height=35, values=list(cliente_dict.keys()))
    lista.grid(row=0, column=1, padx=30, pady=30)

    ctk.CTkLabel(frame_interno, text="Nome").grid(
        row=1, column=0, pady=30, padx=30)
    nome_entry = ctk.CTkEntry(frame_interno, width=200, height=35)
    nome_entry.grid(row=1, column=1)

    ctk.CTkLabel(frame_interno, text="Telefone").grid(row=1, column=3)
    telefone_entry = ctk.CTkEntry(frame_interno, width=200, height=35)
    telefone_entry.grid(row=1, column=4, padx=30, pady=30)
    telefone_entry.bind(
        "<KeyRelease>", lambda event: formatar_telefone(telefone_entry))

    ctk.CTkLabel(frame_interno, text="E-mail").grid(row=2, column=0)
    email_entry = ctk.CTkEntry(
        frame_interno, width=200, height=35)
    email_entry.grid(row=2, column=1, padx=30, pady=30)

    def preencher_campos_cliente():
        selecionado = lista.get()
        cliente_id = cliente_dict.get(selecionado)
        if cliente_id:
            for c in clientes:
                if c[0] == cliente_id:
                    nome_entry.delete(0, ctk.END)
                    nome_entry.insert(0, c[1])
                    telefone_entry.delete(0, ctk.END)
                    telefone_entry.insert(0, c[2])
                    email_entry.delete(0, ctk.END)
                    email_entry.insert(0, c[3])
                    break

    lista.configure(command=lambda _: preencher_campos_cliente())

    def atualizar():
        selecionado = lista.get()
        if selecionado:
            cliente_id = cliente_dict[selecionado]
            ctrl_cli.editar_cliente(cliente_id, nome_entry.get(
            ), telefone_entry.get(), email_entry.get())
            messagebox.showinfo(
                "Atualizado", "Cliente atualizado com sucesso.")
            abrir_gerenciar_clientes(conteudo_frame)

    def excluir():
        selecionado = lista.get()
        if selecionado:
            cliente_id = cliente_dict[selecionado]
            if messagebox.askyesno("Confirmação", "Deseja realmente excluir este cliente?"):
                ctrl_cli.remover_cliente(cliente_id)
                messagebox.showinfo(
                    "Excluído", "Cliente excluído com sucesso.")
                abrir_gerenciar_clientes(conteudo_frame)

    ctk.CTkButton(frame_interno, width=200, height=35, text="Atualizar Cliente",
                  command=atualizar).grid(row=3, column=0, padx=30, pady=10)
    ctk.CTkButton(frame_interno, width=200, height=35, text="Excluir Cliente",
                  command=excluir).grid(row=4, column=0, padx=30, pady=10)


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
    root.grid_columnconfigure(1, weight=1)  # Conteúdo cresce
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
        ("Nova Reserva", abrir_nova_reserva, "restaurante/views/icons/add.png"),
        ("Ver Reservas", abrir_reservas, "restaurante/views/icons/view.png"),
        ("Editar Reserva", abrir_edicao, "restaurante/views/icons/edit.png"),
        ("Cancelar Reserva", abrir_cancelamento,
         "restaurante/views/icons/cancel.png"),
        ("Gerenciar Clientes", abrir_gerenciar_clientes,
         "restaurante/views/icons/group.png"),
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
