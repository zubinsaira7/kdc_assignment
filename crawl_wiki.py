import urllib, json
from wikitools import wiki
from wikitools import api
from wikitools import category
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")
cnt=0 
cat=raw_input("Enter Category : ")
def remove_garbage(text):
    try:
        text = text.replace('\n',' ')
        text = text.replace('\\','\\\\')
        text = text.replace('\'','\\\'')
        text = text.replace('  ','')
        # text = to_unicode(text)
    except Exception, e:
        print "Conversion error"
        return text 
    return text 
def find_summary(title):
    try:    
        url="https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles="+title
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        pageid=str(data['query']['pages'].keys())
        pageid=pageid.replace('[','')
        pageid=pageid.replace(']','')
        pageid=pageid.replace('u\'','')
        pageid=pageid.replace('\'','')
        page_summary=data['query']['pages'][pageid]['extract']
        page_summary=page_summary.encode('utf-8')
    except Exception, e:
        print "Page url error >>>>>>>>>>>>>>>>>>>>>"+str(e)
    return page_summary
def find_pages(title):
    global cnt
    print ":::::::::::::::::::::::::::Category::::::"+str(title)+":::::::::::::::::::::::::::"
    try:    
        url="https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category%3A"+title+"&cmlimit=500"        
        response = urllib.urlopen(url)
        json_data = json.loads(response.read())
        categorymembers=json_data['query']['categorymembers']        
    
        for page in categorymembers:  
            try:          
                page_title=page['title'].encode('utf-8')
                if page_title[0:9]!="Category:":
                    print "Page :::::::::::::::::::"+str(cnt+1)  
                    page_summary=find_summary(page_title)
                    page_summary=remove_garbage(page_summary)
                    page_title=remove_garbage(page_title)

                    doc = {
                            'Category': title,
                            'Title': page_title,
                            'Summary': page_summary
                        }
                    res = es.index(index="kdc", doc_type=cat, id=cnt, body=doc)

                    print "Category::::::::::"+str(title)
                    print "Title:::::::::::::"+str(page_title)
                    print "Summary:::::::::::"+str(page_summary)  
                    cnt+=1                                      
            except Exception,e:
                print "Error :: unicode/orientdb"+str(e)
                continue   
        for category in categorymembers:
            try:        
                cat_title=category['title'].encode('utf-8')
                if cat_title[0:9]=="Category:":
                    #cat_title=remove_garbage(cat_title[9:])
                    cat_title=cat_title[9:]                                     
                    find_pages(cat_title)                    
            except Exception,e:
                print "Error :: categories insertion unicode/orientdb"+str(e)
                continue     
        if cnt>1000:
            exit(1)             
    except Exception, e:
        print "Page url error >>>>>>>>>>>>>>>>>>>>>"+str(e)
    return                    
find_pages(cat)