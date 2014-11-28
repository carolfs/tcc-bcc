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

# Experimentos 4 e 5 da monografia

from q_learning import qlearn, escolha_gibbs
from dcb import agente_x, perms
import locale
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from statistics import mean, stdev
from random import random, choice

num_aps = 300

# Q-Learning
vs = []
for k in range(6):
    escolha = escolha_gibbs(1)
    dados = [
        qlearn([1 if random() < 0.7 else 0 for j in range(num_aps)], k, 0.5, 0.99, escolha, 1, -1)
        for i in range(1000)]
    y = [mean([s[i] for s in dados]) for i in range(num_aps)]
    vs.append(y)
for i in range(num_aps):
    for v in vs:
        print(v[i], end='\t')
    print()
print()
    
# DCB    
vs = []
for k in range(1, 6):
    ps = perms(k)
    dados = [
        agente_x([1 if random() < 0.7 else 0 for j in range(num_aps)], k, choice(ps))
        for i in range(1000)]
    y = [mean([s[i] for s in dados]) for i in range(num_aps)]
    vs.append(y)
for i in range(num_aps):
    for v in vs:
        print(v[i], end='\t')
    print()
