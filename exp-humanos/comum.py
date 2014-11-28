# -*- encoding: utf-8 -*-

#carolfs/tcc-bcc
#Copyright (C) 2014  Carolina Feher da Silva
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Análise dos experimentos com voluntários humanos
# Os resultados estão no diretório exp1-resultados

# Código comum aos experimentos
# Deve ser rodado em Python 2 (o psychopy não roda em Python 3)

from __future__ import absolute_import, division, unicode_literals, print_function, nested_scopes

from psychopy import visual, core, event
import random, math, sys, os, codecs, time

inf = float('inf')
# Teclas usadas na escolha binária
KEYL, KEYR = 'a', 'r'
# Recompensas a serem usadas no experimento
RECBINPOS = 1
RECBINNEG = 0
RECBINMISS = -10
RECMEM = 1
# Tempo de feedback
FEEDBACK_TIME = 1

def seq_binaria(lado, n):
    p = 0.7 if lado == '1' else 0.3
    return [KEYL if random.random() < p else KEYR for i in range(n)]

def pontos(r):
    if r == round(r, 0):
        r = int(r)
    else:
        r = round(r, 1)
    if r < 0:
        t = str(r)
    elif r > 0:
        t = '+' + str(r)
    else:
        t = '0'
    return t.replace('.', ',')

