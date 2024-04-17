from PyQt5 import QtWidgets, QtCore, QtGui
from Model import *
from NewsFeeder import *

class ChatbotApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.model = SentimentalModel()
        # 设置窗口标题和尺寸
        self.setWindowTitle("Chatbot")
        self.setGeometry(100, 100, 500, 400)

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

        # 创建退出按钮
        self.exit_button = QtWidgets.QPushButton("Exit")
        input_layout.addWidget(self.exit_button)
        self.exit_button.clicked.connect(self.close)  # 连接退出按钮的点击事件到 close 方法

        # 将输入布局添加到主布局
        layout.addLayout(input_layout)

        # 设置主布局
        self.setLayout(layout)

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
            # 示例响应
            bot_response = f"{outputs}"
            self.add_message("Chatbot", bot_response)

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

    def message_handling(self, user_message):
        feeder = NewsFeeder(ticker=user_message)
        credit_model = CreditModel()
        news = feeder.get()
        success, summary, _ =  feeder.analyse_news(news)

        return outputs

        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ChatbotApp()
    window.show()
    sys.exit(app.exec_())
