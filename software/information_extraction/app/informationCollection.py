import requests	
import json

#p = "chemistry"
response = requests.get('http://papurapi.llgc.org.uk/?q=full_text%3Aastronomy&fq=category%3A%22News%22&wt=json&indent=true&wt=json&indent=true&rows=999')
print(response.status_code)
data = response.json()
file = open("welshScientists.json", "w")
json.dump(data, file, sort_keys=True, indent=4)
file.close()
