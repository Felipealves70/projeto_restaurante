import sqlite3

# Função que estabelece a conexão com o banco de dados


def conectar():
    return sqlite3.connect('restaurante.db')

# Função que cria todas as tabelas necessárias no banco de dados, caso ainda não existam


def criar_tabelas():
    con = conectar()
    cursor = con.cursor()

    # Cria a tabela de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT)
    ''')

    # Cria a tabela de mesas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL UNIQUE,
            capacidade INTEGER NOT NULL)
    ''')

    # Cria a tabela de reservas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            mesa_id INTEGER,
            data TEXT,
            horario TEXT,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id),
            FOREIGN KEY(mesa_id) REFERENCES mesas(id))
    ''')

    # Cria a tabela de administradores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS adm (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            usuario TEXT,
            senha INTEGER
        )
    ''')

    con.commit()
    con.close()
