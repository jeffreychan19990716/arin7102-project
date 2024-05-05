from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import pandas as pd


class SentimentalModel():
    def __init__(self):
        self.labels = ['negative', 'neutral', 'positive']
        tokenizer_path = "model"
        model_path_finetuned = "model"
        # use the following if wants to download from other pretrained source
        #tokenizer_path = "cardiffnlp/twitter-roberta-base-sentiment"
        #model_path_finetuned = "cardiffnlp/twitter-roberta-base-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path_finetuned)
        self.model.save_pretrained(model_path_finetuned)
        self.tokenizer.save_pretrained(tokenizer_path)

    def predict(self, text):
        # return prediction scores
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        # rank output label and logit score
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
    
    def calculate_overall_esg(self, stable_esg, varying_esg, var=1, n=20):
        # calculate ESG score based on credibility theory
        z = n / (n + var)
        new_esg = []
        for x, delta_x in zip(stable_esg, varying_esg):
            if delta_x == 0:
                new_esg.append(x)
            else:
                new_x = z * x + (1 - z) * delta_x
                new_esg.append(new_x)
        return new_esg


summary = ["Environmental: Chevron's investment in ION Clean Energy, a developer of advanced carbon capture technology for industrial emissions, shows the company's commitment to reducing its environmental impact and addressing climate change. By supporting the development of innovative technologies, Chevron is taking a proactive approach to mitigate the environmental consequences of its operations.", 'Social:', "Governance: Chevron's decision to invest in ION Clean Energy demonstrates the company's strategic focus on sustainability and climate change mitigation. This reflects responsible governance and a commitment to aligning the company's operations with long-term environmental goals."]
summary = ["Environmental: Although not directly focused on the environmental performance of Tesla's vehicles, the news about Tesla cutting EV prices in China may increase the accessibility and affordability of electric vehicles for a broader market. This could lead to higher adoption rates of cleaner transportation options, ultimately reducing greenhouse gas emissions and benefiting the environment.", 'Social:', "Governance: Tesla's decision to cut EV prices in China in response to slowing sales reflects the company's strategic approach to managing its market presence and addressing market challenges. This decision demonstrates the company's adaptability and governance, as it seeks to maintain its market position and continue promoting electric vehicle adoption."]



if __name__ == "__main__":
    model = SentimentalModel()
    esg = [model.predict(x) for x in summary]
    print(esg)