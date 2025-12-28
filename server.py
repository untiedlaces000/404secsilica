from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Storage: { "RoomName": {"peers": ["peerId1", "peerId2"]} }
rooms_db = {}

@app.route('/rooms', methods=['GET', 'POST'])
def handle_rooms():
    if request.method == 'POST':
        data = request.json
        room_name = data.get("room", "Unnamed Room")
        peer_id = data.get("peerId")
        
        if room_name not in rooms_db:
            rooms_db[room_name] = {"peers": []}
        
        if peer_id and peer_id not in rooms_db[room_name]["peers"]:
            rooms_db[room_name]["peers"].append(peer_id)
        
        print(f"✅ Created/Updated Room: {room_name}")
        return jsonify({"name": room_name}), 201
    
    # GET: return room names as list of strings
    return jsonify(list(rooms_db.keys()))

@app.route('/rooms/<room_name>/join', methods=['POST'])
def join_room(room_name):
    data = request.json
    peer_id = data.get("peerId")
    
    if room_name not in rooms_db:
        return jsonify({"error": "Room not found"}), 404
    
    if peer_id and peer_id not in rooms_db[room_name]["peers"]:
        rooms_db[room_name]["peers"].append(peer_id)
    
    print(f"👤 {peer_id} joined room: {room_name}")
    return jsonify({"name": room_name}), 200

@app.route('/rooms/<room_name>/peers', methods=['GET'])
def get_peers(room_name):
    if room_name not in rooms_db:
        return jsonify([])
    return jsonify(rooms_db[room_name]["peers"])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)
