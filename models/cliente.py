import database.db as banco

# Função para adicionar um novo cliente no banco e retornar o ID criado


def adicionar_cliente(nome, telefone, email):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)", (nome, telefone, email))
    con.commit()
    cliente_id = cursor.lastrowid  # Obtém o ID do cliente recém-inserido
    con.close()
    return cliente_id

# Função para listar todos os clientes cadastrados no banco


def listar_clientes():
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id, nome, telefone, email FROM clientes")
    resultado = cursor.fetchall()  # Retorna todos os registros como lista de tuplas
    con.close()
    return resultado

# Função para atualizar os dados de um cliente existente, baseado no ID


def atualizar_cliente(cliente_id, novo_nome, novo_telefone, novo_email):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("UPDATE clientes SET nome = ?, telefone = ?, email = ? WHERE id = ?",
                   (novo_nome, novo_telefone, novo_email, cliente_id))
    con.commit()
    con.close()

# Função para excluir um cliente do banco de dados pelo seu ID


def excluir_cliente(cliente_id):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    con.commit()
    con.close()
