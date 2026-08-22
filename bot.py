#pip install nltk
#pip install wikipedia
import nltk
nltk.download("wordnet")
nltk.download("omw-1.4")
from nltk.corpus import wordnet as wrdnet
key_convo = [
    (["hello","hey","helo","wassup","sup"], "Hello! How can I help you?"),
    (["hi","hii","yo"], "Hi! What's up? How can I help you today?"),
    (["how are you","how are you doing", "how is the josh"],"I'm doing great! How about you?"),
    (["what is your name","what you do","can you work","who are you","tell us about yourself"],"I'm a Python ChatBot Created by NishantSh122. I can talk to you and answer your questions to my capabilities.")
]
terminators = {"exit","bye","goodbye","cya","goodnight","close","shut up"}

question_wrds = {
    "what", "who", "where", "when", "why", "how", "define", "explain", "elaborate", "describe", "discuss", "generate", "tell"
}
starting_phrases = [
    "can you explain",
    "tell me about","do you know about",
    "what is","what are",
    "what was","who is",
    "who was","where is",
    "where was","when is","when was",
    "why is","why was",
    "how is","how does",
    "how do",
    "explain","describe"
]
pfp_phrase = {
    "my name",
    "who am i",
    "your opinion",
    "do you love",
    "do you like me"
}
define_phrase={
    "define", "what is the meaning of"
    "definition of", "what does"
    "meaning by", "meaning of"
}
#removing punctuations and unwanted spaces
def normalisation(text):
    text = text.strip() #remove space
    text= text.lower() #lowerspace
    for ch in ["?","!",".",",","'"]:
        text=text.replace(ch,"") #replacing the character with an empty character literal
    text = ' '.join(text.split()) #splitting large space and resulting in one string with just one space between characters
    return text

#checking question tags
def isfques(text):
    if not text:
        return False
    for phrase in pfp_phrase:
        if phrase in text:
            return False
    word_1 = text.split()[0]
    if word_1 in question_wrds:
        return True
    else:
        return False

#checking define quesiton tags
def isdques(text):
    for phrase in define_phrase:
        if text.startswith(phrase + " "):
            return True
    return False

#removing the question tags and leaving behind the keys to be searched up on wiki
def get_topics(text):
    for phrase in starting_phrases:
        prefix = phrase + " "
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
            break
    return text

#removing the definition question tags and leaving behind the keys to be searceh up on wordnet
def get_word(text):
    for phrase in define_phrase:
        prefix = phrase + " "
        if text.startswith(prefix):
            return text[len(prefix):].strip()
    return None

#adding nltk library to get a more good response for definintions of words.
def get_definition(text):
    synsets = wrdnet.synsets(text)
    if not synsets:
        return None
    definition = synsets[0].definition()
    exammple_sentences = synsets[0].examples()
    return definition, exammple_sentences

while True:
    user = input("You: ")
    user = normalisation(user)
    
    #terminating words
    if user in terminators:
        print("Bot: Goodbye!")
        break
    
    #key_word looker
    found = False
    for keywords, reply in key_convo:
        for keywrd in keywords: #runs till each element in keywords
            if keywrd in user:
                print("Bot:",reply)
                found = True
                break
        if found:
            break
    if found:
        continue
    
    #definition check
    if isdques(user):
        word = get_word(user)
        result = get_definition(word)
        if result is None:
            if isfques(user):
                    topic = get_topics(user)
                    print("Bot: User is asking about:", topic, " searching on wiki...")
                    continue
        else:
            define, example = result #adds result values of get_definiton(returns define and example)
            print("Bot:", define) #prints word and its sentence
            if example:
                print("The word can be used as : ", example[0])
        continue
    
    #ques check
    if isfques(user):
        topic = get_topics(user)
        print("Bot: User is asking about:", topic, " searching on wiki...")
        continue

    #if passes fails all the tests above then execute this at end;
    print("Bot: Sorry, I don't understand that yet.")
    