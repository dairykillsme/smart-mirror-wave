import urllib.request
import json
import time

def newsBasic(newspaper):
    phrases = ["Newsletter Sign Up",
               "Continue reading the main story",
               "Sign Up for the Opinion Today Newsletter Every weekday, get thought-provoking commentary from Op-Ed columnists, the Times editorial board and contributing writers from around the world.",
               "Please verify you're not a robot by clicking the box",
               "Invalid email address. Please re-enter.",
               "You must select a newsletter to subscribe to.",
               "Sign Up You agree to receive occasional updates and special offers for The New York Times's products and services. Thank you for subscribing.",
               "An Error has occurred.",
               "Please try again later.",
               "You are already subscribed to this email.",
               "View all New York Times newsletters.",
               "See Sample",
               "Manage Email Preferences",
               "Not you?",
               "Privacy Policy Opt out or contact us anytime",
               "Advertisement",
               "Photo",
               "Photo.",
               "Advertisement",
               "An error has occurred.",
               "We're interested in your feedback on this page. Tell us what you think",
               "What's Next Loading... Go to Home Page >>",
               "Opt out or contact us anytime"]
    
    #Get 1 day ago
    today = int(time.time() * 1000)
    day = 86400000 * 2
    yesterday = today - day

    #Get Page from WebHose language:english site_type:news site:nytimes.com performance_score:10 
    url = 'http://webhose.io/filterWebContent?token=8c25a471-9249-46cd-834c-2248d9ae99a2&format=json&ts=' + str(yesterday) + '&sort=crawled&q=language%3Aenglish%20site%3Anpr.org%20spam_score%3A0'
    page = urllib.request.urlopen(url)
    
    #Convert Page into JSON Readable
    json_str = page.read().decode('utf-8', 'ignore')
    parsed_json = json.loads(json_str)

    #Get Info
    for article in range(0, len(parsed_json['posts']) - 1):
        newspaper[article] = {}
        newspaper[article]['people'] = {}
        
        newspaper[article]['title'] = parsed_json['posts'][article]['title']
        newspaper[article]['author'] = parsed_json['posts'][article]['author']
        newspaper[article]['body'] = parsed_json['posts'][article]['text']

        for phrase in phrases:
            newspaper[article]['body'] = newspaper[article]['body'].replace(phrase, '')

        try:
            newspaper[article]['image'] = parsed_json['posts'][article]['thread']['main_image']
        except:
            newspaper[article]['image'] = 'NULL'

        for person in range(0, len(parsed_json['posts'][article]['entities']['persons']) - 1):
            newspaper[article]['people'][person] = {}
            newspaper[article]['people'][person]['name'] = parsed_json['posts'][article]['entities']['persons'][person]['name']
            newspaper[article]['people'][person]['sentiment'] = parsed_json['posts'][article]['entities']['persons'][person]['sentiment']
