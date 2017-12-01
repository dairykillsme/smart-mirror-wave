import urllib.request
import json
import time

def newsBasic(newspaper):
    #Get 1 day ago
    today = int(time.time() * 1000)
    day = 86400000
    yesterday = today - day

    #Get Page from WebHose language:english site_type:news site:nytimes.com performance_score:10 
    url = 'http://webhose.io/filterWebContent?token=8c25a471-9249-46cd-834c-2248d9ae99a2&format=json&ts=' + str(yesterday) + '&sort=crawled&q=language%3Aenglish%20site%3Anytimes.com%20has_video%3Afalse%20performance_score%3A%3E1'
    page = urllib.request.urlopen(url)
    
    #Convert Page into JSON Readable
    json_str = page.read().decode('utf-8', 'ignore')
    parsed_json = json.loads(json_str)

    #Get Info
    for article in range(0, len(parsed_json['posts']) - 1):
        print(article)
        newspaper[article] = {}
        newspaper[article]['people'] = {}
        
        newspaper[article]['title'] = parsed_json['posts'][article]['title']
        newspaper[article]['author'] = parsed_json['posts'][article]['author']
        newspaper[article]['body'] = parsed_json['posts'][article]['text']

        try:
            newspaper[article]['image'] = parsed_json['posts'][article]['thread']['main_image']
        except:
            newspaper[article]['image'] = 'NULL'

        for person in range(0, len(parsed_json['posts'][article]['entities']['persons']) - 1):
            newspaper[article]['people'][person] = {}
            newspaper[article]['people'][person]['name'] = parsed_json['posts'][article]['entities']['persons'][person]['name']
            newspaper[article]['people'][person]['sentiment'] = parsed_json['posts'][article]['entities']['persons'][person]['sentiment']
