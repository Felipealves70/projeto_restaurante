# Importa o módulo 'cliente' que está localizado no diretório 'models'
import models.cliente as cliente

# Função para obter a lista de todos os clientes


def get_clientes():
    # Chama a função 'listar_clientes' do módulo 'cliente' e retorna o resultado
    return cliente.listar_clientes()

# Função para editar os dados de um cliente


def editar_cliente(cliente_id, nome, telefone, email):
    # Chama a função 'atualizar_cliente' do módulo 'cliente', passando os novos dados
    cliente.atualizar_cliente(cliente_id, nome, telefone, email)

# Função para remover um cliente do sistema


def remover_cliente(cliente_id):
    # Chama a função 'excluir_cliente' do módulo 'cliente', passando o ID do cliente que será removido
    cliente.excluir_cliente(cliente_id)
