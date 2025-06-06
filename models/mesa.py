import database.db as banco

# Função para listar todas as mesas cadastradas, retornando o id e o número de cada mesa


def listar_mesas():
    con = banco.conectar()
    cursor = con.cursor()
    # Consulta os campos id e numero da tabela mesas
    cursor.execute("SELECT id, numero FROM mesas")
    resultado = cursor.fetchall()  # Pega todos os registros retornados na consulta
    con.close()
    return resultado  # Retorna a lista de mesas (tuplas com id e numero)
