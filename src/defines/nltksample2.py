import csv
import random
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer


greet_in = ('hey', 'sup', 'waddup', 'wassup', 'hi', 'hello', 'good day','ola', 'bonjour', 'namastay', 'hola', 'heya', 'hiya', 'howdy',
'greetings', 'yo', 'ahoy')
greet_out = ['hey', 'hello', 'hi there', 'hi', 'heya', 'hiya', 'howdy', 'greetings', '*nods*', 'ola', 'bonjour', 'namastay']
def greeting(sent):
   for word in sent.split():
      if word.lower() in greet_in:
         return random.choice(greet_out)
        
        
small_talk_responses = {
'how are you': 'I am fine. Thankyou for asking ',
'how are you doing': 'I am fine. Thankyou for asking ',
'how do you do': 'I am great. Thanks for asking ',
'how are you holding up': 'I am fine. Thankyou for asking ',
'how is it going': 'It is going great. Thankyou for asking ',
'goodmorning': 'Good Morning ',
'goodafternoon': 'Good Afternoon ',
'goodevening': 'Good Evening ',
'good day': 'Good day to you too ',
'whats up': 'The sky ',
'sup': 'The sky ',
'thanks': 'Dont mention it. You are welcome ',
'thankyou': 'Dont mention it. You are welcome ',
'thank you': 'Dont mention it. You are welcome '
}
small_talk = small_talk_responses.values()
small_talk = [str (item) for item in small_talk]

def tfidf_cosim_smalltalk(doc, query):
   query = [query]
   tf = TfidfVectorizer(use_idf=True, sublinear_tf=True)
   tf_doc = tf.fit_transform(doc)
   tf_query = tf.transform(query)
   cosineSimilarities = cosine_similarity(tf_doc,tf_query).flatten()
   related_docs_indices = cosineSimilarities.argsort()[:-2:-1]
   if (cosineSimilarities[related_docs_indices] > 0.7):
      ans = [small_talk[i] for i in related_docs_indices[:1]]
      return ans[0]
    
    
def naming(name):
   a = name.split()
   if('my name is' in name):
      for j in a:
         if(j!='my' and j!= 'name' and j!='is'):
            return j
   elif('call me' in name):
      for j in a:
         if(j!='call' and j!= 'me'):
            return j
   elif('name is' in name):
      for j in a:
         if(j!= 'name' and j!='is'):
            return j
   elif('change my name to' in name):
      for j in a:
         if(j!= 'change' and j!='my' and j!= 'name' and j!='to'):
            return j
   elif('change name to' in name):
      for j in a:
         if(j!= 'name' and j!= 'name' and j!='to'):
            return j
   else:
      return name
    
