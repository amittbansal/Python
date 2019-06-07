# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 01:03:12 2016

@author: Amimac
"""

import textmining
import numpy as np
import lda

def term_document_matrix():
    with open("test.txt") as file:
        reading_file_line = file.readlines() 
        reading_file_info = [item.rstrip('\n') for item in reading_file_line]
        
    tdm = textmining.TermDocumentMatrix()    
    tdm.add_doc(' '.join(reading_file_info)) 
    temp = list(tdm.rows(cutoff=1))
    vocab = tuple(temp[0])

    X=np.array(temp[1:])

    model = lda.LDA(n_topics=25, n_iter=2000, random_state=1)
    model.fit(X)

    topic_word = model.topic_word_ 
    n_top_words = 10
    
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
        
term_document_matrix()        