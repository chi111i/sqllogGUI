from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout
from PySide6 import QtWidgets
from PySide6.QtCore import QEventLoop, QTimer
from ui_sql import Ui_MainWindow
from PySide6 import QtCore, QtGui
import re
import sys



class EmittingStr(QtCore.QObject):
    textWritten = QtCore.Signal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
        loop = QEventLoop()
        QTimer.singleShot(1, loop.quit)
        loop.exec()
        QApplication.processEvents()
class MyWidget(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 设置标题
        self.setWindowTitle("sql日志分析 by chi11i")
        self.plainTextEdit_2.setAcceptDrops(False)   # 禁用文本框的拖拽事件
        self.setAcceptDrops(True)# 启用窗口的拖拽事件
        self.comboBox.setEditable(True)
        self.pushButton.clicked.connect(self.test)
        self.pushButton_2.clicked.connect(self.sqllog)
        
        sys.stdout = EmittingStr()
        sys.stdout.textWritten.connect(self.outputWritten)

       

        sys.stdout = EmittingStr()
        self.textBrowser.connect(sys.stdout, QtCore.SIGNAL("textWritten(QString)"), self.outputWritten)
        sys.stderr = EmittingStr()
        self.textBrowser.connect(sys.stderr, QtCore.SIGNAL("textWritten(QString)"), self.outputWritten)


    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()






    def test(self):
        
        a=self.lineEdit.text()
        c=self.comboBox.currentText()

        number_pattern =re.compile(r'{}'.format(c))

        flag=number_pattern.findall(a)
        #print(flag)



        self.textBrowser.setPlainText(str(flag))

    def dragEnterEvent(self, event):
        # 检测拖拽的对象是否是文件
        if event.mimeData().hasUrls():
            event.accept() # 接受事件
        else:
            event.ignore() # 忽略事件

    def dropEvent(self, event):
        # 获取拖拽的文件的路径
        file_path = event.mimeData().urls()[0].toLocalFile()
        #print(file_path)
        # 打开文件


        self.plainTextEdit_2.setPlainText(str(file_path))



    def sqllog(self):

        # 用到的一些变量
        payload_list = []
        result_dict = {}
        result_list = []
        
        # 根据不同的日志填写不同的正则 请灵活修改
        # re_strbool = "0,1\)\),\s(\d+),.+>(\d+)"
        # re_strtime = "flag\),(\d+),\S+='(\d+)"
        args=self.plainTextEdit_2.toPlainText()
        re_str=self.comboBox.currentText()
        print("正在使用的正则表达式:", re_str)

        try:
            print("正在读取分析文件:", args)
            f = open(args, "r", encoding='UTF-8')
            lines = ''.join(f.readlines()).split("\n")
            # print(lines)
            try:
                # 提取数字放入到列表中
                number_pattern = re.compile(r'{}'.format(re_str))
                flag = number = number_pattern.findall(lines[0])
                # print(flag)

                if flag:
                    for line in lines:
                        number = number_pattern.findall(line)
                        if number:
                            payload_list.append(number[0])
                            # print(number[0])  # 观察一些这个输出就清楚正则的写法了
                else:
                    print("正则表达式无法从目标文件提取数据")


                print("还原的明文结果:", end="")
                # 数据分析并转换编码
                # print(payload_list)
                for i in payload_list:
                    result_dict[i[0]] = i[1]
                    # print(i[1])
                for value in result_dict.values():
                    result_list.append(int(value))
                    # print(value)
                for j in result_list:
                    print(chr(j), end="")
                    

            except Exception as e:
                print("正则表达式语法有误")
        except Exception as e:
            print("文件路径或文件内容有误")









if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()



    sys.exit(app.exec())











