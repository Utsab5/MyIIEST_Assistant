import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer=WordNetLemmatizer()
intents=json.loads(open('intents.json').read())

#"rb" => reading in binary mode
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('chatbot_model.model')

# to clean up sentences
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]

    return sentence_words


#to convert sentence into a bag of word    
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag= [0]* len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i]=1


    # Check if the bag length matches the expected input size
    if len(bag) != len(words):
        diff = len(words) - len(bag)
        bag.extend([0] * diff)            

    return np.array(bag)   


def predict_class(sentence):
    bow = bag_of_words((sentence))
    res=model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list=[]
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability': str(r[1])})
    return return_list   


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break 

    return result



###################
def chat(message):
    # message = input("")
    
    ints = predict_class(message)
    
    res = get_response(ints, intents)
    return res



# print("GO! Bot is ready!")

# while True:
#     msg = input("")
    
#     print(chat(msg))    

