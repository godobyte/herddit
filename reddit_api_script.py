import urllib, json
unloaded = True
numberofposts = 5
url = "https://www.reddit.com/r/news.json"
while unloaded:

  response = urllib.urlopen(url)
  data = json.loads(response.read())
  if 'data' in data:
    unloaded = False
    sum = 0;
    index = 0;


    while sum < numberofposts:


      if not data['data']['children'][index]['data']['stickied']:
        #permalink
        print "https://reddit.com"+data['data']['children'][index]['data']['permalink']

        #title
        print data['data']['children'][index]['data']['title']

        #image if there is one, or body
        if data['data']['children'][index]['data']['selftext_html'] is None:
          if 'preview' in data['data']['children'][index]['data']:
            #image
            print data['data']['children'][index]['data']['preview']['images'][0]['source']['url']
        else:
          #body
          print data['data']['children'][index]['data']['selftext']


        sum = sum + 1
      index = index + 1
  else:
    print "Loading..."