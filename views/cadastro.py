import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from models.adm import salvar_usuario  # Função para salvar usuário no banco


def abrir_cadastro(janela_login):
    from views.login import iniciar_login  # Função para abrir a janela de login

    def cadastrar_usuario():
        # Pega os dados digitados nas caixas de entrada
        novo_user = entry_novo_usuario.get()
        nova_senha = entry_nova_senha.get()
        confirmar_senha = entry_confirmar_senha.get()

        # Verifica se as senhas coincidem
        if nova_senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        # Tenta salvar o usuário no banco
        if salvar_usuario(novo_user, nova_senha):
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            cadastro_janela.destroy()  # Fecha a janela de cadastro
            iniciar_login()  # Abre a janela de login
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar usuário.")

    janela_login.destroy()  # Fecha a janela de login atual

    # Cria a nova janela de cadastro
    cadastro_janela = ctk.CTk()
    cadastro_janela.title("Cadastro de Usuário")
    cadastro_janela.geometry("400x400")

    # Label e campo para novo usuário
    ctk.CTkLabel(cadastro_janela, text="Novo Usuário").pack(pady=10)
    entry_novo_usuario = ctk.CTkEntry(cadastro_janela)
    entry_novo_usuario.pack(pady=10)

    # Label e campo para nova senha
    ctk.CTkLabel(cadastro_janela, text="Nova Senha").pack(pady=10)
    entry_nova_senha = ctk.CTkEntry(
        cadastro_janela, show="*")  # Oculta o texto digitado
    entry_nova_senha.pack(pady=10)

    # Label e campo para confirmar senha
    ctk.CTkLabel(cadastro_janela, text="Confirmar Senha").pack(pady=10)
    entry_confirmar_senha = ctk.CTkEntry(cadastro_janela, show="*")
    entry_confirmar_senha.pack(pady=10)

    # Botão para cadastrar, que chama a função cadastrar_usuario
    ctk.CTkButton(cadastro_janela, text="Cadastrar",
                  command=cadastrar_usuario).pack(pady=20)

    cadastro_janela.mainloop()  # Inicia o loop da interface gráfica da janela de cadastro
