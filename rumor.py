# coding: utf-8

import sys
import jieba
#  import math
jieba.load_userdict('user_dict.txt')
import numpy
from sklearn import metrics
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.naive_bayes import MultinomialNB


def input_data(train_file, test_file):
    train_words = []
    train_tags = []
    test_words = []
    test_tags = []
    with open(train_file, 'r') as f1:
        for line in f1:
            tks = line.split('\t')
            if len(tks) != 2:
                continue
            train_words.append(tks[1])
            train_tags.append(tks[0])

    with open(test_file, 'r') as f1:
        for line in f1:
            tks = line.split('\t')
            if len(tks) != 2:
                continue
            test_words.append(tks[1])
            test_tags.append(tks[0])
    return train_words, train_tags, test_words, test_tags


with open('stopwords.txt', 'r') as f:
    stopwords = list([w.strip().decode('utf-8') for w in f])

comma_tokenizer = lambda x: jieba.cut(x, cut_all=True)


def vectorize_1(train_words, test_words):
    v = HashingVectorizer(tokenizer=comma_tokenizer, stop_words=stopwords, n_features=100000, non_negative=True)
    train_data = v.fit_transform(train_words)
    #  print train_data
    test_data = v.fit_transform(test_words)
    return train_data, test_data


def check_neg(input_words_list):
    neg_list = [u'不', u'没有', u'不会', u'不可能', u'不是', u'不想', u'不爱', u'不喜欢', u'没', u'并不', u'不能', u'不好']
    count = 0
    for words in input_words_list:
        if words in neg_list:
            count += 1

    if count % 2 == 1:
        return True
    else:
        return False


def vectorize_2(test_words):
    input_words = jieba.lcut(test_words[0])
    print check_neg(input_words)

    #  if len(jieba.lcut(test_words[0])) < 2:
    if len(jieba.lcut(test_words[0])) < 2:
        return None, False
    else:
        v = HashingVectorizer(tokenizer=comma_tokenizer, stop_words=stopwords, n_features=100000, non_negative=True)
        test_data = v.fit_transform(test_words)
        print test_data
        return test_data, check_neg(input_words)


def evaluate(actual, pred):
    m_precision = metrics.precision_score(actual, pred)
    m_recall = metrics.recall_score(actual, pred)
    print 'precision:{0:.3f}'.format(m_precision)
    print 'recall:{0:0.3f}'.format(m_recall)


def train_clf(train_data, train_tags):
    clf = MultinomialNB(alpha=0.01)
    clf.fit(train_data, numpy.asarray(train_tags))
    return clf


class Rumor_text(object):
    def __init__(self, polarity, subjectivity):
        self.polarity=polarity
        self.subjectivity=subjectivity


def PreLoading():
    train_file = './final_file.txt'
    test_file = './final_test.txt'
    train_words, train_tags, test_words, test_tags = input_data(train_file, test_file)
    train_data, test_data = vectorize_1(train_words, test_words)
    clf = train_clf(train_data, train_tags)
    return clf


def RumorJudges(message, clf):
    [test_data, neg_mark] = vectorize_2([message])

    if test_data is None:
        return Rumor_text(1, 0)
    else:
        result_list = clf.predict_proba(test_data).tolist()[0]
        if neg_mark is True:
            if result_list[1] > 0.9:
                rumor_obj = Rumor_text(1 - result_list[1], result_list[0])
            else:
                rumor_obj = Rumor_text(0.9 - result_list[1], result_list[0])
        else:
            rumor_obj = Rumor_text(result_list[1], result_list[0])
        return rumor_obj


def Add(label, content):
    with open('./final_file.txt', 'a') as append_file:
        append_file.write(str(label)+ '\t'+ content + '\n')
    return "wrote!"


def main():
    if len(sys.argv) < 3:
        print '[Usage]: python classifier.py train_file test_file'
        sys.exit(0)
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    train_words, train_tags, test_words, test_tags = input_data(train_file, test_file)
    train_data, test_data = vectorize_1(train_words, test_words)
    clf = train_clf(train_data, train_tags)
    while 1:
        dd = raw_input("Input your words: ")
        test_data = vectorize_2([dd.decode('utf-8')])
        print clf.predict_proba(test_data).tolist()[0][1]


if __name__ == '__main__':
    main()
