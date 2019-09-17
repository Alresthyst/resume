###         Data Cleasing:
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
import excel, re

#Integer remover.
def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def clean(documents):
    tokenizer = RegexpTokenizer(r'\w+')
    stoplist = set(stopwords.words('english'))
    p_stemmer = PorterStemmer()

    # 아스키 코드를 이용할 수 있는 방법은 없을까?
    punctuation = re.compile(r'[-.?!,":;()①@③⑨⑩⑤②⑦⑥⑧④|\d]')
    texts = []
    for doc in documents:
        raw = doc.lower()
        tokens = tokenizer.tokenize(raw)
        for idx, token in enumerate(tokens):
            token = punctuation.sub("", token)
            #How can I remove the integer tokens?
            if isNumber(token):
                print(token)
                tokens.pop(idx)
        # remove stop words from tokens.
        stopped_tokens = [i for i in tokens if not i in stoplist]
        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        final_token = [i for i in stemmed_tokens if not i in stoplist]
        # add tokens to list
        texts.append(final_token)

    # rid of word that appears only once.
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] > 1] for text in texts]
    return texts

### Preparing Document-Term Matrix.
# Creating the term dictionary of our courpus, where every unique term is assigned an index.
from gensim import corpora, models

doc_clean = clean(excel.doc98_01)
dictionary = corpora.Dictionary(doc_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

###Running LDA Model
# Creating the object for LDA model using gensim library.
Lda = models.LdaModel
ntopics = 10
nwords = 10

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=ntopics, id2word = dictionary, passes=50)

#Pretty printing
for idx, val in ldamodel.print_topics(num_topics=ntopics, num_words=nwords):
    print(idx,":",val)
