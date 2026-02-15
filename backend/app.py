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

if __name__ == "__main__":
    app.run(debug=True)


