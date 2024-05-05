# Running the Chatbot
1. Install LM-Studio. Load a LLM model (e.g. GML-Mistral-merged-v1-gguf) and start a local server.
2. Install all neccessary dependencies
   - PyQt
   - transformers
3. Download the sentimental analysis model from:
   https://connecthkuhk-my.sharepoint.com/:u:/g/personal/laicass_connect_hku_hk/EaoOzAo5hzFJgW2CNE3yfcABTotisC9xVXXd-X6Ci_yuMg?e=rS32WL
   and put in the root directory
4. run with ```python Chatbot.py```, you can test the ticker 'CVX', or input any news url
5. run with ```python Chatbot.py --online```, you can test any ticker, or input any news url


# Important notes
- Input company ticker from SP 500. Due to the API limit for news provider, please test with the ticker 'CVX', where the data has been downloaded locally for offline testing. You can however still test the online model, but may need to try different company as most news are not ESG related. 
- Input any relevant ESG news url to see the associated ESG scores.
- Depending on the computer, it may take a while for the local LLM model to make a response to the UI, please dont close the UI window and wait for the output.
- Each time after exiting the Chatbot, a log of the chat history will be saved with the file name as the timestamp of chat.
