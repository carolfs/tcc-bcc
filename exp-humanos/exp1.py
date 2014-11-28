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

# Experimento 1 - Espacial, com tarefa de memória
# 
# Ele é composto de dois módulos, comum.py e exp1.py
# O experimento é iniciado com o comando
# $ python exp1.py [nome] [lado] [dif]
# no qual:
#   [nome] se refere ao nome do voluntário
#   [lado] ao lado em maioria na escolha binária (1 = esquerda, 2 = direita)
#   [dif] à dificuldade do experimento de memória (1 = fácil, 2 = difícil)
#
# Deve ser rodado em Python 2 (o psychopy não roda em Python 3)

from __future__ import absolute_import, division, unicode_literals, print_function, nested_scopes
from comum import Experimento, KEYL, KEYR, inf, seq_binaria
import sys, random

nome = sys.argv[1]
lado = sys.argv[2]
dif = sys.argv[3]
if lado not in ('1', '2'):
    sys.stderr.write('Segundo parâmetro incorreto!\n')
    sys.exit(0)
if dif not in ('1', '2'):
    sys.stderr.write('Terceiro parâmetro incorreto!\n')
    sys.exit(0)
    
n = 4
memoria = 1 if dif == '1' else n

exp = Experimento(1, nome)
exp.log('%s\t%s\t%d\n\n' % (nome, lado, memoria))

# Treino
i = 0
while True:
    key = exp.mostra_mensagem('Treino', ('num_0', 'escape'))
    if key == 'escape':
        break
    if i % 2 == 0:
        k = KEYL
    else:
        k = KEYR
    exp.escbin(inf, k, log=False)
    if memoria > 0:
        exp.memoria_espacial(inf, n, memoria, log=False)
    exp.fim_trial(False)
    i += 1
exp.zerar_recompensa()

# Calcula as respostas do experimento de escolha binária
seq = seq_binaria(lado, 200)

# Mensagem inicial
exp.mostra_mensagem('Início', ('num_0'))
for r in seq:
    while True:
        resp = exp.escbin(1, r)
        if memoria > 0:
            exp.memoria_espacial(2, n, memoria)
        exp.fim_trial(True)
        if resp is not None:
            break
exp.mostra_mensagem('Fim', ('escape',))