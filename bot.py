#pip install nltk
#pip install wikipedia
#pip install requests
from datetime import datetime
import requests
import difflib
import nltk
nltk.download("wordnet")
nltk.download("omw-1.4")
from nltk.corpus import wordnet as wrdnet

WIKI_SEARCH_URL = "https://en.wikipedia.org/w/api.php"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WTTR_URL = "https://wttr.in"
memory={
    "name": None,
    "age": None,
    "address": None,
    "work": None
}
key_convo = [
    (["hello","hey","helo","wassup","sup"], "Hello! How can I help you?"),
    (["hi","hii","yo"], "Hi! What's up? How can I help you today?"),
    (["how are you","how are you doing", "how is the josh"],"I'm doing great! How about you?"),
    (["what is your name","what you do","can you work","who are you","tell us about yourself"],"I'm a Python ChatBot Created by NishantSh122. I can talk to you and answer your questions to my capabilities.")
]
terminators = {"exit","bye","goodbye","cya","good night","goodnight","close","shut up"}
weather_states = {
    "andhra pradesh",
    "arunachal pradesh",
    "assam",
    "bihar",
    "chhattisgarh",
    "goa",
    "gujarat",
    "haryana",
    "himachal pradesh",
    "jharkhand",
    "karnataka",
    "kerala",
    "madhya pradesh",
    "maharashtra",
    "manipur",
    "meghalaya",
    "mizoram",
    "nagaland",
    "odisha",
    "punjab",
    "rajasthan",
    "sikkim",
    "tamil nadu",
    "telangana",
    "tripura",
    "uttar pradesh",
    "uttarakhand",
    "west bengal"
}
weather_tags = {
    "weather", "temperature","climate","forecast"
}
location_markers = [" in ", " at ", " for ", " of ", " near "]
trailing_noise = {"today","now","right","now?","currently","please","tomorrow","tonight"}
time_tags={
    "time", "clock", "current time"
}
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
define_phrase={
    "define", "what is the meaning of",
    "definition of", "what does",
    "meaning by", "meaning of"
}

#fetching name for the user data
def get_name(text):
    phrases= [
        "my name is",
        "i am", "i'm"
    ]
    for phrase in phrases:
        if text.startswith(phrase + " "):
            name = text[len(phrase):].strip()
            if name:
                return name
    return None

#fetching user age for data
def get_age(text):
    words = text.split()
    if text.startswith("my age is "):
        age = text[len("my age is "):].strip()
        age = age.replace(" years old", "")
        age = age.replace(" years", "")
        age = age.replace(" year old", "")
        age = age.replace(" year", "")
        if age.isdigit():
            return int(age)
    if text.startswith("i am "):
        age = text[len("i am "):].strip()
        age = age.replace(" years old", "")
        age = age.replace(" years", "")
        age = age.replace(" year old", "")
        age = age.replace(" year", "")
        if age.isdigit():
            return int(age)
    return None

#fetching address
def get_address(text):
    if text.startswith("my address is"):
        return text[len("my address is"):].strip()
    if text.startswith("i live in"):
            return text[len("i live in"):].strip()
    return None

#data collecting center
def memory_response(text):
    if "what is my name" in text or "what's my name" in text:
        if memory["name"] is not None:
            return "your name is " + memory["name"] + "."
        return "I don't know your name yet."
    if "who am i" in text:
        if memory["name"] is not None:
            return "You are " + memory["name"] + "."
        return "I don't know your name yet."
    if "how old am i" in text:
        if memory["age"] is not None:
            return "You are " + str(memory["age"]) + " years old."
        return "I don't know your age yet."
    if "what is my age" in text:
        if memory["age"] is not None:
            return "You are " + str(memory["age"]) + " years old."
        return "I don't know your age yet."
    if "what is my address" in text:
        if memory["address"] is not None:
            return "Your address is " + memory["address"] + "."
        return "I don't know your address yet."
    if "where do i live" in text:
        if memory["address"] is not None:
            return "Your address is " + memory["address"] + "."
        return "I don't know your address yet."
    return None

#removing punctuations and unwanted spaces
def normalisation(text):
    text = text.strip().lower() #remove space #lowerspace
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
headers = {
    'User-Agent': 'PythonBot/1.0 (contact@example.com)'
}

#searching the word
def look_wiki(topic):
    try:
        response_wiki = requests.get(
            WIKI_SEARCH_URL,
            headers=headers,
            params = {
                "action":"query",
                "list":"search",
                "srsearch": topic,
                "srlimit":5,
                "format":"json"
            },
            timeout=10
        )
        response_wiki.raise_for_status()
        data = response_wiki.json()
        results = data.get("query",{}).get("search",[])
        titles=[result["title"] for result in results]
        return titles
    except requests.exceptions.RequestException as e:
        print("API Error:", e)
        return None

#chosing the top topic for the user
def top_wiki_title(topic, titles):
    if not titles:
        return None
    lower_titles = [t.lower() for t in titles]
    matches = difflib.get_close_matches(
        topic.lower(),
        lower_titles,
        n=1, #selecting the first topic for the wiki search/summary
        cutoff=0.5 #no results that are way too off --> feature of bot
    )
    if matches:
        matched_index = lower_titles.index(matches[0])
        return titles[matched_index]
    return None

#using the above method and getting summary
def get_sumry(title):
    concatenated_title = requests.utils.quote(title,safe="")
    url = ("https://en.wikipedia.org/api/rest_v1/page/summary/" + concatenated_title)
    try:
        response = requests.get(
            url,headers = headers, timeout=10
        )
        response.raise_for_status()
        data=response.json()
        return data.get("extract") #wikipedia response name (default)
    except requests.exceptions.RequestException:
        return None

