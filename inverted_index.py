class InvertedIndex:
    def __init__(self, tokens):
        self.corpus = set()
        self.corpus_table = {}
        self.__doc_tokens = {k: v for k, v in tokens.items() if k != "q"}

    def take_unique_term(self):
        for t in self.__doc_tokens.values():
            self.corpus.update(t)
        self.corpus = sorted(self.corpus)

    def create_corpus_table(self):
        for term in self.corpus:
            self.corpus_table[term] = {}
            df = 0

            for doc, words in self.__doc_tokens.items():
                tf = words.count(term)
                self.corpus_table[term][doc] = tf

                if tf > 0:
                    df += 1

            self.corpus_table[term]["dft"] = df
