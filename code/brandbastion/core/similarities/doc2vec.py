from gensim.models.doc2vec import TaggedDocument
import gensim
from gensim.models.doc2vec import Doc2Vec
from brandbastion.core.similarities import MODELS_PATH
from brandbastion.core.data import loader
from itertools import tee
from brandbastion.core.data import preprocessing


class TaggedDocumentDecorator():
    def __init__(self, dataset_gen):
        self.original_generator = dataset_gen

    def __iter__(self):
        self.original_generator, self.original_generator_copy = tee(self.original_generator)
        for line in self.original_generator_copy:
            #tokens = line[2].split()
            tokens = preprocessing.lemmatize(line[2])
            yield TaggedDocument(words=tokens, tags=[line[1]])

def load_model(mname):
    import os
    print(os.getcwd())
    return Doc2Vec.load('{}/{}'.format(MODELS_PATH, mname))

def create_embeddings(dataset, mname):
    it = TaggedDocumentDecorator(dataset)

    model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11, alpha=0.025,
                                  min_alpha=0.025)
    model.build_vocab(it)

    for epoch in range(10):
        model.train(it, total_words=model.corpus_count, epochs=1)
        model.alpha -= 0.002
        model.min_alpha = model.alpha
        model.train(it, total_words=model.corpus_count, epochs=1)

    model.save('{}/{}'.format(MODELS_PATH, mname))

def get_similar_comments(sample, model, number):
    #tokens = sample.split()
    tokens = preprocessing.lemmatize(sample)
    new_vector = model.infer_vector(tokens)
    similar = model.docvecs.most_similar([new_vector], topn = number)

    texts = loader.load_from_database([nn[0] for nn in similar])
    result = list()
    for text, nn in zip(texts, similar):
        result.append(['{}'.format(nn[0]), '{}'.format(nn[1]), text[2]])
    return result