import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QLineEdit, QSizePolicy, QPushButton
import json
import os
import observerClasses
from observerClasses import DataEvent, Observable

with open(os.path.join('dadosMenu.json'),'r') as arquivo:
    dados = json.load(arquivo)

class Menu(observerClasses.ConcreteObserverA):
    qtdBotoes = len(dados['botoes'])

    def update(self, subject: Observable, dataEvent: DataEvent) -> None:


        if dataEvent.piscou and dataEvent.tempo > 0.7:
            print('fazendo função')
        else:
            self.selection += 1

            if self.selection > self.qtdBotoes:
                self.selection = 1
            print('trocando botao')

        print(self.selection)

        return super().update(subject, dataEvent)


class App(QMainWindow):
    def __init__(self, parent = None ):
        super().__init__(parent)
        self.setWindowTitle('Menu')
        self.setFixedSize(700,200)
        self.cw = QWidget()
        self.grid = QGridLayout(self.cw)
        
        c = 1
        
        #Adicionando o display
        self.display = QLineEdit()
        self.grid.addWidget(self.display, 0, 0, 1, 7)
        self.display.setDisabled(True)
        self.display.setStyleSheet(
        '*{background-color:white; font-size:30px}'
            )
        
        for i in dados['botoes']:
            print(i)
            self.add_btn(QPushButton(dados['botoes'][i]['title']), 1, c, 1, 1, dados['botoes'][i]['funcao'])
            c += 1

        self.display.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.setCentralWidget(self.cw)

    def add_btn(self, btn, linha, colum, rospam, coldspan, funçao=None):
        self.grid.addWidget(btn, linha, colum, rospam, coldspan)

        btn.clicked.connect(
               lambda:self.display.setText(
                   funçao
                )
            )

        btn.setStyleSheet('*{background-color:white; font-size:30px;border-color:black;}')
        btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)


menu = Menu()

if __name__ == "__main__":
    qt = QApplication(sys.argv)
    app = App()

    app.show()
    qt.exec()