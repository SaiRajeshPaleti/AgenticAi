from flask import Flask, Response, request
from flask_cors import CORS
from azure_helper import azure_fetch_realtime_data

app = Flask(__name__)
CORS(app)

@app.route('/stream')
def stream():
    prompt = request.args.get('prompt', '')
    def event_stream():
        for token in azure_fetch_realtime_data(prompt):
            yield f'data: {token}\n\n'
    return Response(event_stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
