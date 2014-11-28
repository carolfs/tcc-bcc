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

# Este modelo é de autoria de Dobay, Caticha e Baldo
# Veja:
# Eduardo Sangiorgio Dobay. Complexidade e tomada de decisão.
# Dissertação de mestrado, Universidade de São Paulo, 2014.

import random

# Dá todas as possíveis tuplas binárias com n elementos
def perms(n, l = []):
    if n == 1:
        return [(0,), (1,)]
    else:
        nl = []
        for i in perms(n - 1, l):
            nl.append(i + (0,))
            nl.append(i + (1,))
        return nl

def agente_x(g, k, eta):
    mem = {p: (0, 0) for p in perms(k)}
    s = []
    for t, x in enumerate(g):
        assert eta in mem.keys()
        j, mi = mem[eta]
        p0 = (j + 1) / (mi + 2)
        if p0 < 0.5:
            y = 0
        elif p0 > 0.5:
            y = 1
        else:
            y = random.choice((0, 1))
        s.append(y)
        mem[eta] = (j + int(x == 1), mi + 1)
        eta = eta[1:] + (x,)
    return s

def agente_xy(g, k, eta):
    mem = {}
    for p1 in perms(k):
        for p2 in perms(k):
            mem[(p1, p2)] = (0, 0)
    s = []
    for t, x in enumerate(g):
        assert eta in mem.keys()
        j, mi = mem[eta]
        p0 = (j + 1) / (mi + 2)
        if p0 < 0.5:
            y = 0
        elif p0 > 0.5:
            y = 1
        else:
            y = random.choice((0, 1))
        s.append(y)
        mem[eta] = (j + int(x == 1), mi + 1)
        eta = (eta[0][1:] + (x,), eta[0][1:] + (y,))
    return s

# Resultado igual ao do agente xy
def agente_rs(g, k, eta):
    mem = {}
    for p1 in perms(k):
        for p2 in perms(k):
            mem[(p1, p2)] = (0, 0)
    y_ant = eta[1][-1]
    s = []
    for t, x in enumerate(g):
        assert eta in mem.keys()
        j, mi = mem[eta]
        p0 = (j + 1) / (mi + 2)
        if p0 < 0.5:
            sgm = 1
        elif p0 > 0.5:
            sgm = 0
        else:
            sgm = random.choice((0, 1))
        y = y_ant if sgm == 0 else 1 - y_ant
        s.append(y)
        rho = int(x == y)
        mem[eta] = (j + int(rho != sgm), mi + 1)
        eta = (eta[0][1:] + (x,), eta[0][1:] + (y,))
    return s
