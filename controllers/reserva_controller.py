# Importa os módulos de manipulação de cliente, mesa e reserva do diretório 'models'
import models.cliente as cliente
import models.mesa as mesa
import models.reserva as reserva

# Função para processar uma nova reserva


def processar_reserva(nome, telefone, email, data, horario, mesa_nome):
    # Obtém todas as mesas do banco
    mesas = mesa.listar_mesas()

    # Cria um dicionário para mapear o nome da mesa ("Mesa 1", "Mesa 2", etc.) para seu ID
    mesa_dict = {f"Mesa {num}": mid for mid, num in mesas}

    # Obtém o ID da mesa selecionada
    mesa_id = mesa_dict.get(mesa_nome)

    # Se a mesa não existir no dicionário (nome inválido), retorna False
    if mesa_id is None:
        return False  # Mesa inválida

    # Verifica se a mesa está disponível na data e horário desejados
    if not reserva.verificar_disponibilidade(mesa_id, data, horario):
        return False  # Não disponível

    # Adiciona o cliente ao banco de dados e obtém seu ID
    cliente_id = cliente.adicionar_cliente(nome, telefone, email)

    # Faz a reserva com os dados do cliente, mesa, data e horário
    return reserva.fazer_reserva(cliente_id, mesa_id, data, horario)

# Função para obter a lista de mesas em formato de texto para exibir em um ComboBox (ex: "Mesa 1", "Mesa 2")


def get_mesas_para_combobox():
    mesas = mesa.listar_mesas()
    return [f"Mesa {num}" for _, num in mesas]

# Função para obter todas as reservas registradas


def get_reservas():
    return reserva.listar_reservas()

# Função para editar uma reserva existente


def editar_reserva(reserva_id, nova_data, novo_horario, nova_mesa_nome):
    # Obtém todas as mesas e cria um dicionário de nome para ID
    mesas = mesa.listar_mesas()
    mesa_dict = {f"Mesa {num}": mid for mid, num in mesas}
    mesa_id = mesa_dict.get(nova_mesa_nome)

    # Verifica se a nova mesa está disponível na nova data e horário
    if reserva.verificar_disponibilidade(mesa_id, nova_data, novo_horario):
        # Atualiza a reserva com os novos dados
        reserva.atualizar_reserva(reserva_id, nova_data, novo_horario, mesa_id)
        return True  # Sucesso
    return False  # Horário/mesa não disponíveis

# Função para cancelar/excluir uma reserva pelo ID


def excluir_reserva(reserva_id):
    reserva.cancelar_reserva(reserva_id)
