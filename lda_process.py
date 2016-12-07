from gensim import corpora, models
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
docs=[]
for id in range(0,1005):
    res = es.get(index="kdc", doc_type="science",id=id)
    docs.append(res['_source']['words'])
print docs
dictionary = corpora.Dictionary(docs)
corpus = [dictionary.doc2bow(text) for text in docs]
print(corpus[0])
lda_model=models.ldamodel.LdaModel(corpus, num_topics=100, id2word = dictionary, passes=100)
lda_model.save('/home/beta_rygbee/saurabh/kdc_project/models/my_lda_model_science.model')

print ":::::::::::::::::::::::::::::::::::::::::::::::::::"
print lda_model.get_topic_terms(2,topn=10)
print ":::::::::::::::::::::::::::::::::::::::::::::::::::"