from tkinter import *
import random
import time
import sys


gameWindow = Tk()
gameWindow.title("BOUNCY BALL")
gameWindow.geometry("1000x600+100+100")
gameWindow.resizable(0, 0)
gameWindow.wm_attributes("-topmost", 1)
canva = Canvas(gameWindow, width = 1000, height = 500, bd = 0, highlightthickness = 0)
canva.configure(bg = "#781000")
canva.pack()
gameWindow.update()

class Bola:
  def __init__ (self, canvas, base, cor, contadorPontos):
    self.canvas = canvas
    self.base = base
    self.id = canvas.create_oval(0, 0, 30, 30, fill = cor)
    self.canvas.move(self.id, 245, 100)
    comeca = [-3, -2, -1, 0, 1, 2, 3]
    random.shuffle(comeca)
    self.x = comeca[0]
    self.y = -3
    self.canvasAltura = self.canvas.winfo_height()
    self.canvasLargura = self.canvas.winfo_width()
    self.tocaChao = False
    self.contadorPontos = contadorPontos


  def tocarBase(self, posicao):
    basePosicao =  self.canvas.coords(self.base.id)
    if posicao[2] >= basePosicao[0] and posicao[0] <= basePosicao[2]:
      if posicao[3] >= basePosicao[1] and posicao[3] <= basePosicao[3]:
        self.contadorPontos += 1
        return True
      return False
  

  def getContadorPontos(self):
    return self.contadorPontos


  def movimentacao(self) :
      self.canvas.move(self.id,self.x, self.y)
      posicao = self.canvas.coords(self.id)

      if posicao[1] <= 0:
        self.y = 3

      if posicao[3] >= self.canvasAltura:
        self.y = -3
        self.tocaChao = True

      if posicao[0] <= 0:
        self.x = 3

      if posicao[2] >= self.canvasLargura:
        self.x = -3

      if self.tocarBase(posicao) == True:
        self.y = -3

      if self.tocarObstaculo(posicao) == True:
        self.y = 3


class Base:
  def __init__ (self, canvas, cor):  
    self.canvas = canvas
    self.id = canvas.create_rectangle(0, 0, 500, 500, fill = cor)
    self.canvas.move(self.id, 0, 490)
    self.x = 0

    self.canvasLargura = self.canvas.winfo_width()
    self.canvas.bind_all("<KeyPress-Left>", self.movimentoEsquerdaSeta)
    self.canvas.bind_all("<KeyPress-Right>", self.movimentoDireitaSeta)
    self.canvas.bind_all("<KeyPress-Up>", self.pararTeclado)
    self.canvas.bind_all("<KeyPress-Down>", self.pararTeclado)
    

  def movimentacao(self) :
   self.canvas.move(self.id, self.x, 0)
   posicao = self.canvas.coords(self.id)

   if posicao[0] <= 0:
     self.x = 0

   if posicao[2] >= self.canvasLargura:
      self.x = 0


  def movimentoEsquerdaSeta(self, evt):
    self.x = -2


  def movimentoDireitaSeta(self, evt):
    self.x = 2


  def pararTeclado(self, evt):
    self.x = 0


  def movimentoEsquerdaBotao(self):
    self.x = -2


  def movimentoDireitaBotao(self):
    self.x = 2


  def pararBotao(self):
    self.x = 0


class quadrado:
  def __init__(self, canva):
    self.canva = canva
    self.posicaoX = random.randint(0, 1000)
    self.posicaoY = random.randint(0, 400)
    self.id = self.canva.create_rectangle(0, 0, self.posicaoX, self.posicaoY, fill = "#00f0ff")

    
  def tocarObstaculo(self, posicao, bola):
    self.bola = bola
    posicao = self.canvas.coords(self.id)
    bolaPosicao =  self.canvas.coords(self.bola.id)
    if bolaPosicao[0] >= posicao[2]  and  bolaPosicao[2] <= posicao[0]:
      if bolaPosicao[1] >= posicao[3] and  bolaPosicao[3] <= posicao[3]:
        return True
      return False


def sair():
  sys.exit(0)


class Inicio:
  def __init__(self, canva):
    self.canvas = canva
    self.canvas.delete("all")
    self.contadorPontos = 0

    self.base = Base(self.canvas, "#ff5f00")
    self.bola = Bola(self.canvas, self.base,"#0ea3ed", self.contadorPontos)
    self.contadorPontos = self.bola.getContadorPontos()
    self.nivel = 0
    self.contadorPontoNivel = 0

  
  def executando(self):
    self.infomacoes = Label(gameWindow, width = 30, height = 4, padx = 3, text="Pontuação: 0 \n Nível: 1", font=("Arial", 15),bg="#fff")
    self.infomacoes.place(x=300, y=500)
    contNivel = 2
    while 1:
      self.bola.movimentacao()
      self.base.movimentacao()
      self.contadorPontos = self.bola.getContadorPontos()
      if self.contadorPontos % 5 == 0:
        if self.contadorPontoNivel == 0:
          self.nivel += 1
          self.contadorPontoNivel = 1
      if self.contadorPontos % 5 != 0:
        self.contadorPontoNivel = 0

      if self.bola.tocaChao:
        self.canvas.create_text(500, 250, text="GAMEOVER", font=("Arial", 50), fill = "#FFF")
        break
      
      if self.nivel == contNivel:
        quadrados = quadrado(canva)
        contNivel += 1

      
      self.info = str(f"Pontuação: {self.contadorPontos} \n Nível: {self.nivel}")
      self.infomacoes["text"] = self.info

      gameWindow.update_idletasks()
      gameWindow.update()
      time.sleep(0.01)


def iniciar():
  inicio = Inicio(canva)

  botaoDireita = Button(gameWindow, width = 10, height = 2, text="Direita →", bg="orange",command = inicio.base.movimentoDireitaBotao)
  botaoDireita.place(x=890, y=500)

  botaoEsquerda = Button(gameWindow, width = 10, height = 2, text="← Esquerda", bg="orange", command = inicio.base.movimentoEsquerdaBotao)
  botaoEsquerda.place(x=780, y=500)

  botaoParado = Button(gameWindow, width = 24, height = 2, text="Parado ↓↑", bg="orange", command = inicio.base.pararBotao)
  botaoParado.place(x=780, y=550)

  inicio.executando()


botaoComecar = Button(gameWindow, width = 15, text="Começar", bd=0, bg="green", font=("Ubuntu-bold", 10), foreground="#fff", cursor = "hand2", command = iniciar)
botaoComecar.place(x=20, y=515)

botaoSair = Button(gameWindow, width = 15, text="Sair", bd=0, bg="red", font=("Ubuntu-bold", 10), foreground="#fff", cursor = "hand2", command = sair)
botaoSair.place(x=20, y=545)

gameWindow.mainloop()
