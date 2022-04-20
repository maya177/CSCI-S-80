import nltk
import sys
import string
import math
import os

# python questions.py corpus

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # creates dictionary to mapp filename of each '.txt' file
    dictionary = {}

    # opens each file in diretory
    for file in os.listdir(directory):
        # maps files
        with open(os.path.join(directory, file), encoding="utf-8") as ofile:
            dictionary[file] = ofile.read()

    return dictionary


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # defines stopwords from nltk stopwords
    stop_words = nltk.corpus.stopwords.words("english")

    # tokenizes words in document with nltk's word_tokenizer after converting all words to lowercase
    tokens = nltk.tokenize.word_tokenize(document.lower())
    # removes punctuation and English stopworks from tokens
    tokens = [token for token in tokens if token not in string.punctuation and token not in stop_words]
    
    return tokens

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # creates a dictionary to store idfs
    idf_dict = {}

    # defines length of document
    len_doc = len(documents)

    # defines words as names of documents
    words = set(sum(documents.values(), []))

    # iterates through words in the names of documents
    for word in words:

        word_count = 0

        # iterates through documents
        for doc in documents.values():
            # counts the number of word in all documents
            if word in doc:
                word_count += 1

        # calculates idf value 
        idf_dict[word] = math.log(len_doc/word_count)

    return idf_dict

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # creates dictionary to store the sum of tf-idf values
    file_scores = {}

    # iterates through all files, words in the files (dictionary)
    for file, words in files.items():
        #the score is the sum of tf-idf values
        tf_idf_score = 0
        # iterates through each word in the set of words
        for word in query:
            # calculates score for each word 
            tf_idf_score += words.count(word)*idfs[word]
        # adds scores to dictionary
        file_scores[file] = tf_idf_score

    # ranks files according to tf-idf 
    ranked_files = [x[0] for x in sorted(file_scores.items(), key=lambda x: x[1], reverse=True)]

    # returns n top files that match the query
    return ranked_files[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # creates dictionary to store idf scores and term density 
    scores = {}

    # iterates through all sentences, word in sentences
    for sentence, words in sentences.items():
        idf_score = 0
        # iterates through each word in set of words
        for word in query:
            # calculates idf_score for the word
            idf_score += idfs[word]
        # to prevent uneccesary calculations
        if idf_score != 0:
            # calculats term density 
            density = sum([words.count(x) for x in query])/len(words)
            # appends idf score and density to dictionary
            scores[sentence] = (idf_score, density)

    # ranks sentences according to idf
    ranked_sentences = [x[0] for x in sorted(scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]
    
    # returns n top sentences
    return ranked_sentences[:n]

if __name__ == "__main__":
    main()
