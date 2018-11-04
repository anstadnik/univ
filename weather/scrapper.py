import requests
import json
url="https://api.openaq.org/v1/cities?limit=10"
response = json.loads(requests.get(url).text)
print(type(response))
for key in response:
    print(key)
    print(response[key])
import pandas as pd
# # import io
# # import requests
# # from pprint import pprint
# # s=requests.get(url).content
c0=pd.io.json.json_normalize(response['meta'])
c1=pd.io.json.json_normalize(response['results'])
print('#################################')
print(c0)
print('#################################')
print(c1)
