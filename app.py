from flask import Flask, render_template, request, redirect, url_for
from bd import login 

app = Flask(__name__)
user = {}

@app.route('/')
def index():
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
        return ("Login inválido ou usuário não encontrado")

@app.route('/lojista')
def lojista():
    return render_template('lojista.html')

@app.route('/gerente')
def gerente():
    return render_template('gerente.html')

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/area/<int:area>')
def areas(area):
    

if __name__ == '__main__':
    app.run(debug=True)