class Experimento(object):
    def __init__(self, num_exp, nome_sujeito):
        # Cria o arquivo de saída
        if not os.path.isdir('resultados'):
            os.mkdir('resultados')
        fn = ('resultados/exp%d-' % num_exp) + nome_sujeito + '.txt'
        if nome_sujeito == 'teste':
            fullscreen = False
        else:
            fullscreen = True
            if os.path.exists(fn):
                print('Este arquivo já existe. Escrever por cima? (s/n)', end='')
                resp = raw_input().strip()
                if resp != 's':
                    sys.exit()
        self._arq = codecs.open(fn, 'w', 'utf-8')
        self._rec = 0 # recompensa total
        
        # Cria a janela
        self._win = visual.Window(fullscr=fullscreen, units='height', color=(-0.5, -0.5, -0.5))
        self._win.setMouseVisible(False)
        
        # Criação dos objetos que serão desenhados
        self._msg = visual.TextStim(self._win, height=0.05, color='white', pos=(0, 0), alignHoriz='center')
        self._seq = visual.TextStim(self._win, height=0.2)
        self._rectl = visual.Rect(self._win, width=0.2, height=0.2, pos=(-0.4, 0))
        self._rectr = visual.Rect(self._win, width=0.2, height=0.2, pos=(+0.4, 0))
        self._rectm = visual.Rect(self._win, width=0.2, height=0.2, lineColor='DeepSkyBlue', fillColor='DeepSkyBlue')
        self._circl = visual.Circle(self._win, radius=0.075, edges=32, pos=(-0.4, 0), lineColor='Gold', fillColor='Gold')
        self._circr = visual.Circle(self._win, radius=0.075, edges=32, pos=(+0.4, 0), lineColor='Gold', fillColor='Gold')
        self._feedpos = visual.TextStim(self._win, height=0.15, color='Lime', pos=(0, 0.15), alignHoriz='center')
        self._feedzero = visual.TextStim(self._win, height=0.15, color='white', pos=(0, 0.15), alignHoriz='center')
        self._feedneg = visual.TextStim(self._win, height=0.15, color='red', pos=(0, 0.15), alignHoriz='center')
        self._total = visual.TextStim(self._win, height=0.05, color='white', pos=(0, 0.0), alignHoriz='center')
        
        # Recompensa total do voluntário
        self._rec = 0
    
    def zerar_recompensa(self):
        self._rec = 0
    
    def log(self, s):
        self._arq.write(s)
    
    def fim_trial(self, log=True):
        if log:
            self._arq.write('\t%.2f\n' % self._rec)
    
    # Qual feedback usar (muda a cor)
    def feedback(self, r):
        if r < 0:
            fb = self._feedneg
        elif r > 0:
            fb = self._feedpos
        else:
            fb = self._feedzero
        fb.setText(pontos(r))
        height = 0.01 * abs(r) + 0.1
        fb.setHeight(height)
        return fb
    
    # Mostra mensagem e espera até que o voluntário pressione uma tecla
    def mostra_mensagem(self, t, keyList=None):
        self._msg.setText(t)
        self._msg.draw()
        self._win.flip()
        allKeys = event.waitKeys(keyList=keyList)
        return allKeys[0]
    
    # Tarefa de escolha binária
    def escbin(self, maxWait, c, log = True):
        self._rectl.setLineColor('white')
        self._rectr.setLineColor('white')
        self._rectl.draw()
        self._rectr.draw()
        self._win.flip()
        kts = event.waitKeys(keyList=(KEYL, KEYR), maxWait=maxWait)
        if kts is not None:
            resp = kts[0]
        else:
            resp = None
        if resp is None:
            r = RECBINMISS
        elif resp == c:
            r = RECBINPOS
        else:
            r = RECBINNEG
        self._rec += r
        if log:
            self._arq.write('%f\t%s\t%s\t%.2f\t' % (core.getTime(), c, resp, r))
        self._rectl.draw()
        self._rectr.draw()
        if resp is not None:
            if c == KEYL:
                self._circl.draw()
            else:
                self._circr.draw()
        fb = self.feedback(r)
        fb.draw()
        self._total.setText(pontos(self._rec))
        self._total.draw()
        self._win.flip()
        core.wait(FEEDBACK_TIME)
        self._win.flip(clearBuffer=True)
        return resp
    
    # Tarefa de memória espacial
    # n: número de elementos da sequência
    # m: número de elementos que o sujeito deve repetir
    def memoria_espacial(self, maxWait, n, m = None, log = True):
        assert m > 0 and n > 0
        if m is None:
            m = n
        digits = list('123456789')
        random.shuffle(digits)
        digits = digits[:n]

        # Desenhando os quadrados
        xl, xm, xr = -0.4, 0, 0.4
        yu, ym, yd = 0.3, 0, -0.3
        digit_pos = {
            '1': (xl, yd),
            '2': (xm, yd),
            '3': (xr, yd),
            '4': (xl, ym),
            '5': (xm, ym),
            '6': (xr, ym),
            '7': (xl, yu),
            '8': (xm, yu),
            '9': (xr, yu),
        }
        for d in digits:
            self._rectm.setPos(digit_pos[d])
            self._rectm.draw()
            self._win.flip(clearBuffer=True)
            core.wait(0.5)
        
        self._win.flip(clearBuffer=True)
        
        # Obter resposta do problema de memória
        digits = digits[-m:] # Pegar só os m últimos elementos
        now = core.getTime()
        resp = ''
        while True:
            allKeys = event.waitKeys(timeStamped=True, maxWait=(maxWait - core.getTime() + now))
            if allKeys is None:
                break
            thisKey, t = allKeys[-1]
            try:
                if thisKey[4] in '123456789':
                    resp += thisKey[4]
            except IndexError:
                pass
            #elif thisKey == 'backspace':
            #    if len(resp) > 0:
            #        resp = resp[:-1]
            self._seq.setText(resp)
            self._seq.draw()
            self._win.flip()
            if (m == 0 and len(resp) == 1) or (m > 0 and len(resp) == len(digits)):
                break
        if len(resp) < len(digits):
            resp += '-' * (n - len(resp))
        if m == 0:
            r = len(resp) * RECMEM
        else:
            r = sum([1 if s == c else 0 for s, c in zip(resp, digits)]) / len(digits) * RECMEM
        self._rec += r
        if log:
            self._arq.write('%s\t%s\t%.2f' % (''.join(digits), resp, r))
        fb = self.feedback(r)
        fb.draw()
        self._total.setText(pontos(self._rec))
        self._total.draw()
        self._win.flip()
        core.wait(FEEDBACK_TIME)