# Next - Word Predictor
## Using N-grams

This project is completely built on python. The UI design is made similar to Gboard. I know it looks poor😅.
N-Grams in NLP is a concept which uses 'n' to 1 previous words to predict the next word.
N-gram is probably the easiest concept to understand in the whole machine learning space, I guess. An N-gram means a sequence of N words. So for example, “Drink Coffee” is a 2-gram (a bigram), “Want to drink coffee” is a 4-gram, and “to drink coffee” is a 3-gram (trigram).

Why N-gram though?
In Natural Language Processing, or NLP for short, n-grams are used for a variety of things. Some examples include auto completion of sentences (such as the one we see in Gmail these days), auto spell check (yes, we can do that as well), and to a certain extent, we can check for grammar in a given sentence.

N-gram Probabilities
Let’s take the example of a sentence completion system. This system suggests words which could be used next in a given sentence. Suppose I give the system the sentence “Thank you so much for your” and expect the system to predict what the next word will be. Now you and me both know that the next word is “help” with a very high probability. But how will the system know that?

One important thing to note here is that, as for any other artificial intelligence or machine learning model, we need to train the model with a huge corpus of data. Once we do that, the system, or the NLP model will have a pretty good idea of the “probability” of the occurrence of a word after a certain word. So hoping that we have trained our model with a huge corpus of data, we’ll assume that the model gave us the correct answer.

We’re calculating the probability of word “w1” occurring after the word “w2,” then the formula for this is as follows:
   --> count(w2 w1) / count(w2)
which is the number of times the words occurs in the required sequence, divided by the number of the times the word before the expected word occurs in the corpus.
