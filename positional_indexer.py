import os
import numpy
import inspect


#dictionary which maps each unigram term to a a list of tuples 
#where a tuple is of the form (docID , [position1,position2])
position_terms = {}

#same as 'position_terms ' but contains positions encoded with delta encoding
encoded_position_terms = {}
unigrams_list = []
path_to_corpus_folder = "/Users/fathimakhazana/Documents/IRHW3/ParsedTextFiles/"

#create unigrams list from text file
def get_unigrams_list():
    f = open('Task1/TermFiles/unigrams.txt', 'r')
    unigrams = f.readlines()
    for word in unigrams:
        unigrams_list.append(word.strip())
    f.close()


#function which returns variable name as string as a list
#https://stackoverflow.com/a/18425523/8933813
def get_var_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [k for k, v in callers_local_vars if v is var]

def get_document_ID(file):
      docID = file.split(path_to_corpus_folder)
      docID = docID[1]
      docID = docID.split('.txt')[0]
      return docID

#process the corpus to extract tokens as a list   
def process_corpus(x):
     x = x[0]
     x = x.replace(']','')
     x = x.replace('[','')
     x = x.split(", ")
     return x


#function which adds positions of a unigram present in the passed corpus
#as a value in 'position_terms' with the unigram as key 
def find_term_positions_in_document(file):
     corpuslist = []
     f = open(file, 'r')
     x = f.readlines()
     f.close()
     docID = get_document_ID(file)
     corpus = process_corpus(x)
     for token in corpus:
         token = token.replace("'",'')
         corpuslist.append(token) 
     for unigram in unigrams_list:
         positions = [i for i,x in enumerate(corpuslist) if x == unigram]
         if len(positions) > 0:
             position_terms.setdefault(unigram,[]).append((docID, positions))


#main function to fetch positions of all unigrams in all documents         
def create_positional_index():
    files = [i for i in os.listdir(path_to_corpus_folder) if i.endswith(".txt")]
    for file in files:
        find_term_positions_in_document(path_to_corpus_folder + file)


def write_dict_to_file(file_name,dictionary):
     with open(file_name, "a") as f:
         f.writelines('{}:{} \n'.format(k,v) for k, v in dictionary.items())  

def write_list_to_file(result):
    file = get_var_name(result)[0]
    with open(file + '.txt', "w") as f:
         for item in result:
             f.write("%s\n" % item)

#used when required
def read_dict_from_file():
    lines = open('positional_index.txt').readlines()
    for line in lines:
        line = line.strip()
        key,value = line.split(':')
        values_list = eval(value)
        for val in values_list:
            position_terms.setdefault(key,[]).append(val)

#delta encode the positions in 'position terms' for all documents of all terms 
def delta_encode_index():
        for k,v in position_terms.items():
            encoded_position_terms.setdefault(k,[])
            for i in range(len(v)):
                docID = v[i][0]
                positions_list = v[i][1]
                if len(positions_list) > 1:
                    new_list = numpy.empty(len(positions_list), dtype=object)
                    for j in range(len(positions_list) - 1,0,-1):
                        new_list[j] = positions_list[j] - positions_list[j-1]
                    new_list[0]  = positions_list[0]
                    encoded_position_terms.setdefault(k,[]).append((docID, new_list))
                
                else:
                    encoded_position_terms.setdefault(k,[]).append((docID, positions_list))

            
#returns a decoded list 
def decode_lists(encoded_list):
    decoded_list =numpy.empty(len(encoded_list), dtype=object)
    decoded_list[0] =  encoded_list[0]   
    for j in range(0,len(encoded_list) -1):
        decoded_list[j+1] = decoded_list[j] + encoded_list[j+1]
    return list(decoded_list)
               

#return list of document IDs which contain both term1 and term2 within a window of 'w' words apart          
def conjuctive_proximity_query(term1,term2,w):
    term1_query = []
    term2_query = [] 
    result_docs = [] 
    term1_list = encoded_position_terms[term1]
    term2_list = encoded_position_terms[term2]
    #finds two encoded lists containing only same documents 
    if (len(term1_list) > 0 and len(term2_list) > 0):
        if len(term1_list) > len(term2_list):
            for i in range(len(term1_list)):
                for j in range(len(term2_list)):
                    if term1_list[i][0] == term2_list[j][0]:
                        term1_query.append(term1_list[i])
                        term2_query.append(term2_list[j])
        else:
                for i in range(len(term2_list)):
                    for j in range(len(term1_list)):
                        if term2_list[i][0] == term1_list[j][0]:
                            term1_query.append(term1_list[j])
                            term2_query.append(term2_list[i]) 
        #find positions within w
        for x in range(len(term1_query)):
            #both lists contain single term-no need to decode
            if len(term1_query[x][1]) == 1 and len(term2_query[x][1]) == 1:
                if (abs(term1_query[x][1][0] - term2_query[x][1][0]) <= w):
                    result_docs.append(term2_query[x][0])
            #need to decode for longer lists
            else:
                 decoded_term1_list = decode_lists(term1_query[x][1])
                 decoded_term2_list = decode_lists(term2_query[x][1])
                 #process with shorter list first
                 if(len(decoded_term1_list) < len(decoded_term2_list)):
                     for d in range(len(decoded_term1_list)):
                         for element in range(decoded_term1_list[d] - w, decoded_term1_list[d] + w + 1):
                             if element in decoded_term2_list:
                                 if term2_query[x][0] not in result_docs:
                                     result_docs.append(term2_query[x][0])
                             
                 else:
                     for d in range(len(decoded_term2_list)):
                         for element in range(decoded_term2_list[d] - w, decoded_term2_list[d] + w + 1):
                             if element in decoded_term1_list:
                                 if term1_query[x][0] not in result_docs:
                                     result_docs.append(term1_query[x][0])  
        return result_docs
            
    else:
         return "No results found!"
            
                        
    
def task2b():
    space_mission_k6 = conjuctive_proximity_query('space','mission',6)
    space_mission_k12 = conjuctive_proximity_query('space','mission',12)
    earth_orbit_k5 = conjuctive_proximity_query('earth','orbit',5)
    earth_orbit_k10 = conjuctive_proximity_query('earth','orbit',10)
    write_list_to_file(space_mission_k6)
    write_list_to_file(space_mission_k12)
    write_list_to_file(earth_orbit_k5)
    write_list_to_file(earth_orbit_k10)
                   
                    
   
    
create_positional_index()
delta_encode_index()
write_dict_to_file('encoded_positional_index.txt',encoded_position_terms)
task2b()

