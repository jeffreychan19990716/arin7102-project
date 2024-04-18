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
    
    def get_offline(self):
        f = open('example_CVX.json') 
        data = json.load(f)
        return data
    
    def analyse_news(self, news, index):
        content = "The News summary is: " + news["feed"][index]["summary"] + """
            Firstly, answer "Yes, this news is related to ESG" if this news is related to ESG, either one aspect or indirect implication is also ok, then analyze how this news is related to ESG in the three aspect (E, S, G).
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
        
    def analyse_news_offline(self, news=None, index=None):
        text = "Yes, this news is related to ESG.\n1. Environmental: While there are no direct mentions of environmental impact in this news article, it should be noted that oil drilling activities can have significant environmental implications such as greenhouse gas emissions and potential oil spills. Companies operating in the oil industry must ensure they implement sustainable practices and adhere to environmental regulations to minimize any negative impacts on the environment.\n2. Social: The collaboration between two major companies, one being a U.S.-based multinational and the other a Venezuelan state-owned enterprise, might have potential social implications. This partnership could potentially bring job opportunities and economic growth in Venezuela, benefitting the local community. However, further information is required to assess whether these benefits are distributed equitably among all stakeholders, considering possible human rights concerns and labor conditions in Venezuela.\n3. Governance: The easing of U.S. sanctions on Venezuela's oil industry suggests a shift in geopolitical dynamics that could have implications for companies operating in the region. Increased transparency and accountability in business practices are crucial to ensure that both Chevron and PDVSA act responsibly, adhering to international standards and regulatory frameworks."
        if text[:1] == "No":
            return False, [None, None, None], text
        else:
            return True, self.seperate(text), text

    
    def seperate(self, text):
        pattern = r"\d+\.\s"
        segments = re.split(pattern, text)
        segments = [segment.strip() for segment in segments if segment.strip()]
        return segments[-3:]


if __name__ == "__main__":
    company = 'CVX'
    feeder = NewsFeeder(company)
    success, summary, _ = feeder.analyse_news_offline()
    print(summary)
