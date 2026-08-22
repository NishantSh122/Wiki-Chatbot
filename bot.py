key_convo = [
    (["hello","hey","helo","wassup","sup"], "Hello! How can I help you?"),
    (["hi","hii","yo"]),
    (["how are you","how are you doing", "how is the josh"],"I'm doing great! How about you?"),
    (["what is your name","what you do","can you work","who are you","tell us about yourself","I'm a Python ChatBot Created by NishantSh122. I can talk to you and answer your questions to my capabilities."])
]
terminators = {"exit","bye","goodbye","cya","goodnight","close","shut up"}

#removing punctuations and unwanted spaces
def normalisation(text):
    text = text.strip() #remove space
    text= text.lower() #lowerspace
    for ch in ["?","!",".",",","'"]:
        text=text.replace(ch,"") #replacing the character with an empty character literal
    text = ' '.join(text.split()) #splitting large space and resulting in one string with just one space between characters
    
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
        for keywords in keywords: #runs till each element in keywords
            if keywords in user:
                print("Bot:",key_convo[keywords])
                found = True
                break
    if not found:
        print("Bot: Sorry, I don't understand that yet.")