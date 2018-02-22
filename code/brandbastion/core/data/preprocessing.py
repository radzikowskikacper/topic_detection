import nltk

while True:
    try:
        from nltk.stem import WordNetLemmatizer
        from nltk.corpus import wordnet, stopwords
        from nltk.tokenize import WordPunctTokenizer
        break
    except:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download("wordnet")
        nltk.download('stopwords')


class Splitter(object):
    def __init__(self):
        self.splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self,text):
        sentences = self.splitter.tokenize(text)
        tokens = [self.tokenizer.tokenize(sent) for sent in sentences]
        return tokens

class LemmatizationWithPOSTagger(object):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def get_wordnet_pos(self,treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV

        return wordnet.NOUN

    def pos_tag(self,tokens):
        pos_tokens = [nltk.pos_tag(token) for token in tokens]
        pos_tokens = [self.lemmatizer.lemmatize(word, self.get_wordnet_pos(pos_tag)) for pos in pos_tokens for (word, pos_tag) in pos]

        return pos_tokens

splitter = Splitter()
lemmatization_using_pos_tagger = LemmatizationWithPOSTagger()

def remove_sw_and_stem(doc):
    stopset = set(stopwords.words('english'))
    stemmer = nltk.PorterStemmer()
    tokens = WordPunctTokenizer().tokenize(doc)
    clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
    final = [stemmer.stem(word) for word in clean]
    return final

def lemmatize(sentence):
    tokens = splitter.split(sentence)
    lemma_pos_token = lemmatization_using_pos_tagger.pos_tag(tokens)
    return lemma_pos_token