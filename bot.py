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
    "how do","define",
    "explain","describe"
]
pfp_phrase = {
    "my name",
    "who am i",
    "your opinion",
    "do you love",
    "do you like me"
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

#removing the question tags and leaving behind the keys to be searched up on wiki
def get_topics(text):
    for phrase in starting_phrases:
        prefix = phrase + " "
        if(text.startswith(prefix)):
            text = text[len(prefix):].strip()
            break
    return text

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
    
    #ques check
    if isfques(user):
        topic = get_topics(user)
        print("Bot: User is asking about:", topic, " searching on wiki...")
        continue

    #if passes fails all the tests above then execute this at end;
    print("Bot: Sorry, I don't understand that yet.")
    