import urllib, json
url = "https://www.reddit.com/r/aww.json"
response = urllib.urlopen(url)
data = json.loads(response.read())
print data['data']['children'][0]