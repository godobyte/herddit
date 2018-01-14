import urllib, json
numberofposts = 1
url = "https://www.reddit.com/r/ubc.json"
data = {};
while 'data' not in data:
  data = json.loads(urllib.urlopen(url).read())
  print "Loading..."
sum = 0;
index = 0;
while sum < numberofposts:

  if not data['data']['children'][index]['data']['stickied']:
    #permalink

    url = "https://reddit.com"+data['data']['children'][index]['data']['permalink'] +".json"
    print url
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

#comment code
numberofcomments=1
index = 0
data = {'error': 'none'};
while 'error' in data:
  print "Loading..."
  data = json.loads(urllib.urlopen(url).read())

while index < numberofcomments:
  try:
    print index
    comment = data[1]['data']['children'][index]['data']['body']
    parsedcomment = ''
    while 'http' in comment and '.jpg' in comment:
      parsedcomment = parsedcomment + comment[0:comment.find("http")]
      comment = comment[comment.find("http"):len(comment)]
      if '.jpg' in comment:
        picture = comment[0:comment.find(".jpg")+4]
        parsedcomment = parsedcomment + "picture"
        print "picture"
        print picture
      comment = comment[comment.find(".jpg")+4:len(comment)]
    parsedcomment = parsedcomment +comment




    print parsedcomment
    index = index + 1
  except Exception as e:
    if index is 0:
      print('no comments')
    else:
      print('no more comments')
    index=numberofcomments;

