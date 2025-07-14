import wx
from padroes.abcClasses import DataEvent

class Menu(wx.Frame):
    def __init__(self):
        super().__init__(None, title="MENU INTERAÇÃO FACIAL", size=(600, 150))
        self.botoes = ['TELEVISÃO', 'LUZ DA SALA', 'LUZ DA COZINHA', 'AR CONDICIONADO']
        self.botao_selecionado = -1
        self.piscando = False
        self.piscandoInicio = 0
        self.piscandoFim = 0

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_widgets = []
        for i, label in enumerate(self.botoes):
            btn = wx.Button(panel, label=label, size=(130, 60))
            btn.Bind(wx.EVT_BUTTON, self.make_on_click(i))
            hbox.Add(btn, flag=wx.ALL, border=5)
            self.btn_widgets.append(btn)

        panel.SetSizer(hbox)
        self.Centre()
        self.Show()

    def make_on_click(self, index):
        def on_click(event):
            self.selecionar_botao(index)
        return on_click

    def selecionar_botao(self, index):
        self.botao_selecionado = index
        self.highlight_botaoSelecionado()
        self.mostrar_prompt_interacao()

    def highlight_botaoSelecionado(self):
        for i, btn in enumerate(self.btn_widgets):
            if i == self.botao_selecionado:
                btn.SetBackgroundColour(wx.Colour(0, 0, 255))  # azul
            else:
                btn.SetBackgroundColour(wx.Colour(240, 240, 240))  # padrão

            btn.Refresh()

    def mostrar_prompt_interacao(self):
        if self.botao_selecionado >= 0:
            print(f'Selected {self.botoes[self.botao_selecionado]} button!')

    def selecionar_botao_direita(self):
        self.botao_selecionado = (self.botao_selecionado + 1) % len(self.botoes)
        self.highlight_botaoSelecionado()
        self.mostrar_prompt_interacao()

    def interagir_botao_selecionado(self, tempo):
        if self.botao_selecionado >= 0:
            print(f'Interacting with {self.botoes[self.botao_selecionado]} button! Tempo piscando: {tempo:.2f}s')

    def muda_btn(self):
        self.selecionar_botao_direita()

    def interage_btn(self, tempo):
        self.interagir_botao_selecionado(tempo)

    def update(self, dataEvent: DataEvent) -> None:
        # Como update pode vir de outra thread, agende o processamento na thread da GUI
        wx.CallAfter(self._process_update, dataEvent)

    def _process_update(self, dataEvent: DataEvent):
        try:
            if dataEvent.ear < 0.27 and not self.piscando:
                self.piscando = True
                self.piscandoInicio = dataEvent.inicio
            elif dataEvent.ear > 0.27 and self.piscando:
                self.piscando = False
                self.piscandoFim = dataEvent.inicio
                tempoPiscando = self.piscandoFim - self.piscandoInicio
                if tempoPiscando > 1.5:
                    self.interage_btn(tempoPiscando)
                elif tempoPiscando > 0.3:
                    self.muda_btn()
        except Exception as e:
            print(f"Erro no update: {e}")

# Código para rodar a aplicação:
if __name__ == "__main__":
    app = wx.App()
    menu = Menu()
    app.MainLoop()
