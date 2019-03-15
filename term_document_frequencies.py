import json
import inspect


#source:https://stackoverflow.com/a/18425523/8933813
#function which returns variable name as string
def get_var_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [k for k, v in callers_local_vars if v is var]


#used to write file to dictionary
def get_dict(file):
     f = open(file, 'r')
     term_dict = json.loads(f.read())
     return term_dict
    
#returns sorted dictionary of term frequencies
def terms_frequency(term_dict):
    term_frequency = {}
    for k, v in term_dict.items(): 
        count = 0
        for i in range (0,len(v)):
            count = count + v[i][1]
        term_frequency.setdefault(k,[]).append(count)
    term_dict = dict(sorted(term_frequency.items(), key=lambda kv: kv[1],  reverse=True))
    return term_dict

#returns sorted dictionary of document frequencies
def doc_frequency(term_dict):
    document_frequency = {}
    for k, v in term_dict.items(): 
        documents = []
        for i in range (0,len(v)):
            documents.append(v[i][0])
        document_frequency.setdefault(k,[]).append(documents)
        document_frequency[k] = [document_frequency[k], len(documents)]
    doc_dict = dict(sorted(document_frequency.items(), key=lambda kv: kv[0]))
    return doc_dict

def write_dict_to_file(dictionary, dictionary_name):
     with open(dictionary_name + '.txt', "a") as f:
         f.writelines('{}:{} \n'.format(k,v) for k, v in dictionary.items())

#generates stoplist from dictionaries stored in file 
def generate_stop_list(file):
    stoplist = []
    b = {}
    f = open(file, 'r')
    term_list = f.readlines()
    term_list = [t.strip() for t in term_list]
    f.close()
    for i in term_list:
        k,v = i.split(':')
        v = v.split(',')
        for value in v:
          b.setdefault(k,[]).append(value)
    for k,v in b.items():
        count = v[len(v) - 1]
        count = int(count.replace(']',''))
        if count/955 > 0.5:
            stoplist.append(k)
    
    
#Get inverted lists for each unigrams, bigrams and trigrams
unigram_dict = get_dict('InvertedLists/unigram_indexer.txt')
bigram_dict = get_dict('InvertedLists/bigram_indexer.txt')
trigram_dict = get_dict('InvertedLists/trigram_indexer.txt')

#term frequency
unigram_term_frequency = terms_frequency(unigram_dict)
bigram_term_frequency1 = terms_frequency(bigram_dict)
trigram_term_frequency = terms_frequency(trigram_dict)

write_dict_to_file(unigram_term_frequency, get_var_name(unigram_term_frequency)[0])
write_dict_to_file(bigram_term_frequency1, get_var_name(bigram_term_frequency1)[0])
write_dict_to_file(trigram_term_frequency,get_var_name(trigram_term_frequency)[0])

#document frequency
unigram_doc_frequency = doc_frequency(unigram_dict)
bigram_doc_frequency1 = doc_frequency(bigram_dict)
trigram_doc_frequency = doc_frequency(trigram_dict)

write_dict_to_file(unigram_doc_frequency, get_var_name(unigram_doc_frequency)[0])
write_dict_to_file(bigram_doc_frequency1, get_var_name(bigram_doc_frequency1)[0])
write_dict_to_file(trigram_doc_frequency,get_var_name(trigram_doc_frequency)[0])

