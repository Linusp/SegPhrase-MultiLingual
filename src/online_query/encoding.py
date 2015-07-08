# -*- coding: utf-8 -*-

from nltk.tokenize import WordPunctTokenizer
import codecs
import sys

punctuations = u'=^&#\\_*?/()[]{}<>%+-:.,;!|"\''

mapping = dict()

def main(argv):
    rawTextInput = 'rawText.txt'
    argc = len(argv)
    for i in xrange(argc):
        if argv[i] == "-i" and i + 1 < argc:
          rawTextInput = argv[i + 1]
        elif argv[i] == "-o" and i + 1 < argc:
          tokenizedFile = argv[i + 1]
        elif argv[i] == "-map" and i + 1 < argc:
          mappingFile = argv[i + 1]
        elif argv[i] == "-offset" and i + 1 < argc:
          offsetFile = argv[i + 1]
    with codecs.open(mappingFile, encoding='utf-8', mode='r') as input:
        for line in input:
            elements = line.rstrip().split(',')
            mapping[elements[1]] = elements[0]

    outputA = codecs.open(tokenizedFile, encoding='utf-8', mode='w')
    outputB = codecs.open(offsetFile, encoding='utf-8', mode='w')
    for line in codecs.open(rawTextInput, encoding='utf-8', mode='r'):
        offsets = []
        line = line.rstrip()
        spans = list(WordPunctTokenizer().span_tokenize(line))
        # result = WordPunctTokenizer().tokenize(line)
        newline = []
        for tk in spans:
            begin = tk[0]
            end = tk[1]
            tk = line[begin:end]
            if tk == ' ':
                newline.append(' ')
                continue
            if tk in punctuations:
                newline.append(tk)
                newline.append(' ')
                continue
            tk = ''.join([i for i in tk if not i.isdigit() and i not in punctuations]).lower()
            if len(tk) == 0:
                newline.append(' ')
                continue
            if tk not in mapping:
                newline.append('zzzzzzzzzzz')
            else:
                newline.append(mapping[tk])
                offsets.append((tk, begin, end))
            newline.append(' ')
        outputA.write(u''.join(newline).encode('utf8'))
        outputA.write('\n')
        for (string, begin, end) in offsets:
            outputB.write(string)
            outputB.write(',')
            outputB.write(str(begin))
            outputB.write(',')
            outputB.write(str(end))
            outputB.write('\t')
        outputB.write('\n')

if __name__ == "__main__":
    main(sys.argv[1 : ])