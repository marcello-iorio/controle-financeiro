from flask import Flask, request, jsonify
from db import get_connection

app = Flask(__name__)

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

    cursor.execute("SELECT * FROM movimentacoes ORDER BY data DESC")
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


if __name__ == "__main__":
    app.run(debug=True)


