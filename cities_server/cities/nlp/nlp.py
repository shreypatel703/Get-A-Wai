#IMPORTS
import spacy
import cities
import flask
from cities.api.api import getCities, filter_activities
from spacy import displacy 

from nltk.tokenize import word_tokenize

import nltk


@cities.app.route('/nlp/', methods=['GET'])
def do_nlp():
    #SPACY
    nlp = spacy.load("en_core_web_sm")
    

    #input = "I can almost feel the warm sand between my toes as I daydream about a luxurious beach vacation, complete with crystal-clear turquoise waters, palm trees swaying in the gentle ocean breeze, and endless hours of relaxation on a comfy beach chair under the bright sun."
    input = flask.request.args.get('query')
    text = nlp(input)

    #This is getting all the noun phrases from the sentences (avoiding the words that we do not need)
    noun_chunks = []
    for np in text.noun_chunks:
        noun_chunks.append(np.text)
        #print(np.text)


    nouns = " ".join(noun_chunks)

    #print(nouns) #
    #list of things we need for activties and feelings


    activity_keywords = ['adventure sports', 'beachcombing', 'birdwatching', 'boating', 'camping', 'canoeing', 'canyoneering',
                        'cycling', 'diving', 'fishing', 'hiking', 'horseback riding', 'kayaking', 'mountain biking',
                        'mountaineering', 'photography', 'rafting', 'rock climbing', 'sailing', 'scuba diving', 'skiing',
                        'snowboarding', 'snorkeling', 'paddleboarding', 'surfing', 'swimming', 'trekking', 'whale watching',
                        'wildlife viewing', 'wine tasting', 'yoga', 'exploring cultural sites', 'attending festivals or events',
                        'volunteering', 'relaxing on the beach', 'visiting museums', 'visiting amusement parks', 'shopping',
                        'visiting historical landmarks', 'eating local cuisine', 'going on scenic drives', 'taking scenic flights',
                        'cruising', 'visiting botanical gardens', 'taking guided tours', 'going to the theater or opera', 'spas',    
                        'hot springs', 'ziplining', 'skydiving', 'bungee jumping', 'paragliding', 'hang gliding', 'whitewater kayaking',    
                        'ice climbing', 'glacier trekking', 'sandboarding', 'safari', 'backpacking', 'skiing', 'snowmobiling',    
                        'dog sledding', 'ice fishing', 'kiteboarding', 'wakeboarding', 'water skiing', 'dolphin watching',    
                        'seaplane rides', 'zipline and canopy tours', 'hunting', 'rock scrambling', 'mountain climbing',    
                        'mountainboarding', 'kitesurfing', 'base jumping', 'bouldering', 'cave exploring', 'geo caching',    
                        'kite landboarding', 'microlighting', 'parasailing', 'slacklining', 'trampolining', 'ultralight flying',
                        'wake skating', 'wakesurfing', 'white water rafting', 'wind surfing', 'sun', 'clubbing', 'gambling', 'gamble', 'clubs', 'shops', 'sightseeing']
                    
    # feeling_keywords = [
    #     'adventurous', 'alive', 'amazed', 'amused', 'awe', 'awestruck', 'blissful', 'breezy', 'calm', 'carefree', 
    #     'charmed', 'content', 'cozy', 'creative', 'curious', 'ecstatic', 'elevated', 'energized', 'enlightened', 
    #     'enthusiastic', 'excited', 'exhilarated', 'free', 'fulfilled', 'glad', 'grateful', 'happy', 'heartened', 
    #     'humble', 'inspired', 'invigorated', 'joyful', 'liberated', 'lighthearted', 'lively', 'loved', 'nostalgic', 
    #     'open minded', 'optimistic', 'overwhelmed', 'peaceful', 'refreshed', 'relaxed', 'rejuvenated', 'renewed', 
    #     'rested', 'revived', 'satisfied', 'serene', 'spiritual', 'stimulated', 'surprised', 'thankful', 'thrilled', 
    #     'tranquil', 'transformed', 'uplifted', 'wanderlust', 'warm', 'welcoming', 'whimsical', 'wonder'
    # ]



    # !python -m spacy download en_core_web_md  #THIS NEEDS TO BE RUN ONCE BEFORE SO UNCOMMENT, RUN, AND THEN COMMENT, AND THEN IT SHOULD WORK
    
    nlp = spacy.load('en_core_web_md')
    
    # input = "I want to go to an adventurous place such as ziplining or rock climbing. But I also want to relax at a beach maybe. In addition, maybe something in the Carribean"
    

    tokens = nlp(nouns)


    #getting all the words
    travel = " ".join(activity_keywords)
    words = nlp(travel)
    
    #for debugging
    # for token in tokens:
    #     print(token.text, token.has_vector, token.vector_norm, token.is_oov)
    
    token1, token2 = tokens[0], tokens[1]

    #the final List of activties/adjectives
    finalList = set()

    for x in words:
        if x.text == "the": #removing the
            continue
        for y in tokens:
            # print(x, y, y.similarity(x))

            #checking similarity

            # if y.text == "-" and y.similarity(x) > 0.7: 
            #     print(x, y, y.similarity(x))
            if x.similarity(y) > 0.7:
                finalList.add(y.text)
    connection = cities.model.get_db()
    city_results, activities = getCities(list(finalList))
    context = {
        "cities": city_results,
        "activities": activities,
        "type": "cities"
    }
    
    response = flask.jsonify(**context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


    # print("Similarity:", token1.similarity(token2))
if __name__ == '__main__':
    do_nlp()