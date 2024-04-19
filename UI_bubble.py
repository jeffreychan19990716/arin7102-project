from PyQt5 import QtWidgets, QtCore, QtGui
from NewsFeeder import *
from Model import *
import pandas as pd

def search_database(database, ticker):
    data = database.loc[database['ticker'] == ticker]
    stable_esg = [data["e"].values[0], data["s"].values[0], data["g"].values[0]] # yahoo fiance
    var = data["var"].values[0] # https://www.macroaxis.com/invest/technicalIndicator/JNJ/Variance
    return stable_esg, var

class ChatbotApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.model = SentimentalModel()
        self.esg_database = pd.read_csv("database.csv")
        # 设置窗口标题和尺寸
        self.setWindowTitle("Chatbot")
        self.setGeometry(100, 100, 1000, 800)

        # 创建主布局
        layout = QtWidgets.QVBoxLayout()

        # 创建对话框（使用 QListWidget 来显示对话）
        self.chat_list = QtWidgets.QListWidget()
        layout.addWidget(self.chat_list)

        # 创建输入布局（用于输入框、发送按钮和退出按钮）
        input_layout = QtWidgets.QHBoxLayout()

        # 创建文本输入框
        self.input_box = QtWidgets.QLineEdit()
        input_layout.addWidget(self.input_box)

        # 创建发送按钮
        self.send_button = QtWidgets.QPushButton("Send")
        input_layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_message)

        # 创建清空按钮
        self.reset_button = QtWidgets.QPushButton("Restart")
        input_layout.addWidget(self.reset_button)
        self.reset_button.clicked.connect(self.reset)

        # 创建退出按钮
        self.exit_button = QtWidgets.QPushButton("Exit")
        input_layout.addWidget(self.exit_button)
        self.exit_button.clicked.connect(self.close)  # 连接退出按钮的点击事件到 close 方法

        # 将输入布局添加到主布局
        layout.addLayout(input_layout)

        # 设置主布局
        self.setLayout(layout)

    def reset(self):
        self.chat_list.clear()
        self.input_box.clear()
        self.add_message("Chatbot", "Input company ticker")

    def send_message(self):
        # 获取用户输入的消息
        user_message = self.input_box.text()
        if user_message.strip():
            # 将用户消息添加到对话框中
            
            self.add_message("You", user_message)
            outputs = self.message_handling(user_message)

            # 清空输入框
            self.input_box.clear()

            # 这里可以添加聊天机器人的逻辑，将响应显示在对话框中
            for output in outputs:
                self.add_message("Chatbot", output)

    def add_message(self, sender, message):
        # 创建一个 QListWidgetItem 对象
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight) if sender == "You" else item.setTextAlignment(QtCore.Qt.AlignLeft)

        # 设置气泡样式表
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)

        label = QtWidgets.QLabel(message)
        label.setWordWrap(True)


        # 设置气泡样式
        label.setStyleSheet(f"""
            background-color: {'#e1f5fe' if sender == 'You' else '#dcedc8'};
            border-radius: 10px;
            padding: 10px;
        """)

        layout.addWidget(label)
        layout.setContentsMargins(10, 5, 10, 5)  # 设置外边距
        layout.setAlignment(QtCore.Qt.AlignRight if sender == "You" else QtCore.Qt.AlignLeft)
        widget.setLayout(layout)

        # 将自定义的小部件添加到 QListWidgetItem
        item.setSizeHint(widget.sizeHint())
        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, widget)

        # 滚动到底部以显示最新消息
        self.chat_list.scrollToBottom()

    def format_esg_text(self, content):
        if type(content[0]) is str:
            text = "Environmental:{e}\nSocial:{s}\nGovernance:{g}".format(e=content[0], s=content[1], g=content[2])
        else:
            text = "Environmental:{e:.2f}\nSocial:{s:.2f}\nGovernance:{g:.2f}".format(e=content[0], s=content[1], g=content[2])
        return text

    def message_handling(self, user_message):
        ticker = user_message
        feeder = NewsFeeder(ticker=ticker)
        #data = feeder.get()
        #success, summary, _ =  feeder.analyse_news(data, index=0)
        success, summary, _ =  feeder.analyse_news_offline()
        if not success:
            return ["Failed to analyse. Try again!"]
        esg = [self.model.predict(x) for x in summary]
        
        stable_esg, var = search_database(self.esg_database, ticker)
        new_esg = self.model.calculate_overall_esg(stable_esg, esg, var)

        outputs = []
        outputs.append(f"News summary:\n")
        for s in summary:
            outputs.append(s)
        outputs.append(f"News ESG:\n{self.format_esg_text(esg)}")
        outputs.append(f"Original ESG:\n{self.format_esg_text(stable_esg)}")
        outputs.append(f"Updated ESG:\n{self.format_esg_text(new_esg)}")
        return outputs

        

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ChatbotApp()
    window.reset()
    window.show()
    sys.exit(app.exec_())
