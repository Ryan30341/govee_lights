"""
Main web server for Govee Lights Controller
"""
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import os

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    """Main web interface"""
    return render_template('index.html')

@app.route('/api/lights', methods=['GET'])
def get_lights():
    """Get list of available lights"""
    # TODO: Implement Govee API integration
    return jsonify({
        'lights': [],
        'status': 'success'
    })

@app.route('/api/lights/<light_id>/control', methods=['POST'])
def control_light(light_id):
    """Control a specific light"""
    # TODO: Implement light control
    return jsonify({
        'status': 'success',
        'light_id': light_id
    })

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('Client connected')
    socketio.emit('status', {'message': 'Connected to Govee Lights Controller'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)

