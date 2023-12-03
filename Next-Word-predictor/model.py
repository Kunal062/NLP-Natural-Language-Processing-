import nltk
# nltk.download('all')
nltk.download(['nps_chat', 'punkt'])
import re
from nltk.tokenize import sent_tokenize, TweetTokenizer
from collections import defaultdict, Counter
from nltk.corpus import nps_chat
from xml.etree import ElementTree as ET
from nltk.probability import ConditionalFreqDist
from itertools import chain
import matplotlib.pyplot as plt

# default configurations
plt.rcParams["font.size"] = 9

# model
class MarkovChainBackoff:
  def __init__(self):
    self.lookup_dict = defaultdict(list)
    self.cfdist = ConditionalFreqDist()
    self.tweet_tokenizer = TweetTokenizer()
    
  def add_document_line(self, data, preprocessed=False):
    if not preprocessed:
      preprocessed_list = self._preprocess(data)
    else:
      preprocessed_list = data
    pairs = self.__generate_ntuple_keys(preprocessed_list, 1)
    for pair in pairs:
      self.lookup_dict[pair[0]].append(pair[1])
    pairs2 = self.__generate_ntuple_keys(preprocessed_list, 2)
    for pair in pairs2:
      self.lookup_dict[tuple([pair[0], pair[1]])].append(pair[2])
    pairs3 = self.__generate_ntuple_keys(preprocessed_list, 3)
    for pair in pairs3:
      self.lookup_dict[tuple([pair[0], pair[1], pair[2]])].append(pair[3])
  
  def _preprocess(self, string):
    cleaned = re.sub('\d{1,2}-\d{1,2}-\w+', ' ', string).lower()
    cleaned = re.sub('u\d+', ' ', cleaned)
    cleaned = re.sub("[^a-zA-Z']+", ' ', cleaned)
    tokenized = self.tweet_tokenizer.tokenize(text=cleaned)
    return tokenized

  def __generate_ntuple_keys(self, data, n):
    if len(data) < n:
      return

    for i in range(len(data) - n):
      tuple_keys = [ data[i+x] for x in range(n+1) ]
      yield tuple_keys
      
  def suggestion_helper(self, gram_list, suggested):
    # using occurence prioritizing higher ngrams predictions
    # new_suggestions = Counter(self.lookup_dict[gram_list]).most_common()[:3-len(suggested)]
    # new_suggestions = [x for x in new_suggestions if (x[0] not in [y[0] for y in suggested])]
    # suggest = suggested + new_suggestions
    
    # using probability
    new_suggestions = self.cfdist[gram_list]
    print('\n', new_suggestions)
    suggest = sorted(suggested + [x for x in new_suggestions if (x[0] not in [y[0] for y in suggested])], 
                     key = lambda x: x[1], 
                     reverse=True)[:3]
    return suggest
    
    
  def oneword(self, gram_list, suggested=[]):
    suggest = self.suggestion_helper(gram_list[-1], suggested)
    return suggest

  def twowords(self, gram_list, suggested=[]):
    suggest = self.suggestion_helper(tuple(gram_list), suggested)
    if len(suggest) < 3:
        return self.oneword(gram_list[-1:], suggest)
    return suggest

  def threewords(self, gram_list, suggested=[]):
    suggest = self.suggestion_helper(tuple(gram_list), suggested)
    if len(suggest) < 3:
        return self.twowords(gram_list[-2:], suggest)
    return suggest
    
  def morewords(self, gram_list):
    return self.threewords(gram_list[-3:], [])

    
  def generate_suggestion(self, string):
    suggestions = []
    if len(self.lookup_dict) > 0:
        tokens = self._preprocess(string)
        if len(tokens)==1:
            suggestions = self.oneword(tokens)
        elif len(tokens)==2:
            suggestions = self.twowords(tokens)
        elif len(tokens)==3:
            suggestions = self.threewords(tokens)
        elif len(tokens)>3:
            suggestions = self.morewords(tokens)
        return suggestions
    return suggestions
    
  def plot_fd(self, n):
    ntuple_keys = []
    for key, val in self.lookup_dict.items():
        if (isinstance(key, tuple) and len(key)==n) or (isinstance(key, str) and n==1):
            ntuple_keys.append([key]*len(val))

    # chain will flatten the nested arrays
    fdist = nltk.FreqDist(list(chain(*ntuple_keys)))
    # print("Most common ngrams: ", fdist.most_common(10))
    
    # plotting
    fig = plt.figure(figsize = (15,10))
    plt.gcf().subplots_adjust(bottom=0.15) # to avoid x-ticks cut-off
    fdist.plot(30, cumulative=False)
    # plt.show()
    fig.tight_layout()
    # fig.savefig('freqDist.png', bbox_inches = "tight")
    
  def set_cfd(self):
    # make conditional frequencies dictionary
    for key, val in self.lookup_dict.items():
        self.cfdist[key] = Counter(val).most_common()
    
    # transform frequencies to probabilities
    for key in self.cfdist:
        total_count = float(sum([x[1] for x in self.cfdist[key]]))
        for idx, (w, c) in enumerate(self.cfdist[key]):
            self.cfdist[key][idx] = (w, c / total_count)

# initialize
predictor = MarkovChainBackoff()

# for other words
with open('corpus.txt', encoding="utf8") as fp:
  contents = fp.readlines()
  for para in contents:
    sentences = sent_tokenize(para)
    for sentence in sentences:
        predictor.add_document_line(sentence)

# for slang word and abbreviations
for item in ['10-19-20s_706posts.xml', '10-19-30s_705posts.xml', '10-19-40s_686posts.xml', '10-19-adults_706posts.xml', '10-24-40s_706posts.xml', '10-26-teens_706posts.xml', '11-06-adults_706posts.xml', '11-08-20s_705posts.xml', '11-08-40s_706posts.xml', '11-08-adults_705posts.xml', '11-08-teens_706posts.xml', '11-09-20s_706posts.xml', '11-09-40s_706posts.xml', '11-09-adults_706posts.xml', '11-09-teens_706posts.xml']:
  root = nps_chat.xml(item)
  for post in root.findall('.//*/Post'):
    if not post.attrib['class']=='System':
      sentences = sent_tokenize(post.text.strip())
      for sentence in sentences:
        predictor.add_document_line(sentence)

# plotting
predictor.plot_fd(1)
predictor.plot_fd(2)
predictor.plot_fd(3)
predictor.set_cfd()

# for Tkinter app, comment the below code
# while True:
#   text = input()
#   if (text==''):
#     break
#   print(predictor.generate_suggestion(text.strip().lower()))
