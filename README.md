# SISTEMA-WEB-ECOTINS
Sistema WEB para empresa ECOTINS - seminário tech 2026-1

EcoTins - Sistema Web de Coleta de Resíduos

Sistema web desenvolvido para gerenciamento de solicitações de coleta de resíduos recicláveis, criado para projeto acadêmico do curso de Tecnologia em Análise e Desenvolvimento de Sistemas (TADS).

OBJETIVO DO SISTEMA

O EcoTins tem como objetivo facilitar o gerenciamento de:

- Solicitações de coleta de resíduos
- Cadastro de usuários
- Controle administrativo
- Acompanhamento das solicitações
- Organização de resíduos recicláveis

TECNOLOGIAS UTILIZADAS

Backend
- Python
- Flask
- SQLite

Frontend
- HTML5
- CSS3
- JavaScript

ESTRUTURA DO PROJETO

SISTEMA_WEB_ECOTINS/
│
├── BACKEND/
│   ├── app.py
│   ├── init_db.py
│   ├── requirements.txt
│   ├── ecotins.db
│
├── WEB/
│   ├── index.html
│   ├── login.html
│   ├── cadastro.html
│   ├── solicitar.html
│   ├── admin.html
│   └── ...
│
└── README.md

COMO EXECUTAR O SISTEMA

1. Instalar o Python

Download:
https://www.python.org/downloads/ (recomendável a instalação 3.12 por maior compatibilidade)

2. Instalar as Dependências

Abra o terminal na pasta BACKEND:

cd BACKEND (se não tiver aberto na pasta do backend) (as vezes no termiinal fica a parte geral do sistema e não a parte do backend)

Instale todas as dependências do projeto usando:

pip install -r requirements.txt

OBSERVAÇÃO

O arquivo requirements.txt instala automaticamente:

- Flask
- Flask Login
- Flask SQLAlchemy

Caso queira instalar manualmente:

pip install flask
pip install flask-login
pip install flask-sqlalchemy

3. Inicializar o Banco de Dados

Ainda dentro da pasta BACKEND execute:

python init_db.py

Esse comando irá:

- Criar o banco SQLite
- Criar as tabelas
- Criar o usuário administrador padrão

IMPORTANTE

O terminal PRECISA estar dentro da pasta BACKEND (conforme foi informado acima) antes de executar:

python init_db.py

Exemplo correto:

cd BACKEND
python init_db.py

Caso contrário, o SQLite pode criar o banco de dados na pasta errada, causando erros como:

sqlite3.OperationalError: no such table: usuarios

4. Executar o Sistema

Ainda dentro da pasta BACKEND execute:

python app.py

ACESSO AO SISTEMA

Após executar o sistema, abra:

http://127.0.0.1:5000

USUÁRIO ADMINISTRADOR

O sistema cria automaticamente um administrador padrão:

Login:
admin@ecotins.com

Senha:
admin123

FUNCIONALIDADES DO SISTEMA

Usuário Comum
- Cadastro
- Login
- Solicitar coleta
- Visualizar solicitações
- Excluir solicitações

Administrador
- Visualizar usuários
- Editar usuários
- Excluir usuários
- Visualizar solicitações
- Painel administrativo

BANCO DE DADOS

O sistema utiliza SQLite.

Arquivo:
ecotins.db

Tabelas:
- usuarios
- solicitacoes
- solicitacoes_excluidas

SISTEMA DE SESSÃO

O sistema utiliza sessão Flask para:

- Controle de login
- Controle administrativo
- Proteção de páginas

MELHORIAS FUTURAS

- Upload de imagens
- Integração com mapas
- API REST
- Dashboard com gráficos
- Responsividade mobile
- Criptografia de senhas
- Deploy em nuvem

DESENVOLVIDO POR

Projeto acadêmico desenvolvido para o curso de Tecnologia em Análise e Desenvolvimento de Sistemas (TADS).

LICENÇA

Projeto acadêmico para fins educacionais.
