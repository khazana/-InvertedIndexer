import os
import multiprocessing
import re
from nltk import ngrams


#global variable which contains a list of unique unigrams from all documents
unigrams = []
bigrams = []
trigrams = []

path_to_raw_files = '/Users/fathimakhazana/Documents/IRHW2/RawTextFiles/'
path_to_tokenized_files = '/Users/fathimakhazana/Documents/IRHW2/ParsedTextFiles/'

#Reads corpora from saved folder and creates three lists of terms to be part of the index
def get_terms_of_document(f):
    f = open(f,"r")
    tokens_string = f.read()
    f.close()
    list1 = [x.strip() for x in tokens_string.split(',')]
    tokens_list = []
    for l in list1:
        tokens_list.append(l.replace("'",""))
    tokens_list[0] = tokens_list[0].replace('[','')
    tokens_list[len(tokens_list) - 1] = tokens_list[len(tokens_list) - 1].replace(']','')
    for i in range(len(tokens_list)-1):
        tokens_list[i] = re.sub(r'[^a-zA-Z0-9-]', '', tokens_list[i])
                    
    bigrams_list = ngrams(tokens_list,2)
    bigrams_list = [list(elem) for elem in bigrams_list]
    bigrams_list = [' '.join(b) for b in bigrams_list]
    b_list = [b for b in bigrams_list if len(b.split()) > 1]

    trigrams_list = ngrams(tokens_list,3)
    trigrams_list = [list(elem) for elem in trigrams_list]
    trigrams_list = [' '.join(t) for t in trigrams_list]
    t_list = [t for t in trigrams_list if len(t.split()) > 2]

    return tokens_list,b_list,t_list

def save_lists_to_file(file_name,ngrams_list):
    with open(file_name, 'w') as f:
        for item in ngrams_list:
            f.write("%s\n" % str(item))
            

files = [i for i in os.listdir(path_to_tokenized_files) if i.endswith(".txt")]
pool_get_attributes = multiprocessing.Pool(4)
d = pool_get_attributes.map(get_terms_of_document, [path_to_tokenized_files + f for f in files])
pool_get_attributes.close()
pool_get_attributes.join()
unigrams_list = set()
bigrams_list = set()
trigrams_list = set()
for i in range (len(d)):
    ungrams = d[i][0]
    bigrams = d[i][1]
    trigrams = d[i][2]
    for y in range(len(unigrams)):
                    unigrams_list.add(unigrams[y])
    for j in range(len(bigrams)):
                    bigrams_list.add(bigrams[j])
    for k in range(len(trigrams)):
                trigrams_list.add(trigrams[k])  
save_lists_to_file('unigrams.txt',unigrams_list)
save_lists_to_file('bigrams.txt',bigrams_list)
save_lists_to_file('trigrams.txt',trigrams_list)
 

  





