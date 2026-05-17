from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, template_folder='../web', static_folder='../web')
app.secret_key = 'unitins_tads_ecotins'

# Função auxiliar para conectar ao banco de dados SQLite

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'ecotins.db')

def conectar_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# ROTAS DE ACESSO LIVRE
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pontos')
def pontos():
    return render_template('pontosdecoleta.html')

# ==========================================
# AUTENTICAÇÃO (LOGIN / CADASTRO / SAIR)
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    email_preenchido = ""
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        conn = conectar_db()
        user = conn.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['nome']
            session['user_tipo'] = user['tipo']  # 'admin' ou 'user'
            
            if user['tipo'] == 'admin':
                return redirect(url_for('admin_dashboard'))
                
            return redirect(url_for('index'))
        else:
            flash("E-mail ou senha incorretos!")
            email_preenchido = email
            
    return render_template('login.html', email_preenchido=email_preenchido)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        try:
            conn = conectar_db()
            conn.execute('INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, "user")', (nome, email, senha))
            conn.commit()
            conn.close()
            
            flash("Conta criada com sucesso! Faça login")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Este e-mail já está cadastrado no sistema.")
            
    return render_template('cadastro.html')

@app.route('/sair')
def sair():
    session.clear()
    return redirect(url_for('index'))

# ==========================================
# ROTAS DO USUÁRIO COMUM
# ==========================================
@app.route('/solicitar', methods=['GET', 'POST'])
def solicitar():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        tipo = request.form['tipo']
        descricao = request.form['descricao']
        data_atual = datetime.now().strftime('%d/%m/%Y')
        user_id = session['user_id']
        
        conn = conectar_db()
        conn.execute('''
            INSERT INTO solicitacoes (usuario_id, tipo_residuo, descricao, data_pedido) 
            VALUES (?, ?, ?, ?)
        ''', (user_id, tipo, descricao, data_atual))
        conn.commit()
        conn.close()
        
        flash("Solicitação enviada! Acompanhe em Minhas solicitações")
        return redirect(url_for('solicitacoes'))
        
    return render_template('solicitar.html')

@app.route('/solicitacoes')
def solicitacoes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    conn = conectar_db()
    pedidos = conn.execute('SELECT * FROM solicitacoes WHERE usuario_id = ? ORDER BY id DESC', (user_id,)).fetchall()
    conn.close()
    return render_template('solicitacoes.html', pedidos=pedidos)

@app.route('/solicitacoes/excluir', methods=['POST'])
def excluir_solicitacao():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    id_pedido = request.form.get('id_solicitacao')
    
    if not id_pedido:
        return redirect(url_for('solicitacoes'))

    data_exclusao = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    conn = conectar_db()
    pedido = conn.execute('SELECT * FROM solicitacoes WHERE id = ? AND usuario_id = ?', (id_pedido, user_id)).fetchone()
    
    if pedido:
        conn.execute('''
            INSERT INTO solicitacoes_excluidas (id, usuario_id, tipo_residuo, descricao, data_pedido, data_exclusao, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (pedido['id'], pedido['usuario_id'], pedido['tipo_residuo'], pedido['descricao'], pedido['data_pedido'], data_exclusao, pedido['status']))
        
        conn.execute('DELETE FROM solicitacoes WHERE id = ?', (id_pedido,))
        conn.commit()
        flash("Solicitação excluída com sucesso!")
    
    conn.close()
    return redirect(url_for('solicitacoes'))

# ==========================================================================
# PAINEL DO ADMINISTRADOR CENTRALIZADO
# ==========================================================================

@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if session.get('user_tipo') != 'admin':
        flash("Acesso Negado: Esta área é restrita para administradores.")
        return redirect(url_for('index'))
        
    conn = conectar_db()
    conn.row_factory = sqlite3.Row
    
    solicitacoes_ativas = conn.execute('SELECT * FROM solicitacoes ORDER BY id DESC').fetchall()
    usuarios = conn.execute('SELECT id, nome, email, tipo FROM usuarios ORDER BY id DESC').fetchall()
    excluidos = conn.execute('SELECT * FROM solicitacoes_excluidas ORDER BY data_exclusao DESC').fetchall()
    
    total_usuarios = len(usuarios)
    total_ativas = len(solicitacoes_ativas)
    total_excluidas = len(excluidos)
    
    conn.close()
    
    return render_template('admin.html', 
                           solicitacoes=solicitacoes_ativas, 
                           usuarios=usuarios, 
                           excluidos=excluidos,
                           total_usuarios=total_usuarios,
                           total_ativas=total_ativas,
                           total_excluidas=total_excluidas)

# API rápida para o JavaScript buscar os dados do usuário para editar sem mudar de página
@app.route('/admin/usuarios/dados/<int:id>')
def admin_dados_usuario(id):
    if 'user_id' not in session or session.get('user_tipo') != 'admin':
        return jsonify({"erro": "Não autorizado"}), 403
    
    conn = conectar_db()
    usuario = conn.execute('SELECT id, nome, email, tipo FROM usuarios WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if usuario:
        return jsonify(dict(usuario))
    return jsonify({"erro": "Usuário não encontrado"}), 404

# AÇÃO DO ADMIN: Salvar alteração de dados e privilégios (Altera para admin/user)
@app.route('/admin/usuarios/salvar', methods=['POST'])
def admin_salvar_usuario():
    if 'user_id' not in session or session.get('user_tipo') != 'admin':
        return redirect(url_for('login'))
        
    id_usuario = request.form.get('id_usuario')
    nome = request.form['nome']
    email = request.form['email']
    tipo = request.form['tipo'] # Recebe 'admin' ou 'user' do select
    
    conn = conectar_db()
    try:
        conn.execute('UPDATE usuarios SET nome = ?, email = ?, tipo = ? WHERE id = ?', (nome, email, id_usuario))
        conn.commit()
        flash("Usuário atualizado com sucesso!")
    except sqlite3.IntegrityError:
        flash("Erro: Este e-mail já está em uso por outro usuário.")
    finally:
        conn.close()
        
    return redirect(url_for('admin_dashboard'))

# AÇÃO DO ADMIN: Excluir Usuário direto pelo Dashboard
@app.route('/admin/usuarios/excluir', methods=['POST'])
def admin_excluir_usuario():
    if 'user_id' not in session or session.get('user_tipo') != 'admin':
        return redirect(url_for('login'))
        
    id_usuario = request.form.get('id_usuario')
    
    if id_usuario:
        conn = conectar_db()
        conn.execute('DELETE FROM usuarios WHERE id = ?', (id_usuario,))
        conn.commit()
        conn.close()
        flash("Usuário removido com sucesso!")
        
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)