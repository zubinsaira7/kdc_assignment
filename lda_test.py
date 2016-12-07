from gensim import corpora, models
from elasticsearch import Elasticsearch
import numpy as np
domain=raw_input("Domain : ")
id=raw_input("DOC Query number : ")
es = Elasticsearch("http://localhost:9200")
res = es.get(index="kdc", doc_type=domain,id=id)
doc=res['_source']['words']
text=res['_source']['Summary']

docs=[]
for id in range(0,1005):
    res = es.get(index="kdc", doc_type=domain,id=id)
    docs.append(res['_source']['words'])

lda_model=models.LdaModel.load('/home/beta_rygbee/saurabh/kdc_project/models/my_lda_model_'+domain+'.model')

id2word = corpora.Dictionary(docs)
query = id2word.doc2bow(doc)
result=lda_model[query]
#print query

print "QUERY  :: " + str(doc)
print "Result :: " +str(result)
print "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
for r in result:	
	print "Matched with     :: " + str(float(r[1])*100)+ " percentage."
	print "Topic words      :: " + str(lda_model.print_topic(r[0], 10))
	print "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"






#print(lda_model.print_topics(100))

# print ":::::::::::::::::::::::::::::::::::::::::::::::::::"
# print(lda_model.print_topics(num_topics=100, num_words=5))

#print lda_model.print_topic(90, topn=200)
#print lda_model.get_topic_terms(20,topn=10)
# print ":::::::::::::::::::::::::model::::::::::::::::::::::::::"
# print lda_model
# print ":::::::::::::::::::::::::::::::::::::::::::::::::::"
# print lda_model.show_topics(100, 20)

# print topic 28


# another way
# for i in range(0, model.num_topics-1):
#     print model.print_topic(i)