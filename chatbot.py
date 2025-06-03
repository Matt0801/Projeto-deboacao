import os
from flask import Flask, request, jsonify
from flask import abort
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://deboaacao.vercel.app"])

client = OpenAI(api_key=os.getenv("key"))

key = os.getenv("key") #colocado no render

@app.route('/chat', methods=['POST'])
def chat():
    origin = request.headers.get('Origin')
    if origin != "https://deboaacao.vercel.app":
        abort(403)
        
    token = request.headers.get('Authorization')

    if token != f"Bearer {key}":
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    user_input = data.get('message')

    mensagens = [
        {"role": "system", "content": "Você é um assistente simpático e informativo de uma ONG que ajuda comunidades carentes."},
        {"role": "user", "content": user_input}
    ]

    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=mensagens
        )
        reply = resposta.choices[0].message.content
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f'Erro: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
