import sqlite3
from tkinter import messagebox

# Função que conecta ao banco de dados


def conectar():
    return sqlite3.connect('restaurante.db')

# Função que salva um novo usuário administrador no banco, verificando se já existe


def salvar_usuario(usuario, senha):
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Verifica se o usuário já está cadastrado
        cursor.execute("SELECT * FROM adm WHERE usuario = ?", (usuario,))
        if cursor.fetchone():
            messagebox.showerror("Erro", "Usuário já existe.")
            return False

        # Insere o novo usuário na tabela
        cursor.execute(
            "INSERT INTO adm (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
        return False

# Função que verifica se as credenciais de login estão corretas


def verificar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()

    # Busca usuário com login e senha informados
    cursor.execute(
        "SELECT * FROM adm WHERE usuario = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()

    # Retorna True se encontrou usuário, False caso contrário
    return resultado is not None
