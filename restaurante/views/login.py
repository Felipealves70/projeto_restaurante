import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from database.db import verificar_login
from views.interface import janela_principal
from views.cadastro import abrir_cadastro

def iniciar_login():
    def fazer_login():
        user = entry_usuario.get()
        senha = entry_senha.get()
        if verificar_login(user, senha):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            root.destroy()
            janela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    # Configurações gerais
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Login")
    root.geometry("850x550")
    root.grid_columnconfigure((0, 1), weight=1)
    root.grid_rowconfigure(0, weight=1)

    # === FRAME ESQUERDO COM IMAGEM ===
    frame_esquerdo = ctk.CTkFrame(root, corner_radius=0, fg_color="#eeedee")
    frame_esquerdo.grid(row=0, column=0, sticky="nsew")
    frame_esquerdo.grid_rowconfigure(0, weight=1)
    frame_esquerdo.grid_columnconfigure(0, weight=1)

    imagem = Image.open("restaurante/views/img/logopng.png")
    imagem_resized = ctk.CTkImage(imagem, size=(500, 500))  # tamanho base

    imagem_label = ctk.CTkLabel(frame_esquerdo, image=imagem_resized, text="")
    imagem_label.grid(row=0, column=0, sticky="nsew")

    # === FRAME DIREITO COM FORMULÁRIO ===
    frame_direito = ctk.CTkFrame(root)
    frame_direito.grid(row=0, column=1, sticky="nsew")
    frame_direito.grid_rowconfigure((0, 1, 2), weight=1)
    frame_direito.grid_columnconfigure(0, weight=1)

    # Sub-frame centralizado para o conteúdo
    conteudo = ctk.CTkFrame(frame_direito, fg_color="transparent")
    conteudo.grid(row=1, column=0, sticky="n")
    conteudo.grid_columnconfigure(1, weight=1)

    # Campos e labels
    label_usuario = ctk.CTkLabel(conteudo, text="Usuário", font=('Arial', 16))
    label_usuario.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    entry_usuario = ctk.CTkEntry(
        conteudo, width=250, corner_radius=10, height=45)
    entry_usuario.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    label_senha = ctk.CTkLabel(conteudo, text="Senha", font=('Arial', 16))
    label_senha.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    entry_senha = ctk.CTkEntry(
        conteudo, show="*", width=250, corner_radius=10, height=45)
    entry_senha.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    botao_login = ctk.CTkButton(
        conteudo, height=40, text="Entrar", command=fazer_login, width=250, corner_radius=20)
    botao_login.grid(row=4, column=0, columnspan=2, pady=20)

# Botão de cadastro
    botao_cadastro = ctk.CTkButton(
        conteudo, height=35, text="Cadastrar", command=abrir_cadastro, width=250, corner_radius=20, fg_color="gray")
    botao_cadastro.grid(row=5, column=0, columnspan=2, pady=(0, 10))

    root.mainloop()
