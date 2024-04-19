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
            if l == 'negative':
                s = -s
            result[l] = s
        result = sorted(result.items(), key=lambda x:abs(x[1]), reverse=True)[0][1]
        return result
    
    def calculate_overall_esg(self, stable_esg, varying_esg, var, n=50):
        alpha = n / (n + var)
        beta = var / (n + var)
        new_esg = alpha * np.array(stable_esg) + beta * np.array(varying_esg)
        return new_esg


summary = ["The rise in oil prices could have a negative impact on climate change efforts due to increased emissions from the burning of fossil fuels. Furthermore, the ongoing war may also cause disruptions in energy supply chains and disrupt renewable energy projects, which could further exacerbate environmental issues.",
        "The economic uncertainty arising from the rise in oil prices and potential global repercussions of the war could affect employment prospects, business sustainability, and overall living conditions of people worldwide. Additionally, concerns about the impact on economies may increase market volatility, which can have a ripple effect on individuals' savings, investments, and retirement plans.",
        "The fluctuation in oil prices and global economic impacts could challenge governments' ability to manage their economies effectively and implement policies that address climate change and sustainable development goals. These events may also highlight the need for more cooperation between nations to mitigate the consequences of such unforeseen circumstances on global markets, which are interconnected through trade, capital flows, and other mechanisms."
        ]

text1 = "1. Environmental: The rise in oil prices could have a negative impact on climate change efforts due to increased emissions from the burning of fossil fuels. Furthermore, the ongoing war may also cause disruptions in energy supply chains and disrupt renewable energy projects, which could further exacerbate environmental issues. 2. Social: The economic uncertainty arising from the rise in oil prices and potential global repercussions of the war could affect employment prospects, business sustainability, and overall living conditions of people worldwide. Additionally, concerns about the impact on economies may increase market volatility, which can have a ripple effect on individuals' savings, investments, and retirement plans. 3. Governance: The fluctuation in oil prices and global economic impacts could challenge governments' ability to manage their economies effectively and implement policies that address climate change and sustainable development goals. These events may also highlight the need for more cooperation between nations to mitigate the consequences of such unforeseen circumstances on global markets, which are interconnected through trade, capital flows, and other mechanisms."
text2 = "1. Environmental: The news focuses on FuelCell Energy, a company that develops and manufactures fuel cell energy platforms designed for decarbonizing power and producing hydrogen. These technologies have the potential to significantly reduce carbon emissions, which is aligned with ESG's environmental objectives. 2. Social: Although not explicitly mentioned in this particular news summary, some social implications could be derived from the company's efforts. For example, the use of cleaner energy sources may improve air quality and contribute to a healthier environment for people living near areas where traditional power plants are prevalent. Additionally, the development of sustainable energy solutions may create job opportunities in the green energy sector. 3. Governance: The news does not provide direct information on how FuelCell Energy's governance practices align with ESG standards. However, as a publicly traded company listed on Nasdaq, investors and shareholders may be interested in understanding how the company manages its impact on environmental and social issues, including their sustainability policies, corporate governance structures, and stakeholder engagement efforts."


if __name__ == "__main__":
    model = SentimentalModel()
    esg = [model.predict(x) for x in summary]
    print(esg)
