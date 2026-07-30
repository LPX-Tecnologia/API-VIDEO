from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_FILE = 'videos.json'

def carregar():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar(dados):
    with open(DB_FILE, 'w') as f:
        json.dump(dados, f)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"api": "Clipador - Vídeos", "versao": "1.0.0"})

@app.route('/api/videos', methods=['GET'])
def listar():
    return jsonify(carregar())

@app.route('/api/videos', methods=['POST'])
def upload():
    data = request.json
    videos = carregar()
    
    video = {
        "id": len(videos) + 1,
        "url": data.get('url'),
        "titulo": data.get('titulo'),
        "legenda": data.get('legenda', ''),
        "estilo": data.get('estilo', 'padrao'),
        "status": "processando",
        "criado_em": str(datetime.now())
    }
    videos.append(video)
    salvar(videos)
    return jsonify(video), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))
    app.run(host='0.0.0.0', port=port)