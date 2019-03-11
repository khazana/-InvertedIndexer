from bs4 import BeautifulSoup
import os
from collections import defaultdict
import json


#global dictionaries which contains terms as the key and values 
#are in the form (docID1,term_count),(docID2,term_count)]
unigram_term = {}
bigram_term = {}
trigram_term = {}

path_to_raw_files = '/Users/fathimakhazana/Documents/IRHW3/RawTextFiles/'
path_to_tokenized_files = '/Users/fathimakhazana/Documents/IRHW3/ParsedTextFiles/'

#dictionary which contains document ID as key and number of terms in it as value
#includes all terms, unigrams, bigrams and trigrams
term_count = {}
term_count= defaultdict(lambda: 0, term_count)
        

#returns list of ngrams which were saved to files in 'extract_terms.py'
def get_ngrams_list_from_file():
      f = open('unigrams.txt', 'r')
      unigrams_list = f.readlines()
      f.close()
    
      f = open('bigrams.txt', 'r')
      bigrams_list = f.readlines()
      f.close()
      
      f = open('trigrams.txt', 'r')
      trigrams_list = f.readlines()
      f.close()
      return unigrams_list, bigrams_list, trigrams_list 


def get_document_ID(file):
    docID = file.split(path_to_raw_files)
    docID = docID[1]
    docID = docID.split('_raw.txt')[0]
    return docID
 
#extract appropriate text from webpage from saved raw HTML files       
def extract_text_from_webpage(rawfile):
    fh = open(rawfile,"rb")
    contents = fh.read().decode(errors='replace')
    all_text = []
    soup = BeautifulSoup(contents,features="lxml")
    if soup.select(".firstHeading"):
         first_heading =  soup.select(".firstHeading")[0].text
         all_text.append(first_heading)
    soup = soup.find("div", {"class":"mw-body"})
    if soup.find('div', id="toc"):
        soup.find('div', id="toc").decompose()
    if soup.find('div', {"class":"reflist"}):
        soup.find('div', {"class":"reflist"}).decompose()
    if soup.find_all("div", {'class':'navbox'}): 
        for div in soup.find_all("div", {'class':'navbox'}): 
            div.decompose()
    text = soup.text
    text = text.lower()
    return text
    
#find count of unigrams which occur in a document    
def find_unigrams_count_in_document(text,unigrams_list,docID):
    for unigram in unigrams_list:
        unigram = unigram.strip()
        unigram = " " + unigram + " "
        if unigram in text:
            unigram_term.setdefault(unigram,[]).append((docID, text.count(unigram)))
            count = term_count[docID]
            term_count[docID] = count + text.count(unigram)
            
#find count of bigrams which occur in a document              
def find_bigrams_count_in_document(text,bigrams_list,docID):
    for bigram in bigrams_list:
        bigram = bigram.strip()
        bigram = " " + bigram + " "
        if bigram in text:
            bigram_term.setdefault(bigram,[]).append((docID, text.count(bigram)))
            count = term_count[docID]
            term_count[docID] = count + text.count(bigram)
            
#find count of trigrams which occur in a document              
def find_trigrams_count_in_document(text,trigrams_list,docID): 
    for trigram in trigrams_list:
        trigram = trigram.strip()
        trigram = " " + trigram + " "
        if trigram in text:
            trigram_term.setdefault(trigram,[]).append((docID, text.count(trigram)))
            count = term_count[docID]
            term_count[docID] = count + text.count(trigram)
           
            
#main function which creates the inverted index      
def inverted_indexer():
    files = [i for i in os.listdir(path_to_raw_files) if i.endswith(".txt")]
    unigrams_list, bigrams_list, trigrams_list  =  get_ngrams_list_from_file()
    for file in files:
        docID = get_document_ID(file)
        text = extract_text_from_webpage(path_to_raw_files + file)
        find_unigrams_count_in_document(text,unigrams_list,docID)
        find_bigrams_count_in_document(text,bigrams_list,docID)
        find_trigrams_count_in_document(text,trigrams_list,docID)

        
#save dictionaries to text file
def write_dict_to_file():
    f = open('InvertedLists/unigram_indexer.txt', 'w+')
    f.write(json.dumps(unigram_term))
    g = open('InvertedLists/bigram_indexer.txt', 'w+')
    g.write(json.dumps(bigram_term))
    h = open('InvertedLists/trigram_indexer.txt', 'w+')
    h.write(json.dumps(trigram_term))
    i = open('term_count.txt', 'w+')
    i.write(json.dumps(term_count))


inverted_indexer()
write_dict_to_file()
        
        
