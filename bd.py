import mysql.connector
from mysql.connector import errors
from datetime import datetime

def criarConexao():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password="",
            database="fabrica"
        )
        return conexao
    except errors.InterfaceError as error: 
        print("Erro de integridade: ", error)
        return None

def login(usuario, senha):
    conexao = criarConexao()
    if conexao is None:
        return {"erro": "Erro de conexão"}
    
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM usuarios WHERE idUsuarios = %s AND senha = %s;", (usuario, senha))
    resultado = cursor.fetchall()

    usuario_info = {}

    if len(resultado) > 0:
        usuario_info = {
            'id': resultado[0][0],
            'nome': resultado[0][1],
            'funcao': resultado[0][2],
            'senha': resultado[0][3]
        }
    else:
        usuario_info["erro"] = "Usuário não encontrado"
    
    cursor.close()
    conexao.close()
    return usuario_info

def buscarProdutos(area):
    conexao = criarConexao()
    if conexao is None:
        return {"erro": "Erro de conexão"}
    
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM produtos WHERE area = %s", (area,))
    resultado = cursor.fetchall()

    produtos = {}
    if len(resultado) > 0:
        for i in range(len(resultado)):
            produtos[resultado[i][0]] = {
                "nome": resultado[i][1],
                "quantidade": resultado[i][2],
                "lote": resultado[i][3],
                "data": resultado[i][4],
            }

    for i, produto in produtos.items():
        data_produto = produto["data"]
        diferenca = (data_produto - datetime.now().date()).days
        produto["classe_alerta"] = 'bg-red-300' if diferenca < 30 else 'bg-white'
    
    cursor.close()
    conexao.close()
    return produtos

def buscarProduto(idProduto):
    conexao = criarConexao()
    if conexao is None:
        return {"erro": "Erro de conexão"}
    
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos WHERE idProdutos = %s", (idProduto,))
    resultado = cursor.fetchone()

    produto = {}
    if resultado:
        produto = {
            "idProduto": resultado[0],
            "nome": resultado[1],
            "quantidade": resultado[2],
            "lote": resultado[3],
            "data": resultado[4],
            "area": resultado[5],
        }
    else:
        produto = {"erro": "Produto não encontrado"}

    cursor.close()
    conexao.close()
    return produto

def venderProduto(idProduto, quantidade, destino):
    conexao = criarConexao()
    if conexao is None:
        return {"erro": "Erro de conexão"}

    cursor = conexao.cursor()

    try:
        cursor.execute(f"SELECT quantidade FROM produtos WHERE idProdutos = {idProduto}")
        resultado = cursor.fetchall()

        if not resultado:
            return {"erro": "Produto não encontrado"}

        quantidade_disponivel = resultado[0][0]

        if int(quantidade) > quantidade_disponivel:
            return {"erro": "Quantidade insuficiente!"}

        cursor.execute(
            f"INSERT INTO vendas (quantidadeVenda, dataHora, destino, idProdutos) "
            f"VALUES ({quantidade}, NOW(), '{destino}', {idProduto})"
        )

        cursor.execute(
            f"UPDATE produtos SET quantidade = quantidade - {quantidade} WHERE idProdutos = {idProduto}"
        )

        conexao.commit()

        return True

    except Exception as e:
        return {"erro": str(e)}

    finally:
        cursor.close()
        conexao.close()


def estoque():
    conexao = criarConexao()
    if conexao is None:
        return {"erro": "Erro de conexão"}
    
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos") 
    result = cursor.fetchall()
    estoque = {}

    if len(result) > 0:
        for i in range(len(result)):
            estoque[result[i][0]] = {
                "nome": result[i][1],
                "quantidade": result[i][2],
                "lote": result[i][3],
                "data": result[i][4],
                "area": result[i][5],
            }
    else:
        estoque = {"error": True}

    cursor.close()
    conexao.close()

    return estoque