#final call directly to the wikipedia
def get_wikipedia(topic):
    titles = look_wiki(topic)
    if titles is None:
        return None
    if not titles:
        return None
    title = top_wiki_title(
        topic,titles
    )
    if title is None:
        return None
    sumry = get_sumry(title)
    if sumry is None:
        return None
    if isAmbiguity(sumry):
        return None
    return title, sumry

#removing ambiguity of words
def isAmbiguity(sumry):
    if not sumry:
        return True
    if "may refer to:" in sumry.lower() and len(sumry)<200:
        return True
    return False

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

#weather detecting 
def isweather(text):
    for tags in weather_tags:
        if tags in text:
            return True
    return False

#getting location data
def get_location(text):
    padded = " " + text + " "
    best_idx = -1
    best_marker_len = 0
    for marker in location_markers:
        idx = padded.find(marker)
        if idx != -1 and (best_idx == -1 or idx < best_idx):
            best_idx = idx
            best_marker_len = len(marker)
    if best_idx == -1:
        return None
    location = padded[best_idx + best_marker_len:].strip()
    for tag in weather_tags:
        location = location.replace(tag, "").strip()
    words = [w for w in location.split() if w not in trailing_noise]
    location = " ".join(words)
    return location if location else None

#getting weather details
def get_mausam(place):
    try:
        response = requests.get(
            WTTR_URL + "/" + requests.utils.quote(place),
            params={"format": "j1"},
            headers=headers, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        current = data.get("current_condition", [None])[0]
        area = data.get("nearest_area", [None])[0]
        if current is None:
            return None, None
        resolved_name = None
        if area:
            area_name = area.get("areaName", [{}])[0].get("value")
            region = area.get("region", [{}])[0].get("value")
            resolved_name = area_name if area_name else region
        return current, resolved_name
    except requests.exceptions.RequestException as e:
        print("Weather API Error:", e)
        return None, None

#decoding the weather codes
def weather_decoder(code):
    weather_codes ={
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(code,"Weather condition unavailable")

#giving back all weather data 
def weather_response(place):
    result, resolved_name = get_mausam(place)
    if result is None:
        return None
    temperature = result.get("temperature_2m")
    humidity = result.get("relative_humidity_2m")
    wind = result.get("wind_speed_10m")
    code = result.get("weather_code")
    condition = weather_decoder(int(code)) if code is not None else "Weather condition unavailable"
    display_name = (resolved_name or place).title()
    return(
        "Weather in " + display_name + ":\n"
        "Temperature: " + str(temperature) + "°C\n"
        "Condition: " + condition + "\n"
        "Humidity: " + str(humidity) + "%\n"
        "Wind speed: " + str(wind) + " km/h"
    )
#api response collector
def weather_response(place):
    result, resolved_name = get_mausam(place)
    if result is None:
        return None
    temperature = result.get("temp_C")
    humidity = result.get("humidity")
    wind = result.get("windspeedKmph")
    condition = result.get("weatherDesc", [{}])[0].get("value", "Weather condition unavailable")
    display_name = (resolved_name or place).title()
    return(
        "Weather in " + display_name + ":\n"
        "Temperature: " + str(temperature) + "°C\n"
        "Condition: " + condition + "\n"
        "Humidity: " + str(humidity) + "%\n"
        "Wind speed: " + str(wind) + " km/h"
    )
def istques(text):
    for phrase in time_tags:
        if phrase in text:
            return True
    return False
def get_time():
    current_time= datetime.now()
    return current_time.strftime("%I:%M:%S %p")
awaiting_location = False

#MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN # 
#MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN #
#MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN #

while True:
    user = input("You: ")
    user = normalisation(user)
    
    #storage
    name = get_name(user)
    if name is not None:
        memory["name"]=name
        print("Bot: Nice to meet you, "+name+"!")
        continue
    age = get_age(user)
    if age is not None:
        memory["age"]=age
        print("Bot: I'll remember that you are " + str(age) + " years old.")
        continue
    address = get_address(user)
    if address is not None:
        memory["address"]
        print("Bot: I'll remember that you live in " + address + ".")
        continue
    
    memory_result = memory_response(user)
    if memory_result is not None:
        print("Bot:", memory_result)
        continue
    
    #state word check
    if awaiting_location:
        place = get_location(user)
        result = weather_response(place)
        if result is None:
            print("Bot: Sorry, I couldn't find weather data for '" + place + "'. Try a nearby bigger city or check the spelling?")
        else:
            print("Bot: ",result)
        awaiting_location =False
        continue
    
    #terminating words
    if user in terminators:
        print("Bot: Goodbye!")
        break
    
    #weather report
    if isweather(user):
        place = get_location(user)
        if place is None:
            print("Bot: Which state would you like the weather for?")
            awaiting_location=True
            continue
        result=weather_response(place)
        if result is None:
            print("Bot: Sorry, I couldn't find weather data for '" + place + "'. Try a nearby bigger city or check the spelling?")
        else: 
            print("Bot: ", result)
        continue
    
    #time report
    if istques(user):
        current_time = get_time()
        print("Bot: The current time is", current_time)
        continue
    
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
            result1 = get_wikipedia(word)
            if result1 is None:
                print("I am still an undertrained chatbot. I don't know the above information. Please feel free to ask something else.")
            else:
                title, sumry = result1
                print("Bot: ",sumry)
                print("/source:",title)
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
        result = get_wikipedia(topic)
        if result is None:
            print("I am still an undertrained chatbot. I don't know the above information. Please feel free to ask something else.")
        else:
            title, sumry = result
            print("Bot: ",sumry)
            print("/source:",title)
        continue

    #if passes fails all the tests above then execute this at end;
    print("Bot: Sorry, I don't understand that yet.")
    