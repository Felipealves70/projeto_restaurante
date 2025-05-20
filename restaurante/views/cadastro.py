import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from models.adm import salvar_usuario

def abrir_cadastro():
        from views.login import iniciar_login
        def cadastrar_usuario():
            novo_user = entry_novo_usuario.get()
            nova_senha = entry_nova_senha.get()
            confirmar_senha = entry_confirmar_senha.get()

            if nova_senha != confirmar_senha:
                messagebox.showerror("Erro", "As senhas não coincidem.")
                return

            # Aqui você chamaria uma função para salvar o usuário no banco
            # Exemplo fictício: salvar_usuario(novo_user, nova_senha)
            # Você deve implementar `salvar_usuario` em `db.py`
            if salvar_usuario(novo_user, nova_senha):
                messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
                cadastro_janela.destroy()
                iniciar_login()
            else:
                messagebox.showerror("Erro", "Erro ao cadastrar usuário.")

        cadastro_janela = ctk.CTkToplevel()
        cadastro_janela.title("Cadastro de Usuário")
        cadastro_janela.geometry("400x400")

        ctk.CTkLabel(cadastro_janela, text="Novo Usuário").pack(pady=10)
        entry_novo_usuario = ctk.CTkEntry(cadastro_janela)
        entry_novo_usuario.pack(pady=10)

        ctk.CTkLabel(cadastro_janela, text="Nova Senha").pack(pady=10)
        entry_nova_senha = ctk.CTkEntry(cadastro_janela, show="*")
        entry_nova_senha.pack(pady=10)

        ctk.CTkLabel(cadastro_janela, text="Confirmar Senha").pack(pady=10)
        entry_confirmar_senha = ctk.CTkEntry(cadastro_janela, show="*")
        entry_confirmar_senha.pack(pady=10)

        ctk.CTkButton(cadastro_janela, text="Cadastrar", command=cadastrar_usuario).pack(pady=20)