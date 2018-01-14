#!/usr/bin/python

import httplib, urllib, base64, json, sys

###############################################
#### Update or verify the following values. ###
###############################################




def main(argv):

       # Replace the subscription_key string value with your valid subscription key.
   subscription_key = 'da370ca9abc04597846057a56fca8f7f'

   # Replace or verify the region.
   #
   # You must use the same region in your REST API call as you used to obtain your subscription keys.
   # For example, if you obtained your subscription keys from the westus region, replace
   # "westcentralus" in the URI below with "westus".
   #
   # NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
   # a free trial subscription key, you should not need to change this region.
   uri_base = 'westcentralus.api.cognitive.microsoft.com'

   headers = {
       # Request headers.
       'Content-Type': 'application/json',
       'Ocp-Apim-Subscription-Key': subscription_key,
   }

   params = urllib.urlencode({
       # Request parameters. All of them are optional.
       'visualFeatures': 'Categories,Description,Color',
       'language': 'en',
   })

   # The URL of a JPEG image to analyze.
   # body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/1/12/Broadway_and_Times_Square_by_night.jpg'}"
   body = "{'url':'%s'}" % argv[1]

   try:
       # Execute the REST API call and get the response.
       conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
       conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
       response = conn.getresponse()
       data = response.read()

       # 'data' contains the JSON data. The following formats the JSON data for display.
       parsed = json.loads(data)
       print ("Response:")
       print parsed['description']['captions'][0]['text']
       # print (json.dumps(parsed, sort_keys=True, indent=2))
       conn.close()

   except Exception as e:
       print('Error:')
       print(e)

if __name__ == "__main__":
   main(sys.argv)

   