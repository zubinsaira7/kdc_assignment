# import urllib, json
# from wikitools import wiki
# from wikitools import api
# from wikitools import category
# from elasticsearch import Elasticsearch
# es = Elasticsearch("http://localhost:9200")
# from text_cleaner import Cleaner
# for id in range(0,1005):
#     res = es.get(index="kdc", doc_type="computing",id=id)
#     print res['_source']['words']
#     print ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"

from elasticsearch import Elasticsearch
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

es = Elasticsearch("http://localhost:9200")
docs=[]
for id in range(0,1005):
    res = es.get(index="kdc", doc_type="arts",id=id)
    #print res['_source']['words']
    docs.append(res['_source']['words'])
print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#raw_input("docs: ")
#print docs
#docs=[['word1', 'word2', 'word3', 'lastword'], ['label1']]
sentence = LabeledSentence([[u'some', u'words', u'here']], [[u'SENT_1']])


class LabeledLineSentence(object):
    def __init__(self, doc_list):
        self.doc_list = doc_list
    def __iter__(self,):
        for uid, line in enumerate(self.doc_list):
            yield LabeledSentence(line, ['SENT_%s' % uid])

doc_itr=LabeledLineSentence(docs)


doc_model = Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
doc_model.build_vocab(doc_itr)
for epoch in range(1000):
    doc_model.train(doc_itr)
    doc_model.alpha -= 0.002  # decrease the learning rate
    doc_model.min_alpha = doc_model.alpha
doc_model.save('/home/beta_rygbee/saurabh/kdc_project/models/my_model_arts.doc2vec')
print doc_model.vocab.keys()
print "????????????????????????????????????????????????????????????????????????????????????"
print doc_model.docvecs.similarity(21,102)
print "????????????????????????????????????????????????????????????????????????????????????"
