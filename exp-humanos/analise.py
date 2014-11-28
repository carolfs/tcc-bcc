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

import os
from statistics import mean

expdir = './exp1-resultados'
for fn in os.listdir(expdir):
    if fn[-4:] == '.txt' and fn[:4] == 'exp1':
        with open(os.path.join(expdir, fn)) as arq:
            nome, lado, memoria = arq.readline().split('\t')
            if nome == 'teste' or nome == 'test':
                continue
            if lado == '1':
                a = 1
                r = 0
            else:
                assert lado == '2'
                a = 0
                r = 1
            arq.readline()
            g = []
            s = []
            mem = 0
            for linha in arq:
                partes = linha.split('\t')
                assert len(partes) == 8
                if partes[2] != 'None':
                    g.append(a if partes[1] == 'a' else r)
                    s.append(a if partes[2] == 'a' else r)
                mem += float(partes[6])
            mem /= 200
            assert len(g) == 200
            assert len(s) == 200
            i = 50
            print(nome, int(memoria), mean(s[0:i]), mean(s[i:2*i]), mean(s[2*i:3*i]), mean(s[3*i:]), mem, sep='\t')