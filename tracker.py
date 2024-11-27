from flask import Flask, request, jsonify

app = Flask(__name__)

file_registry = {}  # {file_hash: {piece_index: [list of (peer_ip, peer_port)]}}

@app.route('/announce', methods=['POST'])
def announce():
    data = request.json
    file_hash = data['file_hash']
    piece_index = data['piece_index']
    peer_info = (data['ip'], data['port'])
    if file_hash not in file_registry:
        file_registry[file_hash] = {}
    if piece_index not in file_registry[file_hash]:
        file_registry[file_hash][piece_index] = []
    file_registry[file_hash][piece_index].append(peer_info)
    return jsonify({"status": "success"}), 200

@app.route('/get_peers', methods=['GET'])
def get_peers():
    file_hash = request.args.get('file_hash')
    piece_index = int(request.args.get('piece_index'))
    peers = file_registry.get(file_hash, {}).get(piece_index, [])
    return jsonify({"peers": peers}), 200

if __name__ == '__main__':
    app.run(port=8080)
