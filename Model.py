from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import pandas as pd


class SentimentalModel():
    def __init__(self):
        self.labels = ['negative', 'neutral', 'positive']
        MODEL_PATH = f"cardiffnlp/twitter-roberta-base-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        self.model.save_pretrained(MODEL_PATH)
        self.tokenizer.save_pretrained(MODEL_PATH)

    def predict(self, text):
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        result = {}
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        for i in range(scores.shape[0]):
            l = self.labels[ranking[i]]
            s = scores[ranking[i]]
            result[l] = s
        result = sorted(result.items(), key=lambda x:abs(x[1]), reverse=True)[0]
        if result[0] == "neutral":
            return 0
        elif result[0] == "negative":
            return -result[1]
        else:
            return result[1]
    
    def calculate_overall_esg(self, stable_esg, varying_esg, var, n=50):
        #alpha = n / (n + var)
        #beta = var / (n + var)
        z = 0.95
        #varying_esg > 0.7
        new_esg = []
        for x, delta_x in zip(stable_esg, varying_esg):
            if delta_x == 0:
                new_esg.append(x)
            else:
                new_x = z * x + (1-z) * delta_x
                new_esg.append(new_x)
        return new_esg


summary = ["Environmental: Chevron's investment in ION Clean Energy, a developer of advanced carbon capture technology for industrial emissions, shows the company's commitment to reducing its environmental impact and addressing climate change. By supporting the development of innovative technologies, Chevron is taking a proactive approach to mitigate the environmental consequences of its operations.", 'Social:', "Governance: Chevron's decision to invest in ION Clean Energy demonstrates the company's strategic focus on sustainability and climate change mitigation. This reflects responsible governance and a commitment to aligning the company's operations with long-term environmental goals."]
summary = ["Environmental: Although not directly focused on the environmental performance of Tesla's vehicles, the news about Tesla cutting EV prices in China may increase the accessibility and affordability of electric vehicles for a broader market. This could lead to higher adoption rates of cleaner transportation options, ultimately reducing greenhouse gas emissions and benefiting the environment.", 'Social:', "Governance: Tesla's decision to cut EV prices in China in response to slowing sales reflects the company's strategic approach to managing its market presence and addressing market challenges. This decision demonstrates the company's adaptability and governance, as it seeks to maintain its market position and continue promoting electric vehicle adoption."]

if __name__ == "__main__":
    model = SentimentalModel()
    esg = [model.predict(x) for x in summary]
    print(esg)