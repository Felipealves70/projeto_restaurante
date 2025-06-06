import sqlite3
import csv
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Função para exportar os dados da tabela reservas para um arquivo CSV


def exportar_csv(conteudo_frame=None):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('restaurante.db')
        cursor = conn.cursor()

        # Buscar todos os dados da tabela reservas
        cursor.execute("SELECT * FROM reservas")
        colunas = [desc[0]
                   # Obtém os nomes das colunas
                   for desc in cursor.description]
        dados = cursor.fetchall()  # Obtém todas as linhas dos dados
        totalReservas = len(dados)  # Conta o total de reservas encontradas
        conn.close()

        # Abre uma janela para o usuário escolher onde salvar o arquivo CSV
        caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivo CSV", "*.csv")],
            title="Salvar como"
        )

        if not caminho_arquivo:
            return  # Usuário cancelou o salvamento

        # Abre/cria o arquivo CSV no caminho escolhido e escreve os dados
        with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            # Escreve a primeira linha com os nomes das colunas
            escritor.writerow(colunas)
            # Escreve todas as linhas de dados
            escritor.writerows(dados)

            escritor.writerow([])              # Insere uma linha em branco
            # Escreve o total de reservas no final
            escritor.writerow(["Total de Reservas", f" {totalReservas}"])

        # Exibe uma mensagem informando que a exportação foi concluída
        messagebox.showinfo("Exportação Concluída",
                            f"Arquivo salvo em:\n{caminho_arquivo}")

    except Exception as e:
        # Exibe uma mensagem de erro caso algo dê errado
        messagebox.showerror("Erro", f"Ocorreu um erro ao exportar:\n{str(e)}")
