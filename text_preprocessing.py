from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class TextPreprocessing:
    tokens = {}

    def __init__(self, stopwords, query, docs):
        self.__stopwords = stopwords
        self.__query = query
        self.__docs = docs

    def tokenization(self):
        self.tokens = {"q": self.__query.split()}

        for doc, word in zip(self.__docs.keys(), self.__docs.values()):
            self.tokens[doc] = word.split()

    def case_folding(self):
        for key, token in zip(self.tokens.keys(), self.tokens.values()):
            arr = []
            for word in token:
                arr.append(word.lower())
            self.tokens[key] = arr

    def stopword_removal(self):
        for key, token in zip(self.tokens.keys(), self.tokens.values()):
            for stopword in self.__stopwords:
                if stopword in token:
                    token.remove(stopword)
            self.tokens[key] = token

    def stemming(self):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        for key, token in zip(self.tokens.keys(), self.tokens.values()):
            words = " ".join(token)
            opt = stemmer.stem(words)
            self.tokens[key] = opt.split()

    def get_doc_length(self, doc):
        return len(doc)
