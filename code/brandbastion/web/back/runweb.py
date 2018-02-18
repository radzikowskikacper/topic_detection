from flask import Flask
from flask import request
from flask import jsonify
from brandbastion.core.similarities import doc2vec, tfidf
from brandbastion.core.data import loader
import os


app = Flask(__name__)

print("Loading models")
models = {}#{'tfidf' : tfidf.load_model('tfidf.model'), 'doc2vec' : doc2vec.load_model('doc2vec.model')}
dataset = loader.load_from_file('IG-comments.txt')
#doc2vec.create_embeddings(dataset, 'model.model10')
models['doc2vec'] = doc2vec.load_model('model.model10')
doc2vec.get_similar_comments("I love hamburgers", models['doc2vec'], dataset)
print('Done')

@app.route('/recalculate')
def recalculate():
    pass

@app.route('/data')
def data():
    pass

@app.route('/visualize')
def visualize():
    pass

@app.route('/similarity/<string:model>', methods=['GET'])
def predict(model):
    if model == 'doc2vec':
        similar_comments = doc2vec.get_similar_comments(request.args.get('sample'), models['doc2vec'], dataset)

        response = jsonify({'sample' : request.args.get('sample'), 'results' : similar_comments})
        response.status_code = 200
        return response

if __name__ == "__main__":
    pass
    #app.run(host='0.0.0.0', port=9999)