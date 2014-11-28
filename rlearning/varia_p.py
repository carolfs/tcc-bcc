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

# Imprime os dados do Q-Learning para vários valores de p
# Veja o experimento 3 da monografia

import random
from math import exp
import sys
from statistics import mean, stdev
import locale
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from q_learning import qlearn, escolha_gibbs

if __name__ == '__main__':
    gama = 0.99
    alfa = 0.5
    tau = 1
    fesc = escolha_gibbs(tau)
    k = 3
    vp = 1
    vn = -1
    num_aps = 300
    reps = 1000
    
    for p in (0.5, 0.6, 0.7, 0.8, 0.9, 1):
        resultados = []
        for rep in range(reps):
            g = tuple(1 if random.random() < p else 0 for i in range(num_aps))
            s = qlearn(g, k, alfa, gama, fesc, vp, vn)
            resultados.append((g, s))
        
        y = np.array([mean([s[i] for g, s in resultados]) for i in range(num_aps)])
        print(p, *y, sep="\t")