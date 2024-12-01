from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from chat.chat import generate_response

app = Flask(__name__, static_folder='web-ui/build', static_url_path='/')
CORS(app)

@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    user_message = data.get('message', '')
    try:
        response = generate_response(user_message)

        return jsonify({
            'status': 'success',
            'response': response
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)