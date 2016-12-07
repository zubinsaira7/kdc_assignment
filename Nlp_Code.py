import urllib, json
from wikitools import wiki
from wikitools import api
from wikitools import category
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
from text_cleaner import Cleaner
from spacy.en import English
parser = English()

# for id in range(1,10):
#     res = es.get(index="kdc", doc_type="arts",id=id)
#     print res['_source']['Summary']
#     print ":::::::::::::::::::::::::: After Cleaning ::::::::::::::::::::::"
#     clnr=Cleaner()
#     clean_text=clnr.clean_string(res['_source']['Summary'])
#     print clean_text
#     print "::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
#     sentence_text=parser(res['_source']['Summary'])
#     for span in sentence_text.sents:
#         print span
#         print ":::::::::::::::::::::::span:::::::::::::::::::::::::::::::::::::::::"
# science 1005 arts 1260 computing 1005


clnr=Cleaner()
for id in range(0,1262):
    res = es.get(index="kdc", doc_type="computing",id=id)
    print res['_source']['Summary']
    print ":::::::::::::::::::::::::: After Cleaning "+str(id)+"::::::::::::::::::::::"   
    sentence_text=parser(res['_source']['Summary'])
    title=parser(res['_source']['Title'])
    category=parser(res['_source']['Category'])
    doc_as_list=[]
    if sentence_text!="":
        sentence_list=[]
        for sentence in sentence_text.sents:
            if len(sentence)!=0:                
                #print span
                #print "::::::----------:::::::::"
                clean_text=clnr.clean_string(str(sentence))
                #print clean_text
                sentence_list.append(clean_text)
                #doc_as_list=clnr.clean_string(sentence_text)
                for token in clean_text:
                    doc_as_list.append(str(token))
            else:
                print "::::::NO SENTENCE:::::::::"
        #print sentence_list
        print ":::::::::::::::::::::::span:::::::::::::::::::::::::::::::::::::::::"
        #print doc_as_list        
        #print ":::::::::::::::::::::::doc_list:::::::::::::::::::::::::::::::::::::::::"
        
        doc={
            'Category':str(category),
            'Title':str(title),
            'Summary':str(sentence_text),
            'sentence_list':sentence_list,
            'words': doc_as_list
            }
        es.index(index="kdc",doc_type='computing',id=id,body=doc)
        print doc
    else:
        print "::::::::::::::BLANK::::::::::::::::"


# clnr=Cleaner()
# for id in range(0,1006):
#     res = es.get(index="kdc", doc_type="arts",id=id)
#     print res['_source']['Summary']
#     print ":::::::::::::::::::::::::: After Cleaning "+str(id)+"::::::::::::::::::::::"   
#     sentence_text=parser(res['_source']['Summary'])
#     if sentence_text!="":
#         for span in sentence_text.sents:
#             if len(span)!=0:
#                 print span
#                 print "::::::----------:::::::::"
#                 clean_text=clnr.clean_string(str(span))
#                 print clean_text
#             else:
#                 print "::::::NO SENTENCE:::::::::"
#             print ":::::::::::::::::::::::span:::::::::::::::::::::::::::::::::::::::::"
#     else:
#         print "::::::::::::::BLANK::::::::::::::::"





#for hit in res['hits']['hits']:
    #print("%(Category)s %(Summary)s: %(Title)s" % hit["_source"])
 #   print("%(Category)s" % hit["_source"])
  #  print("::::::::::::::::::::::::::::::::::::::::::::::::")



#             try:          
#                 page_title=page['title'].encode('utf-8')
#                 if page_title[0:9]!="Category:":
#                     print "Page :::::::::::::::::::"+str(cnt+1)  
#                     page_summary=find_summary(page_title)
#                     page_summary=remove_garbage(page_summary)
#                     page_title=remove_garbage(page_title)

#                     doc = {
#                             'Category': title,
#                             'Title': page_title,
#                             'Summary': page_summary
#                         }
#                     res = es.index(index="kdc", doc_type=cat, id=cnt, body=doc)

#                     print "Category::::::::::"+str(title)
#                     print "Title:::::::::::::"+str(page_title)
#                     print "Summary:::::::::::"+str(page_summary)  
#                     cnt+=1                                      
#             except Exception,e:
#                 print "Error :: unicode/orientdb"+str(e)
#                 continue   
#         for category in categorymembers:
#             try:        
#                 cat_title=category['title'].encode('utf-8')
#                 if cat_title[0:9]=="Category:":
#                     #cat_title=remove_garbage(cat_title[9:])
#                     cat_title=cat_title[9:]                                     
#                     find_pages(cat_title)                    
#             except Exception,e:
#                 print "Error :: categories insertion unicode/orientdb"+str(e)
#                 continue     
#         if cnt>1000:
#             exit(1)             
#     except Exception, e:
#         print "Page url error >>>>>>>>>>>>>>>>>>>>>"+str(e)
#     return                    
# find_pages(cat)