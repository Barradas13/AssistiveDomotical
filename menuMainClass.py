import observerClasses
from observerClasses import DataEvent, Observable
import PySimpleGUI as sg
from observerClasses import Observer


class Menu(Observer):
    def __init__(self):
        self.botoes = ['Facebook', 'Twitter', 'Instagram', 'LinkedIn', 'YouTube']
        self.botao_selecionado = 0
        self.window = None

    def create_layout(self):
        layout = [[sg.Button(button, key=f'button_{i}', button_color=('white', 'blue'), size=(15, 5)) for i, button in enumerate(self.botoes)]]
        return layout

    def run(self):
        self.window = sg.Window('Social Media Buttons', self.create_layout(), size=(750, 200))

        while True:
            event, values = self.window.read()
            if event in (sg.WINDOW_CLOSED, 'Exit'):
                break

            for i, button in enumerate(self.botoes):
                if event == f'button_{i}':
                    self.selecionar_botao(button)
                    self.highlight_botaoSelecionado()
                    self.mostrar_prompt_interacao()

        self.window.close()

    def selecionar_botao(self, button):
        self.botao_selecionado = self.botoes.index(button)

    def selecionar_botao_direita(self):
        # Função para selecionar o próximo botão.
        self.botao_selecionado = (self.botao_selecionado + 1) % len(self.botoes)
        print("")

    def interagir_botao_selecionado(self):
        selected_button = self.botoes[self.botao_selecionado]
        print(f'Interacting with {selected_button} button!')
        return selected_button

    def mostrar_prompt_interacao(self):
        selected_button = self.botoes[self.botao_selecionado]
        print(f'Selected {selected_button} button!')
        return selected_button

    def highlight_botaoSelecionado(self):
        for i, button in enumerate(self.botoes):
            if i == self.botao_selecionado:
                self.window[f'button_{i}'].update(button_color=('white', 'green'))
            else:
                self.window[f'button_{i}'].update(button_color=('white', 'blue'))


    def update(self,  subject: Observable, dataEvent: DataEvent) -> None:
        try:
            if dataEvent.piscou and dataEvent.tempo < 0.7:
                self.selecionar_botao_direita()
                self.highlight_botaoSelecionado()
                self.mostrar_prompt_interacao()
            elif dataEvent.piscou and dataEvent.tempo > 0.7:
                self.interagir_botao_selecionado()
                self.mostrar_prompt_interacao()
        except AttributeError:
            pass

        print(self.selection)