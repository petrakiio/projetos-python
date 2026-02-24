from flask import Flask, jsonify, request
import requests


def open_server():
    app = Flask(__name__)

    @app.route("/ip", methods=["POST"])
    def receber_ip():
        data = request.get_json(silent=True) or {}
        mensagem = data.get("mensagem", "")
        origem = data.get("origem", "desconhecida")
        return jsonify(
            {"status": "ok", "recebido": mensagem, "origem": origem}
        ), 200

    app.run(host="localhost", debug=True, port=5000)


