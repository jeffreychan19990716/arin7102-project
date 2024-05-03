import requests, json
from openai import OpenAI
import re

class NewsFeeder:
    def __init__(self, ticker):
        self.url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey=DVCH41JKGLK7G4UK&time_from=20240314T0130&time_to=20240414T0130&sort=LATEST&limit=5'
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        self.ticker = ticker

    def get(self):
        x = requests.get(self.url)
        xmlstr = x.content.decode('utf-8')
        data = json.loads(xmlstr)
        return data
    
    def get_offline(self, ticker="CVX"):
        f = open('example_CVX.json') 
        data = json.load(f)
        return data
    
    def analyse_news(self, news, index):
        content = "The News summary is: " + news["feed"][index]["summary"] + """
            Firstly, answer "Yes, this news is related to (environmental/social/governance/none of any ESG aspect)" if this news is related to ESG, either one aspect is ok, then analyze how this news is related to ESG in the three aspect (E, S, G).
            Answer in the form of:
            1. Environmental: 
            2. Social:
            3. Governance:

            Answer "No, this news is not related to ESG" if this news is not related to ESG, no need to do the further analyze.
            """
        completion = self.client.chat.completions.create(model="local-model", messages=[{"role": "user", "content": content},],temperature=0.7)
        text = completion.choices[0].message.content
        if "No" in text[:10]:
            return False, [None, None, None], text
        else:
            return True, self.seperate(text), text
        
    def analyse_url(self, url):
        content = "Summarize the news in the given url: " + str(url)
        completion = self.client.chat.completions.create(model="local-model", messages=[{"role": "user", "content": content},],temperature=0.7)
        news = completion.choices[0].message.content
        content = "The News summary is: " + news + """
            Firstly, answer "Yes, this news is related to (environmental/social/governance/none of any ESG aspect)" if this news is related to ESG, either one aspect is ok, then analyze how this news is related to ESG in the three aspect (E, S, G).
            Answer in the form of:
            1. Environmental: 
            2. Social:
            3. Governance:

            Answer "No, this news is not related to ESG" if this news is not related to ESG, no need to do the further analyze.
            """
        completion = self.client.chat.completions.create(model="local-model", messages=[{"role": "user", "content": content},],temperature=0.7)
        text = completion.choices[0].message.content
        if "No" in text[:10]:
            return False, [None, None, None], text, news
        else:
            return True, self.seperate(text), text, news
        
    def analyse_url_offline(self, url):
        news = "Tesla has cut the prices of its electric vehicles (EVs) in China in line with the recent price reductions in the US, as the company faces slowing sales and increased competition in the mainland market. The price reductions apply to the Model S, Model X, Model 3, and Model Y vehicles, and range from a 3% to 6% decrease depending on the model. The move is seen as an attempt to boost sales and maintain its market share in the face of growing competition from domestic EV manufacturers such as NIO, Xpeng, and Li Auto. The price cut also comes amid a global semiconductor shortage that has affected the automobile industry, causing production delays and supply chain disruptions."
        # https://www.scmp.com/business/china-business/article/3259790/battle-market-share-tesla-cuts-ev-prices-mainland-china-line-us-sales-slow
        text = "Yes, this news is related to environmental and governance aspects.\n1. Environmental: Although not directly focused on the environmental performance of Tesla's vehicles, the news about Tesla cutting EV prices in China may increase the accessibility and affordability of electric vehicles for a broader market. This could lead to higher adoption rates of cleaner transportation options, ultimately reducing greenhouse gas emissions and benefiting the environment.\n2. Social:\n3. Governance: Tesla's decision to cut EV prices in China in response to slowing sales reflects the company's strategic approach to managing its market presence and addressing market challenges. This decision demonstrates the company's adaptability and governance, as it seeks to maintain its market position and continue promoting electric vehicle adoption."
        return True, self.seperate(text), text, news
        
    def analyse_news_offline(self, index=None):
        text = ''
        if self.ticker == 'CVX':
            text = "Yes, this news is related to environmental and governance aspects.\n1. Environmental: Chevron's investment in ION Clean Energy, a developer of advanced carbon capture technology for industrial emissions, shows the company's commitment to reducing its environmental impact and addressing climate change. By supporting the development of innovative technologies, Chevron is taking a proactive approach to mitigate the environmental consequences of its operations.\n2. Social:\n3. Governance: Chevron's decision to invest in ION Clean Energy demonstrates the company's strategic focus on sustainability and climate change mitigation. This reflects responsible governance and a commitment to aligning the company's operations with long-term environmental goals."
        if self.ticker == 'PCCYF':
            text = "Yes, this news is related to environmental, social, and governance aspects.\n1. Environmental: The nation's largest oil and gas producer's commitment to peak carbon emissions next year and double the contribution of low-carbon energy to its output capacity demonstrates their focus on reducing their environmental impact and transitioning to cleaner energy sources.\n2. Social: By concentrating on low-carbon energy and reducing greenhouse gas emissions, the company is contributing to global efforts to combat climate change and protect public health. This can have a positive social impact by promoting a more sustainable and healthier society.\n3. Governance: The commitment made by the company's top leaders to achieve these ambitious goals reflects strong governance and strategic decision-making. It demonstrates that the company is actively considering and addressing ESG issues as part of its overall business strategy."
        if self.ticker == 'TSLA':
            text = "Yes, this news is related to environmental and governance aspects.\n1. Environmental: Although not directly focused on the environmental performance of Tesla's vehicles, the news about Tesla cutting EV prices in China may increase the accessibility and affordability of electric vehicles for a broader market. This could lead to higher adoption rates of cleaner transportation options, ultimately reducing greenhouse gas emissions and benefiting the environment.\n2. Social:\n3. Governance: Tesla's decision to cut EV prices in China in response to slowing sales reflects the company's strategic approach to managing its market presence and addressing market challenges. This decision demonstrates the company's adaptability and governance, as it seeks to maintain its market position and continue promoting electric vehicle adoption."

        if "No" in text[:10]:
            return False, [None, None, None], text
        else:
            return True, self.seperate(text), text

    @classmethod
    def seperate(self, text):
        pattern = r"\d+\.\s"
        segments = re.split(pattern, text)
        segments = [segment.strip() for segment in segments if segment.strip()]
        return segments[-3:]


if __name__ == "__main__":
    company = 'TSLA'
    feeder = NewsFeeder(company)
    success, summary, _ = feeder.analyse_news_offline()
    print(summary)
