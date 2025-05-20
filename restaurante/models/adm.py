import sqlite3

def salvar_usuario(usuario, senha):
    try:
        conn = sqlite3.connect("restaurante/restaurante.db")  # Substitua pelo caminho real do seu banco
        cursor = conn.cursor()

        # Verifica se o usuário já existe
        cursor.execute("SELECT * FROM adm WHERE usuario = ?", (usuario,))
        if cursor.fetchone():
            print("Usuário já existe.")
            return False

        # Insere novo usuário
        cursor.execute("INSERT INTO adm (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
        return False