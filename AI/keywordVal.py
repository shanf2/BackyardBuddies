import math
from operator import itemgetter
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

def importantWords(post):

    # TF (Term Frequency) = Number of times a term t appears in the text / Total number of words in the document
    # ITF (Inverse Term Frequency) = log(total number of sentences / Number of sentences with term t)
    # TF-ITF = TF * ITF = More TF-ITF value, more important is the variable

    stop_words = set(stopwords.words('english')) 

    # Step 1 : Find total words in the document
    total_words = doc.split()
    total_word_length = len(total_words)

    # Step 2 : Find total number of sentences
    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)

    # Step 3: Calculate TF for each word
    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())

    # Check if a word is there in sentence list
    def check_sent(word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))

    # Step 4: Calculate ITF for each word
    itf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in itf_score:
                itf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                itf_score[each_word] = 1

    # Performing a log and divide
    itf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in itf_score.items())

    # Step 5: Calculating TF*ITF
    tf_itf_score = {key: tf_score[key] * itf_score.get(key, 0) for key in tf_score.keys()} 

    # Get top N important words in the document
    def get_top_n(dict_elem, n):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
        return result

    top = get_top_n(tf_itf_score, 5)
    return tf_score,tf_itf_score

# def testDisplay():
#     print("hello")
# 
# doc = 'I am a McMaster student. I am in my fourth year, doing my capstone project. For the capstone project, my team is doing a social media website. Planning to incoporate AI into the capstone project. My capstone group have five members. It is fun. Hello world.'
# output_top,out=importantWords(doc)
# print("out: ", out.keys())
# print("top: ", output_top)