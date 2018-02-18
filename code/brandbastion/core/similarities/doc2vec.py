from gensim.models.doc2vec import TaggedDocument
import gensim
from gensim.models.doc2vec import Doc2Vec
from brandbastion.core.similarities import MODELS_PATH


class TaggedDocument2(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list



    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield TaggedDocument(words=doc.split(), tags=[self.labels_list[idx]])

def load_model(mname):
    return Doc2Vec.load('{}/{}'.format(MODELS_PATH, mname))

def create_embeddings(data, mname):
    total_words = sum([len(d.split()) for d in data.values()])
    it = TaggedDocument2(data.values(), list(data.keys()))

    model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11, alpha=0.025,
                                  min_alpha=0.025)  # use fixed learning rate
    model.build_vocab(it)
    for epoch in range(10):
        model.train(it, total_words = total_words, epochs=1)
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no deca

    model.save('{}/{}'.format(MODELS_PATH, mname))

def get_similar_comments(sample, model, data):
    tokens = sample.split()
    new_vector = model.infer_vector(tokens)
    print(new_vector.shape)
    return [(nn[0], nn[1], data['{}'.format(nn[0])]) for nn in model.docvecs.most_similar([new_vector])]