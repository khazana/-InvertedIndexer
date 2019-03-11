# InvertedIndexer
Contains code for different types of indexers such as simple inverted indexer, positional indexer etc.

There are two paths 'path_to_raw_files' and 'path_to_tokenized_files' used throughout the project. 'path_to_raw_files' is a folder consisting of raw HTML webpages downloaded from the list of URLS given in BFS.txt. 'path_to_tokenized_files' consists of the tokenized and processed version of the same webpages.

This projects consists of four python files. Their functions are described as follows in the order they should be executed:

1.extract_list_of_terms.py - This code should be run first. This code when run creates list of unique unigrams, bigrams and trigrams from the corpus of all the documents given in BFS.txt. It saves each list to a text file called unigrams.txt, bigrams.txt and trigrams.txt in the project directory.

2.simple_inverted_indexer.py - This code creates three inverted indexes, one where terms consist of a single word, another on for terms consisting of two words, and the third index is for terms made up of three words. It saves the lists as text files under the folder InvertedLists as unigram_indexer.txt, bigram_indexer.txt and trigram_indexer.txt.

The code also saves the number of terms which occur in each document in a dictionary and saves that to a text file called 'term_count.txt'.

3.positional_indexer.py - This code creates a positional index using a dictionary for terms consisting of only one word. The key is the term and the value is of the form [(documentID1, [position1,position2]),(documentID2, [position1,position2])]. It contains a function to delta encode the positions and saves the encoded index to a file called 'encoded_positional_index.txt'. The code also has a function called ' conjuctive_proximity_query(term1,term2,w)' which returns a list of documents containing both the terms term1 and term2 if they occur only with a proximity window 'w'. It saves the required result lists for Task 2 to text files.

4.term_document_frequencies.py - This code generates a term frequency dictionary where the key is the term and value is the term frequency. It also has a function to generate document frequency dictionary where the key is the term and value is a list of tuples containing document IDs and document frequency. The output of this code is six text files. Two files for word
unigrams, two files for word bigrams, and two files for word trigrams. 

## Libraries used
Beautiful soup, os, json, collections, numpy, inspect, re, string, itertools, 

## Installation
 
This project requires Python 3.7.1 There are a few packages which have to be installed to be able to run the code. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install them as follows:


```bash
pip install bs4 
pip install nltk
pip install collections
```

## Usage

```bash
python extract_list_of_terms.py
python simple_inverted_indexer.py
python positional_indexer.py 
python term_document_frequencies.py
```

