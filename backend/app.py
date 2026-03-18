from flask import Flask, request, jsonify
from db import get_connection
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "API Controle Financeiro funcionando"

@app.route("/movimentacoes", methods=["POST"])
def criar_movimentacao():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO movimentacoes (tipo, valor, data, descricao, categoria_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        data["tipo"],
        data["valor"],
        data["data"],
        data.get("descricao"),
        data.get("categoria_id")
    )

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"status": "ok"}), 201

@app.route("/movimentacoes", methods=["GET"])
def listar_movimentacoes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT m.*, c.nome as categoria FROM movimentacoes m LEFT JOIN categorias c ON m.categoria_id = c.id")
    movimentacoes = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(movimentacoes)

@app.route("/saldo", methods=["GET"])
def calcular_saldo():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            SUM(CASE WHEN tipo = 'entrada' THEN valor ELSE 0 END) -
            SUM(CASE WHEN tipo = 'saida' THEN valor ELSE 0 END)
        AS saldo
        FROM movimentacoes
    """)

    resultado = cursor.fetchone()
    saldo = resultado[0] if resultado[0] is not None else 0

    cursor.close()
    conn.close()

    return jsonify({"saldo": float(saldo)})

@app.route("/categorias", methods=["POST"])
def criar_categoria():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO categorias (nome) VALUES (%s)",
        (data["nome"],)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "ok"}), 201

@app.route("/categorias", methods=["GET"])
def listar_categorias():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(categorias)

@app.route("/movimentacoes/<int:id>", methods=["PUT"])
def atualizar_movimentacao(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE movimentacoes
        SET tipo = %s,
            valor = %s,
            data = %s,
            descricao = %s,
            categoria_id = %s
        WHERE id = %s
    """

    cursor.execute(sql, (
        data["tipo"],
        data["valor"],
        data["data"],
        data["descricao"],
        data["categoria_id"],
        id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"status": "atualizado"})

if __name__ == "__main__":
    app.run(debug=True)


