import urllib, json
numberofposts = 3
url = "https://www.reddit.com/r/funny.json"
url1=""
data = {};
while 'data' not in data:
  data = json.loads(urllib.urlopen(url).read())
  print "Loading..."
sum = 0;
index = 0;
while sum < numberofposts:

  if not data['data']['children'][index]['data']['stickied']:
    #permalink

    url1 = "https://reddit.com"+data['data']['children'][index]['data']['permalink'] +".json"
    print url1
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
  index1 = 0
  data1 = {'error': 'none'};
  print "comment:"
  print ""
  while 'error' in data1:
    print "Loading..."
    data1 = json.loads(urllib.urlopen(url1).read())

  while index1 < numberofcomments:
    try:
      print index1
      comment = data1[1]['data']['children'][index1]['data']['body']
      parsedcomment = ''
      while 'http' in comment and '.jpg' in comment:
        parsedcomment = parsedcomment + comment[0:comment.find("http")]
        comment = comment[comment.find("http"):len(comment)]
        if '.jpg' in comment:
          if 'http' not in comment[5:comment.find(".jpg")+4]:
            picture = comment[0:comment.find(".jpg")+4]
            parsedcomment = parsedcomment + "picture"
            print "picture"
            print picture
          else:
            parsedcomment = parsedcomment + comment[0:5]
            comment = comment[5:len(comment)]
            parsedcomment = parsedcomment = comment[0:comment.find('http')]
            comment = comment[comment.find('http'):len(comment)]
        comment = comment[comment.find(".jpg")+4:len(comment)]
      parsedcomment = parsedcomment +comment




      print parsedcomment
      index1 = index1 + 1
    except Exception as e:
      if index1 is 0:
        print('no comments')
      else:
        print('no more comments')
      index1=numberofcomments;

