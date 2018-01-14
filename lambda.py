"""
Alexa app herddit
@nwHacks2018
"""

from __future__ import print_function
import httplib, urllib, base64, json, sys


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ initialize the session
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the herd it. " \
                    "Please pick your favorite sub reddit " \
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite subreddit by saying, " \
                    "read u b c subreddit."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using herd it. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_Subreddit_attributes(favorite_Subreddit):
    return {"favoriteSubreddit": favorite_Subreddit}


def set_subred_in_session(intent, session):
    """ Subreddit picked by user
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Subreddit' in intent['slots']:
        favorite_Subreddit = intent['slots']['Subreddit']['value']
        session_attributes = create_favorite_Subreddit_attributes(favorite_Subreddit)
        speech_output = "The Subreddit you picked is " + \
                        favorite_Subreddit + \
                        ". You can ask me to read your favorite Subreddit by saying, " \
                        "read my favorite Subreddit."
        reprompt_text = "You can ask me to read your favorite Subreddit by saying, " \
                        "read my favorite Subreddit."
    else:
        speech_output = "I'm not sure what your favorite Subreddit is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite Subreddit is. " \
                        "You can tell me your favorite Subreddit by saying, " \
                        "my favorite Subreddit is u b c."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_reddit_posts(subreddit):
    unloaded = True
    numberofposts = 5
    url = "https://www.reddit.com/r/%s.json" % subreddit
    print(url)
    speech = "";

    while unloaded:
      response = urllib.urlopen(url)
      data = json.loads(response.read())

      if 'data' in data:
        unloaded = False
        sum = 0;
        index = 0;

        while sum < numberofposts:
          if not data['data']['children'][index]['data']['stickied']:
            #title
            print(data['data']['children'][index]['data']['title'])
            speech += str(data['data']['children'][index]['data']['title'])
            #image if there is one, or body
            if data['data']['children'][index]['data']['selftext_html'] is None:
              #image
              image_url = data['data']['children'][index]['data']['preview']['images'][0]['source']['url']
              print("querying Microsoft Vision API" + image_url)
              print(get_image_description(image_url))
              speech += str(get_image_description(image_url))
            else:
              #body
              print(data['data']['children'][index]['data']['selftext'])
              speech += str(data['data']['children'][index]['data']['selftext'])

            sum = sum + 1
          index = index + 1
      else:
        print("Loading...")

    print(speech)
    return speech

def get_image_description(url):

    subscription_key = 'da370ca9abc04597846057a56fca8f7f'
    uri_base = 'westcentralus.api.cognitive.microsoft.com'

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.urlencode({
        'visualFeatures': 'Categories,Description,Color',
        'language': 'en',
    })

    body = "{'url':'%s'}" % url

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        print ("Response:")
        print(parsed['description']['captions'][0]['text'])
        conn.close()
        return parsed['description']['captions'][0]['text']

    except Exception as e:
        print('Error:')
        print(e)

def get_Subreddit_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteSubreddit" in session.get('attributes', {}):
        favorite_Subreddit = session['attributes']['favoriteSubreddit']

        speech_output = get_reddit_posts(favorite_Subreddit)
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite Subreddit is. " \
                        "You can tell me your favorite Subreddit by saying, " \
                        "my favorite Subreddit is u b c."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MySubredIntent":
        return set_subred_in_session(intent, session)
    elif intent_name == "ReadSubredIntent":
        return get_Subreddit_from_session(intent, session)
    elif intent_name == "StopIntent":
        return on_session_stopped(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_stopped(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
