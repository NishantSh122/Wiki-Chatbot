key_convo = {
    "hello" : "Hello! How can I help you?",
    "hi": "Hi! Nice to meet you.",
    "how are you" : "I'm doing great!",
    "what is your name": "I'm a python chatbot."
}
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
    normalisation(user)
    
    #terminating words
    if user in terminators:
        print("Bot: Goodbye!")
        break
    
    #key_word looker
    found = False
    for keyword in key_convo:
        if keyword in user:
            print("Bot:",key_convo[keyword])
            found = True
            break
    if not found:
        print("Bot: Sorry, I don't understand that yet.")