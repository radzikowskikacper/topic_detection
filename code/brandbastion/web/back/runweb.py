from flask import Flask
from flask import request
from flask import jsonify
from brandbastion.core.similarities import doc2vec
from brandbastion.core.data import loader


app = Flask(__name__)

print("Loading models")
models = {}
models['doc2vec'] = doc2vec.load_model('model.model')
print('Done')

@app.route('/transfer_to_db')
def transfer_to_db():
    loader.save_to_database('IG-comments.txt')

@app.route('/recalculate')
def recalculate():
    doc2vec.create_embeddings(loader.load_from_database(), 'model.model')
    models['doc2vec'] = doc2vec.load_model('model.model')

@app.route('/data', methods = ['POST'])
def data():
    loader.add_to_db(request.get('comment'))

@app.route('/similarity/<string:model>/<int:number>', methods=['GET'])
def predict(model, number):
    if model == 'doc2vec':
        similar_comments = doc2vec.get_similar_comments(request.args.get('sentence'), models['doc2vec'], number)
        response = jsonify({'sentence' : request.args.get('sentence'), 'results' : similar_comments})
        response.status_code = 200
        return response

def start_server():
    app.run(host='0.0.0.0', port=9999)
