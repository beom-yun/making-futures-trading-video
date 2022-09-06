import os
import sys
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from edit_movie import *
from read_csv_file import *


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form_class = uic.loadUiType(resource_path('form.ui'))[0]


class MyWindow(QWidget, form_class):
    def __init__(self):
        self.table_header = ['선택', '종목코드', '종목명', '구분', '체결가',
                             '수량', '주문시간', '청산가', '청산시간', '통화', '거래소']
        self.video = None
        self.transactions = None
        self.check_boxes = []

        super().__init__()
        self.setupUi(self)
        self.init_ui(self.table_header)

        self.btn_video_open.clicked.connect(self.video_open)
        self.btn_csv_open.clicked.connect(self.csv_open)
        self.btn_make.clicked.connect(self.make_videos)

    def init_ui(self, table_header):
        self.table.setColumnCount(len(table_header))
        self.table.setHorizontalHeaderLabels(table_header)
        self.table.horizontalHeader().sectionClicked.connect(self.select_clicked)

    def select_clicked(self, n):
        if n != 0:
            return
        b = True
        for check_box in self.check_boxes:
            b &= check_box.isChecked()
        for check_box in self.check_boxes:
            check_box.setChecked(False if b else True)

    def video_open(self):
        file_name = self.file_open()
        if not file_name:
            return None
        self.video = file_name
        self.label_video_name.setText(str(file_name.split('/')[-1]))
        self.dtEdit_movie.setDateTime(now())

    def csv_open(self):
        df = self.get_transactions()
        if not df:
            return
        self.transactions = df
        self.show_table(df)

    def file_open(self):
        file = QFileDialog.getOpenFileName(self)
        return file[0] if file[0] else None

    def get_transactions(self):
        file_name = self.file_open()
        if not file_name:
            return None
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
            self.check_boxes.append(check)

            # 1 ~ 열
            for j in range(1, len(self.table_header)):
                item = QTableWidgetItem(str(data[i][self.table_header[j]]))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def make_videos(self):
        if not self.video:
            print('원본 동영상 파일 필요')
            return
        if not self.transactions:
            print('체결내역 파일 필요')
            return
        options = self.get_options()

        edit_video(self.video, self.transactions, options)

    def get_options(self):
        options = {
            'prev_sec': int(self.spin_prev.text()),
            'after_sec': int(self.spin_after.text()),
            'start_time': self.dtEdit_movie.text(),
            'check_boxes': [check_box.isChecked() for check_box in self.check_boxes]
        }
        return options


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
