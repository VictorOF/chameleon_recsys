import numpy as np
import re
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.corpus import stopwords

from ..acr_commons import UNK_TOKEN, PAD_TOKEN


def nan_to_str(value):
    return '' if type(value) == float else value  

def get_words_freq(tokenized_articles, network='RNN'):
    if network == 'HAN':
        words_freq = FreqDist([word for article in tokenized_articles for sent in article for word in sent])
    else:
        words_freq = FreqDist([word for article in tokenized_articles for word in article])
    return words_freq    

def tokenize_text(text, clean_str_fn, lower_first_word_sentence=False):
    text = clean_str_fn(text)
    tokenized_text = []
    new_sentence = False
    for word in word_tokenize(text):
        if word in ['.', '?', '!']:
            new_sentence = True
        else:
            if lower_first_word_sentence and new_sentence:
                word = word.lower()
                new_sentence = False

        tokenized_text.append(word)

    return tokenized_text  

def tokenize_articles(articles, tokenization_fn=None, clean_str_fn=lambda x: x, sentence=False):
    if tokenization_fn == None:
        tokenized_articles = [tokenize_text(text, clean_str_fn) for text in articles]
    else:
        tokenized_articles = [tokenization_fn(text, sentence=sentence) for text in articles]
    return tokenized_articles

def print_vocab_tokens_stats(tokenized_int_texts, texts_lengths, word_vocab):
    print('# tokens by article stats - Mean: {:.1f}, Median: {:.1f}, Max: {:.1f}'.format(
          np.mean(texts_lengths), np.median(texts_lengths), np.max(texts_lengths))
         )

    if (sum(texts_lengths) == 0):
        perc_words_found_vocab = 0
    else:
        perc_words_found_vocab = (sum([len(list(filter(lambda word: word != word_vocab[UNK_TOKEN], doc))) for doc in tokenized_int_texts]) / \
                              float(sum(texts_lengths))) * 100
    print('{:.2f}%  tokens were found in vocabulary.'.format(perc_words_found_vocab))

def convert_tokens_to_int(tokenized_articles, word_vocab):
    
    def token_to_int(token):
        return word_vocab[token] if token in word_vocab else word_vocab[UNK_TOKEN] 

    texts_int = list([np.array([token_to_int(token) for token in article]) for article in tokenized_articles])
    texts_lengths = np.array([len(doc) for doc in texts_int])
    print_vocab_tokens_stats(texts_int, texts_lengths, word_vocab)

    return texts_int, texts_lengths

#beware: copied and modified code
def convert_sent_tokens_to_int(tokenized_articles, word_vocab):

    def token_to_int(token):
        return word_vocab[token] if token in word_vocab else word_vocab[UNK_TOKEN] 
    sent_int = []
    sent_shape = []
    pad_token_int = token_to_int(PAD_TOKEN)
    for article in tokenized_articles:
       if len(article) != 0:
           length = max(map(len, article))
           sent_numpy = np.array([[token_to_int(word) for word in sent] + [pad_token_int]*(length-len(sent)) for sent in article]) # make array with same lengh to all sentences in the article
           sent_int.append(sent_numpy.flatten())
           sent_shape.append(list(sent_numpy.shape))
       else:
           sent_int.append(np.array([]))
           sent_shape.append([0,0])
    # sent_int = list([np.array( [np.array([token_to_int(word) for word in sent]) for sent in article]) for article in tokenized_articles])
    # sent_lengths = np.array([len(article_sentences) for article_sentences in sent_int])
    
    return sent_int, sent_shape

