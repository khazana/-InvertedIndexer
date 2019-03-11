#This code saves unigrams, bigrams and trigrams extracted from the corpus to text files


from bs4 import BeautifulSoup
import re
from nltk import tokenize
import string
import itertools
import os
from nltk import ngrams


#global variable which contains a list of unique unigrams from all documents
unigrams = []

path_to_raw_files = '/Users/fathimakhazana/Documents/IRHW3/RawTextFiles/'
path_to_tokenized_files = '/Users/fathimakhazana/Documents/IRHW3/ParsedTextFiles/'

#Function to create the corpus for a document (from previous assigment)
#Raw content of all URLS in BFS.txt are stored in 'path_to_raw_files'
#Extracts required content and tokenizes it
#Removes punctuation except '-'
#Saves the corpus in 'ParsedTextFiles'
#also appends unigrams from each corpus to global variable 'unigrams'(added for this assignment)
def get_unigrams_for_document(rawfile):
    fh = open(rawfile,"rb")
    contents = fh.read().decode(errors='replace')
    all_text = []
    soup = BeautifulSoup(contents,features="lxml")
    if soup.select(".firstHeading"):
         first_heading =  soup.select(".firstHeading")[0].text
         first_heading = tokenize.wordpunct_tokenize(first_heading.lower().strip())
         all_text.append(first_heading)
    soup = soup.find("div", {"class":"mw-content-ltr"})
    if soup.find('div', id="toc"):
        soup.find('div', id="toc").decompose()
    if soup.find('div', {"class":"reflist"}):
        soup.find('div', {"class":"reflist"}).decompose()
    if soup.find_all("div", {'class':'navbox'}): 
        for div in soup.find_all("div", {'class':'navbox'}): 
            div.decompose()
    content = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p','li'])
    file_name = rawfile.split(path_to_raw_files)[1]
    file_name = file_name.split('_raw.txt')[0]
    file_name = file_name + '.txt'
    if '\\n' in file_name:
        file_name = file_name.replace('\\n','')
    if '/' in file_name:
        file_name = file_name.replace('/','-')
    with open(path_to_tokenized_files + file_name, 'w') as f:
        for header in content:
            text = header.text
            text = text.replace('[edit]', '')
            text = re.sub(r"\[\d+", " ", text)
            remove = string.punctuation
            remove = remove.replace("-", "")
            pattern = r"[{}]".format(remove)
            text = re.sub(pattern, "", text)  
            text = tokenize.wordpunct_tokenize(text.lower().strip())
            all_text.append(text)
        processed_list = list(itertools.chain.from_iterable(all_text))
        f.write("%s\n" % processed_list)
        for word in processed_list:
            word = re.sub(r'[^a-zA-Z0-9-]', '', word)
            if word:
                if word not in unigrams:
                    unigrams.append(word)

#function to get unigrams from all documents  
#result stored in variable 'unigrams'                    
def get_unigrams():
    files = [i for i in os.listdir(path_to_raw_files) if i.endswith(".txt")]
    for file in files:
        get_unigrams_for_document(path_to_raw_files + file)     
        
#function which creates a list of ngrams from unigrams list      
def create_ngrams_list(n):
    ngrams_list = ngrams(unigrams,n)
    terms_list = [list(elem) for elem in ngrams_list]
    return terms_list

        
def save_lists_to_file(file_name,ngrams_list):
    with open(file_name, 'w') as f:
        for item in ngrams_list:
            item = ' '.join(item)
            f.write("%s\n" % str(item))


get_unigrams()
bigrams = create_ngrams_list(2)
trigrams = create_ngrams_list(3)
save_lists_to_file('unigrams.txt', unigrams)
save_lists_to_file('bigrams.txt', bigrams)
save_lists_to_file('trigrams.txt', trigrams)


    


    
        