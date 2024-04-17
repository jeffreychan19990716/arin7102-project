from PyQt5 import QtWidgets, QtGui
from sentiment import *

class ChatbotApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.model = SentimentalModel()
        # 设置窗口标题和尺寸
        self.setWindowTitle("Chatbot")
        self.setGeometry(100, 100, 500, 400)

        # 创建主布局
        layout = QtWidgets.QVBoxLayout()

        # 创建对话框（文本编辑器，用于显示对话）
        self.text_area = QtWidgets.QTextEdit()
        self.text_area.setReadOnly(True)  # 设置为只读
        layout.addWidget(self.text_area)

        # 创建输入布局（用于输入框和发送按钮）
        input_layout = QtWidgets.QHBoxLayout()

        # 创建文本输入框
        self.input_box = QtWidgets.QLineEdit()
        input_layout.addWidget(self.input_box)

        # 创建发送按钮
        self.send_button = QtWidgets.QPushButton("Send")
        input_layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_message)

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
            # 将用户消息显示在对话框中
            self.text_area.append(f"You: {user_message}")
            print(user_message)
            news = seperate(user_message)
            outputs = {}
            outputs["Enviornmental"] = self.model.predict(news["e"])
            outputs["Social"] = self.model.predict(news["s"])
            outputs["Goverance"] = self.model.predict(news["g"])



            # 清空输入框
            self.input_box.clear()

            # 这里可以添加聊天机器人的逻辑，将响应显示在对话框中
            # 示例响应
            bot_response = f"ChatBot: {outputs}"
            self.text_area.append(bot_response)

if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    window = ChatbotApp()
    window.show()
    sys.exit(app.exec_())