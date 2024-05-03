from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QFont, QIcon
from PyQt5.QtCore import Qt
from NewsFeeder import *
from Model import *
import pandas as pd
import itertools
import time

TICKER_NOT_FOUND = -1
NEWS_NOT_FOUND = -2

def search_database(database, ticker):
    data = database.loc[database['Symbol'] == ticker]
    stable_esg = [data["Environment Risk Score"].values[0], 
                  data["Social Risk Score"].values[0],
                  data["Governance Risk Score"].values[0]]
    #var = data["var"].values[0] # https://www.macroaxis.com/invest/technicalIndicator/JNJ/Variance
    var = 0
    return stable_esg, var

class ChatbotApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.model = SentimentalModel()
        self.esg_database = pd.read_csv("SP 500 ESG Risk Ratings.csv")
        self.setWindowTitle("ESG Investment News Chatbot")
        self.setGeometry(100, 100, 1800, 1000)

        layout = QtWidgets.QVBoxLayout()

        self.chat_list = QtWidgets.QListWidget()
        self.chat_list.setStyleSheet("background-color:#fcf6e7;")
        layout.addWidget(self.chat_list)
        

        input_layout = QtWidgets.QHBoxLayout()

        self.input_box = QtWidgets.QLineEdit()
        input_layout.addWidget(self.input_box)

        self.send_button = QtWidgets.QPushButton("Send")
        input_layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet(
            "QPushButton::hover{"
            "background-color: #538685;"
            "color: white;"
            "font: bold;"
            "border: none;"
            "}"
        )

        self.reset_button = QtWidgets.QPushButton("Restart")
        input_layout.addWidget(self.reset_button)
        self.reset_button.clicked.connect(self.reset)
        self.reset_button.setStyleSheet(
            "QPushButton::hover{"
            "color: white;"
            "font: bold;"
            "background-color: #d78675;"
            "border: none;"
            "}"
        )

        layout.addLayout(input_layout)
        self.setLayout(layout)

    def reset(self):
        self.chat_list.clear()
        self.input_box.clear()
        self.add_message("Chatbot", "Welcome to ESG Investment News Chatbot!!\nPlease input the company ticker that you want to analyse. Or, input a news hyperlink directly for ESG score analysis.")

    def send_message(self):
        user_message = self.input_box.text()
        if user_message.strip():
            self.add_message("You", user_message)
            outputs = self.message_handling(user_message)
            self.input_box.clear()
            for output in outputs:
                self.add_message("Chatbot", output)

    def add_message(self, sender, message):
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight) if sender == "You" else item.setTextAlignment(QtCore.Qt.AlignLeft)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        label = QtWidgets.QLabel(message)
        label.setWordWrap(True)
        label.setStyleSheet(f"""
            background-color: {'#e1f5fe' if sender == 'Chatbot' else '#dcedc8'};
            border-radius: 10px;
            padding: 10px;
        """)
        
        profile_icon = QtWidgets.QLabel()

        if sender == "Chatbot":
            profile_pixmap = QPixmap("Chatbot icon transparent.png")
            profile_icon.setPixmap(profile_pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(profile_icon)
            layout.addWidget(label)
        else:
            profile_pixmap = QPixmap("profile icon.png")
            profile_icon.setPixmap(profile_pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(label)
            layout.addWidget(profile_icon)
            

        layout.setContentsMargins(10, 5, 10, 5)
        layout.setAlignment(QtCore.Qt.AlignRight if sender == "You" else QtCore.Qt.AlignLeft)
        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, widget)

    def format_esg_text(self, content):
        text = "Environmental:{e:.2f}\nSocial:{s:.2f}\nGovernance:{g:.2f}".format(e=content[0], s=content[1], g=content[2])
        return text
    
    def check_for_url(self, text): 
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, text)
        return [x[0] for x in url]
    
    def generate_esg_report(self, ticker, success, summary, outputs):
        if not success:
            outputs.append("Failed to analyse. Try again!")
            return outputs
        esg = [self.model.predict(x) for x in summary]
        if ticker is not None:
            outputs.append(f"Here is the analysis for ESG news for {ticker}:")
        else:
            outputs.append(f"Here is the analysis:")
        for news, score, sub in zip(summary, esg, ["Environment", "Social", "Goverance"]):
            if abs(score) < 1e-4:
                text = sub + " related aspect is not identified."
                outputs.append(text)
            else:
                text = news + "\n" + sub + " score is: " + "{:.2f}".format(score)
                outputs.append(text)
        if ticker is not None:
            try:
                stable_esg, var = search_database(self.esg_database, ticker)
                new_esg = self.model.calculate_overall_esg(stable_esg, esg, var)
                outputs.append("The updated ESG scores are:\nEnvironmental:{:.2f}-->{:.2f}\nSocial:{:.2f}-->{:.2f}\nGovernance:{:.2f}-->{:.2f}"\
                            .format(*list(itertools.chain.from_iterable(zip(stable_esg, new_esg)))))
            except:
                outputs.append("Failed to analyse. Try again!")
                return outputs
        return outputs

    def message_handling(self, user_message):
        outputs = []
        if len(self.check_for_url(user_message)) > 0:
            url = self.check_for_url(user_message)
            feeder = NewsFeeder(ticker=None)
            success, summary, _, news = feeder.analyse_url(url)
            print(success, summary)
            outputs.append(f"Here is the news summary:\n{news}")
            return self.generate_esg_report(None, success, summary, outputs)
        elif user_message not in self.esg_database["Symbol"].to_list():
            return self.error_handling(user_message, TICKER_NOT_FOUND)
        else:
            ticker = user_message
        feeder = NewsFeeder(ticker=ticker)

        ### Hard code
        '''
        if ticker == 'CVX':
            hyperlink = "https://www.zacks.com/stock/news/2251751/chevron-cvx-invests-in-carbon-capture-firm-ion-clean-energy"
            text = "Chevron (CVX) invests in ION Clean Energy, a developer of advanced carbon capture technology for industrial emissions, aiming to accelerate commercialization and combat climate change."
        elif ticker == 'PCCYF':
            hyperlink = "https://www.scmp.com/business/article/3256971/petrochina-track-peak-carbon-emissions-double-output-powered-low-carbon-energy-top-executives"
            text = "The nation's largest oil and gas producer says it is on track to peak carbon emissions next year and double the contribution of low-carbon energy to its output capacity over two years, top leaders say."
        else:
            return self.error_handling(user_message, NEWS_NOT_FOUND)
        
        outputs.append(f"Here is the recent news article link relating to ESG:\n{hyperlink}\nHere is the news summary:\n{text}")
        '''
        ### Hard code

        data = feeder.get_offline()
        success, summary, response = feeder.analyse_news(data, index=22)
        #success, summary, _ = feeder.analyse_news_offline()
        outputs = self.generate_esg_report(ticker, success, summary, outputs)
        
        return outputs

    def error_handling(self, user_message, error):
        text = None
        if error == TICKER_NOT_FOUND:
            text = f"Sorry, the company {user_message} is not found. Please check if you have input correctly."
        if error == NEWS_NOT_FOUND:
            text = f"Sorry, recent ESG news for {user_message} are currently unavailable. Please try again later or search for other companies."
        return [text,]
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    font = QFont("Calibri")
    app.setFont(font)
    window = ChatbotApp()
    window.setWindowIcon(QIcon('Chatbot icon.png'))
    window.reset()
    window.show()
    sys.exit(app.exec_())
