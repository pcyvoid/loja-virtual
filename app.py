from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from bd import login, listarProdutos, adicionarProduto
import bd


app = Flask(__name__)
app.secret_key = '123'


user = {}


@app.route('/')
def index():
    conexao = bd.criarConexao()
    if not conexao:
        return render_template('errorConnection.html', errorBD="Erro de conexão com o banco de dados")
    return render_template('login.html', e=False)


def criarConexao():
    return mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='',
        database='superselect'
    )


@app.route("/logar", methods=['POST'])
def logar():
    global user


    usuario = request.form["id"]
    senha = request.form["senha"]
   
    user = login(usuario, senha)
   
    if "erro" in user:
        return render_template('login.html', e=True)
   
    if user['tipo'] == 'Comum':
        return redirect("/comum")
    elif user['tipo'] == 'Gerente':
        return redirect("/gerente")
    else:
        return "Login inválido ou usuário não encontrado"


@app.route('/comum')
def comum():
    session['origem'] = 'Comum'
    conexao = criarConexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    produtos = listarProdutos()
    return render_template('comum.html', produtos=produtos)


@app.route('/gerente')
def gerente():
    session['origem'] = 'Gerente'
    conexao = criarConexao()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM produtos")
    produtos = listarProdutos()
    return render_template('gerente.html', produtos=produtos)


@app.route('/gerente/adicionar')
def adicionarProduto():
    return render_template('adicionar.html')
    
@app.route('/gerente/adicionar/final', methods=['POST'])
def novoProduto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    categoria = request.form['categoria']
    preco = request.form['preco']
    validade = request.form['validade']
    
    bd.adicionarProduto(nome, descricao, categoria, preco, validade)

    return redirect(url_for('gerente'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
