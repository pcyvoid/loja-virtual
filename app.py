from flask import Flask, render_template, request, redirect, url_for, session
from bd import login, buscarProdutos, buscarProduto, venderProduto, estoque as bd_estoque 
import bd
import datetime

app = Flask(__name__)
app.secret_key = '123'

user = {}

@app.route('/')
def index():
    conexao = bd.criarConexao()
    if not conexao:
        return render_template('errorConnection.html', errorBD="Erro de conexão com o banco de dados")
    return render_template('login.html', e=False)

@app.route("/logar", methods=['POST'])
def logar():
    global user

    usuario = request.form["id"]
    senha = request.form["senha"]
    
    user = login(usuario, senha)
    
    if "erro" in user:
        return render_template('login.html', e=True)
    
    if user['funcao'] == 'lojista':
        return redirect("/lojista")
    elif user['funcao'] == 'Gerente':
        return redirect("/gerente")
    else:
        return "Login inválido ou usuário não encontrado"

@app.route('/lojista')
def lojista():
    session['origem'] = 'lojista'
    return render_template('lojista.html')

@app.route('/gerente')
def gerente():
    session['origem'] = 'gerente'
    return render_template('gerente.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/area/<int:area>')
def areas(area):
    produtos = buscarProdutos(area)
    print(produtos.items())
    return render_template('area.html', produtos=produtos, area=area, data=datetime.datetime.now().date())

@app.route("/venda/<int:idProduto>")
def venda(idProduto):
    produto = buscarProduto(idProduto)
    return render_template('venda.html', produto=produto, data=datetime.datetime.now().date())

@app.route("/venda/<int:idProduto>/", methods=["POST"])
def finalizarVenda(idProduto):
    quantidade = request.form["quantidade"]
    destino = request.form["destino"]

    resultado = venderProduto(idProduto, quantidade, destino)
    if resultado is True: 
        return render_template('popup.html', venda=True)
    else:
        return render_template('popup.html', venda=False)

@app.route("/estoque")
def estoque():
    relatorio_produtos = bd_estoque() 
    return render_template("estoque.html", relatorios=relatorio_produtos, date=datetime.datetime.now().date())

@app.route("/vendas")
def vendas():
    conexao = bd.criarConexao()
    if conexao is None:
        return render_template('errorConnection.html', errorBD="Erro de conexão com o banco de dados")
    
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM vendas") 
    vendas_realizadas = cursor.fetchall()
    
    lista_vendas = []
    for venda in vendas_realizadas:
        lista_vendas.append({
            "quantidadeVenda": venda[1],
            "dataHora": venda[2],
            "destino": venda[3],
            "idProduto": venda[4],
        })
    
    cursor.close()
    conexao.close()
    
    return render_template("vendas.html", vendas=lista_vendas, date=datetime.datetime.now().date())

if __name__ == '__main__':
    app.run(debug=True)
