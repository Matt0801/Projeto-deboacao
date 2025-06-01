from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

client = OpenAI(api_key="minha_key")

@app.route('/chat', methods=['POST'])
def chat():
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
