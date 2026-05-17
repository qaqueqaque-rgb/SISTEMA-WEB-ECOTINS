🌱 EcoTins - Sistema Web de Coleta de Resíduos

Sistema web desenvolvido para gerenciamento de solicitações de coleta de resíduos recicláveis, criado para projeto acadêmico do curso de Tecnologia em Análise e Desenvolvimento de Sistemas (TADS).

📌 Objetivo do Sistema

O EcoTins tem como objetivo facilitar o gerenciamento de:

Solicitações de coleta de resíduos
Cadastro de usuários
Controle administrativo
Acompanhamento das solicitações
Organização de resíduos recicláveis
🛠️ Tecnologias Utilizadas
Backend
Python
Flask
SQLite
Frontend
HTML5
CSS3
JavaScript
📂 Estrutura do Projeto
SISTEMA_WEB_ECOTINS/
│
├── BACKEND/
│   ├── app.py
│   ├── init_db.py
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
⚙️ Como Executar o Sistema
1. Instalar o Python

Download:

https://www.python.org/downloads/ (sugiro versão 3.12 por maior compatibilidade)

2. Instalar as Dependências

Abra o terminal na pasta BACKEND:

cd BACKEND

Depois execute:

pip install flask
3. Inicializar o Banco de Dados

Ainda dentro da pasta BACKEND execute:

python init_db.py

Esse comando irá:

Criar o banco SQLite
Criar as tabelas
Criar o usuário administrador padrão
⚠️ IMPORTANTE

O terminal PRECISA estar dentro da pasta BACKEND antes de executar:

python init_db.py

Exemplo correto:

cd BACKEND
python init_db.py

Caso contrário, o SQLite pode criar o banco de dados na pasta errada, causando erros como:

sqlite3.OperationalError: no such table: usuarios
4. Executar o Sistema

Ainda dentro da pasta BACKEND execute:

python app.py
🌐 Acesso ao Sistema

Após executar o sistema, abra:

http://127.0.0.1:5000
👤 Usuário Administrador

O sistema cria automaticamente um administrador padrão:

Login:
admin@ecotins.com
Senha:
admin123
📋 Funcionalidades do Sistema
Usuário Comum
Cadastro
Login
Solicitar coleta
Visualizar solicitações
Excluir solicitações
Administrador
Visualizar usuários
Editar usuários
Excluir usuários
Visualizar solicitações
Painel administrativo
🗄️ Banco de Dados

O sistema utiliza SQLite.

Arquivo:

ecotins.db

Tabelas:

usuarios
solicitacoes
solicitacoes_excluidas
🔐 Sistema de Sessão

O sistema utiliza sessão Flask para:

Controle de login
Controle administrativo
Proteção de páginas
🚀 Melhorias Futuras
Upload de imagens
Integração com mapas
API REST
Dashboard com gráficos
Responsividade mobile
Criptografia de senhas
Deploy em nuvem
👨‍💻 Desenvolvido por

Projeto acadêmico desenvolvido para o curso de Tecnologia em Análise e Desenvolvimento de Sistemas (TADS).

📄 Licença

Projeto acadêmico para fins educacionais.