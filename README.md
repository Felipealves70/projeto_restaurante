# Sistema de Gerenciamento de Reservas de Restaurante

Este é um sistema desenvolvido em Python para o gerenciamento de reservas em um restaurante temático. O projeto foi estruturado seguindo o padrão MVC (Model-View-Controller), com separação clara das responsabilidades e uso de banco de dados SQLite.

## 🧾 Funcionalidades

- Cadastro de clientes
- Criação de reservas
- Edição e exclusão de reservas e clientes
- Login de acesso
- Interface gráfica com Custom Tkinter

## 🛠️ Tecnologias Utilizadas

- Python 3
- Custom Tkinter (interface gráfica)
- SQLite (banco de dados local)
- Padrão MVC

## 📁 Estrutura do Projeto

```
├── restaurante/
│   ├── main.py                  # Arquivo principal para executar o sistema
│   ├── restaurante.db           # Banco de dados SQLite
│   ├── controllers/             # Lógica de controle (clientes e reservas)
│   ├── models/                  # Modelos (Cliente, Mesa, Reserva, Admin)
│   └── database/                # Conexão com o banco de dados
└── README.md
```

## ▶️ Como Executar o Projeto

1. **Clone o repositório ou extraia o ZIP**
   ```bash
   git clone <url-do-repositorio>
   ```

2. **Acesse a pasta do projeto**
   ```bash
   cd restaurante-att_carlos/restaurante
   ```

3. **Instale os requisitos**
   - Para Windows: 
      ```bash
      pip install customtkinter, tkcalendar, pillow
      ```

   - Para Linux (caso necessário):
     ```bash
      pip install pillow customtkinter tkcalendar
     ```

4. **Execute o sistema**
   ```bash
   python main.py
   ```

## 🔐 Login de Administrador

Ao iniciar o sistema, será necessário efetuar login como administrador. 

para acessar use esse acesso:

   usuário: adm senha: 123

## 📌 Observações

- O banco de dados (`restaurante.db`) já está incluído com dados de exemplo.
- Este projeto foi desenvolvido para fins educacionais e pode ser expandido com mais funcionalidades, como confirmação por e-mail, reservas online, etc.

## 👨‍💻 Autores

Carlos Henrique, Luan Brito, Felipe Alves(projeto acadêmico)

---

Sinta-se à vontade para adaptar, melhorar ou contribuir com o projeto!
