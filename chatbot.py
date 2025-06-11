import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, origins=["https://deboaacao.vercel.app"])

api_key = os.getenv("API_KEY")
acess_key = os.getenv("key")

@app.route('/chat', methods=['POST'])
def chat():
    origin = request.headers.get('Origin')
    origens_permitidas = [
        "https://deboaacao.vercel.app",
        "https://deboaacao.vercel.app/",
        None
    ]

    if origin not in origens_permitidas:
        abort(403)
    
    token = request.headers.get('Authorization')
    if token != f"Bearer {acess_key}":
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    user_input = data.get('message')

    mensagens = [
        {"role": "system", "content": "Você é um assistente simpático e informativo de uma ONG que ajuda comunidades carentes."},
        {"role": "user", "content": user_input}
    ]

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
                "messages": mensagens
            }
        )
        response.raise_for_status()
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f'Erro: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
