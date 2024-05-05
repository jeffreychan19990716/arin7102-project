# Running the Chatbot
1. Install LM-Studio. Load a LLM model (e.g. GML-Mistral-merged-v1-gguf) and start a local server.
2. Install all neccessary dependencies
   - PyQt
   - transformers
3. Download the sentimental analysis model from:
   https://connecthkuhk-my.sharepoint.com/:u:/g/personal/laicass_connect_hku_hk/EaoOzAo5hzFJgW2CNE3yfcABTotisC9xVXXd-X6Ci_yuMg?e=rS32WL
   and put in the root directory
4. run with ```python UI_bubble.py```


# Using the Chatbot
1. Input company ticker from SP 500. Due to the API limit for news provider, we recommend testing the ticker 'CVX'.
2. Input any relevant ESG news url to see the associated ESG scores.
3. Depending on the computer, it may take a while for the local LLM model to make a response to the UI.
