import database.db as banco

# Verifica se uma mesa está disponível em uma data e horário específicos


def verificar_disponibilidade(mesa_id, data, horario):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute(
        "SELECT * FROM reservas WHERE mesa_id=? AND data=? AND horario=?", (mesa_id, data, horario))
    # Busca se já existe uma reserva para essa mesa, data e horário
    resultado = cursor.fetchone()
    con.close()
    return resultado is None  # Retorna True se não houver reserva, ou seja, está disponível

# Cria uma nova reserva caso a mesa esteja disponível na data e horário informados


def fazer_reserva(cliente_id, mesa_id, data, horario):
    if verificar_disponibilidade(mesa_id, data, horario):
        con = banco.conectar()
        cursor = con.cursor()
        cursor.execute("INSERT INTO reservas (cliente_id, mesa_id, data, horario) VALUES (?, ?, ?, ?)",
                       (cliente_id, mesa_id, data, horario))
        con.commit()
        con.close()
        return True  # Reserva feita com sucesso
    return False  # Reserva não feita porque mesa não está disponível

# Lista todas as reservas com dados do cliente e da mesa, ordenando por data e horário


def listar_reservas():
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("""
        SELECT reservas.id, clientes.nome, mesas.numero, mesas.capacidade, reservas.data, reservas.horario
        FROM reservas
        JOIN clientes ON reservas.cliente_id = clientes.id
        JOIN mesas ON reservas.mesa_id = mesas.id
        ORDER BY reservas.data, reservas.horario
    """)
    resultado = cursor.fetchall()  # Retorna lista de todas as reservas com detalhes
    con.close()
    return resultado

# Atualiza os dados de uma reserva específica (data, horário e mesa)


def atualizar_reserva(reserva_id, data, horario, mesa_id):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("UPDATE reservas SET data=?, horario=?, mesa_id=? WHERE id=?",
                   (data, horario, mesa_id, reserva_id))
    con.commit()
    con.close()

# Cancela (exclui) uma reserva com base no ID


def cancelar_reserva(reserva_id):
    con = banco.conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM reservas WHERE id = ?", (reserva_id,))
    con.commit()
    con.close()
