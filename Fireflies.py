import requests
from bs4 import BeautifulSoup
url = "https://host-elterxrz-prod.prod.cywar.xyz:49817/"
fireflies = "12431"
method = "GET"
session = requests.session()
while True:
    if method == "GET":
        req = session.get(url+f"?FIREFLIES={fireflies}",verify=False)
    elif method == "POST":
        req = session.post("https://host-elterxrz-prod.prod.cywar.xyz:49817/",verify=False,data={'FIREFLIES':fireflies})
    soup = BeautifulSoup(req.text,"html.parser")
    soup = soup.find('canvas')
    soup = soup.get('title')
    fireflies = soup.split(" ")[1]
    method = soup.split(" ")[0]
    print(soup)