import database.db as banco

# Insere mesas iniciais no banco de dados, numeradas de 1 a 10, cada uma com capacidade para 4 pessoas


def inserir_mesas_iniciais():
    con = banco.conectar()
    cursor = con.cursor()
    for i in range(1, 11):  # Loop de 1 até 10
        try:
            # Tenta inserir uma mesa com número i e capacidade 4
            cursor.execute(
                "INSERT INTO mesas (numero, capacidade) VALUES (?, ?)", (i, 4))
        except:
            pass  # Se a mesa já existe (erro de UNIQUE), ignora e continua
    con.commit()  # Confirma as alterações no banco
    con.close()   # Fecha a conexão
