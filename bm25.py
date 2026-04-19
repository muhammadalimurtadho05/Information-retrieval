import math


class BM25:
    def __init__(self, tokens, corpus_table, avgdl, k1=1.2, b=0.75):
        # ambil dokumen saja (tanpa query)
        self.docs = {k: v for k, v in tokens.items() if k != "q"}
        self.query = tokens["q"]

        self.corpus_table = corpus_table
        self.N = len(self.docs)
        self.avgdl = avgdl

        self.k1 = k1
        self.b = b

        # hitung panjang dokumen
        self.doc_len = {doc: len(words) for doc, words in self.docs.items()}

        # hitung IDF BM25
        self.idf = self.calculate_idf()

    def calculate_idf(self):
        idf = {}
        for term in self.query:
            if term in self.corpus_table:
                df = self.corpus_table[term]["dft"]
                idf[term] = math.log((self.N - df + 0.5) / (df + 0.5))
            else:
                idf[term] = 0
        return idf

    def calculate_score(self):
        scores = {}

        for doc, words in self.docs.items():
            score = 0
            dl = self.doc_len[doc]

            # hitung K
            K = self.k1 * ((1 - self.b) + self.b * (dl / self.avgdl))

            for term in self.query:
                if term not in self.corpus_table:
                    continue

                tf = self.corpus_table[term][doc]
                idf = self.idf.get(term, 0)

                if tf == 0:
                    continue

                numerator = tf * (self.k1 + 1)
                denominator = tf + K

                score += idf * (numerator / denominator)

            scores[doc] = score

        return scores

    def rank(self):
        scores = self.calculate_score()
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked
