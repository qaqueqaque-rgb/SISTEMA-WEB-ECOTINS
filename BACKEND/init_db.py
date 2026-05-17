import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'ecotins.db')

def configurar_banco():
    conn = sqlite3.connect('ecotins.db')
    cursor = conn.cursor()

    print("Configurando banco de dados com níveis de acesso...")

    # 1. Tabela de Usuários atualizada com a coluna 'tipo'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'comum' -- 'comum' ou 'admin'
        )
    ''')

    # 2. Tabela de Solicitações Ativas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            tipo_residuo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data_pedido TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Aguardando Coleta',
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')

    # 3. Tabela de Solicitações Excluídas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes_excluidas (
            id INTEGER PRIMARY KEY,
            usuario_id INTEGER,
            tipo_residuo TEXT,
            descricao TEXT,
            data_pedido TEXT,
            data_exclusao TEXT,
            status TEXT
        )
    ''')

    # 4. Criar um Administrador Padrão automaticamente para testes
    try:
        # Se o admin já existir, o UNIQUE do email vai dar erro e o try ignora
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, tipo) 
            VALUES ('Administrador EcoTins', 'admin@ecotins.com', 'admin123', 'admin')
        ''')
        print("-> Usuário Administrador criado com sucesso!")
        print("   E-mail: admin@ecotins.com | Senha: admin123")
    except sqlite3.IntegrityError:
        print("-> O usuário Administrador já estava cadastrado.")

    conn.commit()
    conn.close()
    print("Sucesso: Banco de dados EcoTins totalmente atualizado!")

if __name__ == '__main__':
    configurar_banco()