'''
import requests

url = "https://rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com/rewrite"

payload = "{\r\n    \"language\": \"en\",\r\n    \"strength\": 3,\r\n    \"text\": \"lets do this\"\r\n}"
headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "rewriter-paraphraser-text-changer-multi-language.p.rapidapi.com",
    'x-rapidapi-key': "SIGN-UP-FOR-KEY"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
'''
import http.client
conn = http.client.HTTPSConnection("api.webscrapingapi.com")

conn.request("GET", "/v1?api_key=tszmJJkXUJX7azs0N7EXnf1UxscP3x2O&url=https%3A%2F%2Fapi.ipify.org%2F%3Fformat%3Djson&device=desktop&proxy_type=datacenter")

res = conn.getresponse()
data = res.read()
decoded = data.decode("utf-8")
print(data.decode("utf-8"))