import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from read_csv_file import *

form_class = uic.loadUiType('qt/form.ui')[0]


class MyWindow(QWidget, form_class):
    def __init__(self):
        self.table_header = ['선택', '종목명', '구분', '체결가',
                             '수량', '주문시간', '청산가', '청산시간', '통화', '거래소']

        super().__init__()
        self.setupUi(self)
        self.init_ui(self.table_header)

        self.btn_video_open.clicked.connect(self.video_open)
        self.btn_csv_open.clicked.connect(self.csv_open)

    def init_ui(self, table_header):
        self.table.setColumnCount(len(table_header))
        self.table.setHorizontalHeaderLabels(table_header)

    def video_open(self):
        file_name = self.file_open()
        print('video file', file_name)

    def csv_open(self):
        df = self.get_transactions()
        if df:
            self.show_table(df)

    def file_open(self):
        file = QFileDialog.getOpenFileName(self)
        return file[0] if file[0] else None

    def get_transactions(self):
        file_name = self.file_open()
        if not file_name:
            return
        self.label_csv_name.setText(str(file_name.split('/')[-1]))
        return read_csv_file(file_name)

    def show_table(self, data):
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setRowCount(len(data))

        for i in range(len(data)):
            # 0열 체크박스
            check = QCheckBox()
            check.setChecked(True)
            cellWidget = QWidget()
            layoutCB = QHBoxLayout(cellWidget)
            layoutCB.addWidget(check)
            layoutCB.setAlignment(Qt.AlignCenter)
            layoutCB.setContentsMargins(0, 0, 0, 0)
            cellWidget.setLayout(layoutCB)
            self.table.setCellWidget(i, 0, cellWidget)

            # 1 ~ 열
            for j in range(1, len(self.table_header)):
                item = QTableWidgetItem(str(data[i][self.table_header[j]]))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
