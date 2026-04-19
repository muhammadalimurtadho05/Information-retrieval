from read_documents import documents as docs
from text_preprocessing import TextPreprocessing
from inverted_index import InvertedIndex
from bm25 import BM25

# stopwords list
def retrieval(query):
    stopwords = [
        "dengan",
        "dan",
        "untuk",
        "pada",
        "di",
        "dari",
        "yang",
        "karena",
        "akibat",
        "penelitian",
        "hasil",
        "metode",
        "data",
        "analisis",
        "studi",
        "artikel",
        "jurnal",
        "penulis",
        "berdasarkan",
        "menunjukkan",
        "dapat",
        "dilakukan",
        "tahun",
        "terhadap",
        "antara",
        "dalam",
    ]


    # >= step 1: text preprocessing
    tp = TextPreprocessing(stopwords, query, docs)
    # tokenization
    tp.tokenization()
    # case folding
    tp.case_folding()
    # stopword removal
    tp.stopword_removal()
    # stemming
    tp.stemming()
    # get tokens
    tokens = tp.tokens


    # >= step 2: get documents length and create inverted index
    # sum all doc length
    total_doc_length = 0

    for k in tokens:
        total_doc_length += tp.get_doc_length(tokens[k])

    # calulate avgl
    avgl = total_doc_length / len(list(tokens.values())[1:])  # avgl value


    # >= step 3: corpus table
    corpus = InvertedIndex(tokens)
    # select all unique terms from each docs
    corpus.take_unique_term()
    # create corpus table
    corpus.create_corpus_table()
    # get corpus taable
    corpus_table = corpus.corpus_table


    # inisialisasi BM25
    bm25 = BM25(tokens, corpus_table, avgl)

    # hitung ranking
    ranking = bm25.rank()
    hasil = {}
    if all(score == 0 for _, score in ranking):
        hasil['404'] = "Tidak ada dokumen yang relevan dengan query." 
        #print("\nTidak ada dokumen yang relevan dengan query.")
    else:
        #print("\n=== HASIL RANKING BM25 ===")
        for doc, score in ranking:
            #print(f"{docs[doc]}: {score:.4f} - doc-id -> {doc}")
            hasil[doc] = docs[doc]
    
    return hasil
