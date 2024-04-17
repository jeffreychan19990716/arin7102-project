import requests, json
from openai import OpenAI
import re

class NewsFeeder:
    def __init__(self, ticker):
        self.url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey=DVCH41JKGLK7G4UK&time_from=20240314T0130&time_to=20240414T0130&sort=LATEST&limit=5'
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

    def get(self):
        x = requests.get(self.url)
        xmlstr = x.content.decode('utf-8')
        data = json.loads(xmlstr)
        return data
    
    def analyse_news(self, news, index):
        content = "The News summary is: " + news["feed"][index]["summary"] + """
            Firstly, answer "Yes, this news is related to ESG" if this news is related to ESG, either one aspect or indirect impplication is also ok, then analyze how this news is related to ESG in the three aspect (E, S, G).
            Answer in the form of:
            1. Environmental: 
            2. Social:
            3. Governance:

            Answer "No, this news is not related to ESG" if this news is not related to ESG, no need do the further analyze.
            """
        completion = self.client.chat.completions.create(model="local-model", messages=[{"role": "user", "content": content},],temperature=0.7)
        text = completion.choices[0].message.content
        if text[:1] == "No":
            return False, [None, None, None], text
        else:
            return True, self.seperate(text), text
    
    def seperate(self, text):
        pattern = r"\d+\.\s"
        segments = re.split(pattern, text)
        segments = [segment.strip() for segment in segments if segment.strip()]
        return segments


if __name__ == "__main__":
    company = 'CVX'
    feeder = NewsFeeder(company)
    data = feeder.get()
    feeder.analyse_news(data, index=0)