import os
import json
from datetime import datetime
from flask import Flask, render_template, request, url_for
from flask_socketio import SocketIO, emit
import threading

# Вказуємо правильні шляхи до папок зі статичними файлами та шаблонами
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, static_folder=static_path, template_folder=template_path)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

if not os.path.exists('storage'):
    os.makedirs('storage')
if not os.path.exists('storage/data.json'):
    with open('storage/data.json', 'w') as f:
        json.dump({}, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message.html')
def message():
    return render_template('message.html')

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    new_data = {now: {'username': username, 'message': message}}
    with open('storage/data.json', 'r+') as f:
        stored_data = json.load(f)
        stored_data.update(new_data)
        f.seek(0)
        json.dump(stored_data, f)
    emit('message', new_data, broadcast=True)

def run_flask():
    socketio.run(app, port=3000)

def run_socket_server():
    pass

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    socket_thread = threading.Thread(target=run_socket_server)
    socket_thread.start()








