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

# Q-Learning

import random
from math import exp
import sys
from statistics import mean, stdev
import configparser
import locale
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Permutações
def perms(n, l = []):
    if n == 0:
        return [tuple()]
    else:
        nl = []
        for i in perms(n - 1, l):
            nl.append(i + (0,))
            nl.append(i + (1,))
        return nl

def a_gulosa(Q, s):
  if Q[s][0] > Q[s][1]:
    return 0
  elif Q[s][0] < Q[s][1]:
    return 1
  else:
    return random.choice((0, 1))

# Calculando a ação do agente
# pela política epsilon-gulosa
def escolha_epsilon_gulosa(epsilon):
    def f(Q, s):
        return a_gulosa(Q, s) if random.random() >= epsilon else \
            random.choice((0, 1))
    return f

# Calculando a ação do agente
# usando Gibbs
def escolha_gibbs(tau):
    def f(Q, s):
        e0 = exp(Q[s][0] / tau)
        e1 = exp(Q[s][1] / tau)
        return 0 if random.random() < e0 / (e0 + e1) else 1
    return f


# Executa o Q-Learning tentando prever o próximo elemento da sequência binária g
# Parâmetros:
#   g: sequência binária a ser prevista
#   k: memória
#   alfa: taxa de aprendizado
#   gama: desconto temporal
#   escolha: função de escolha (gulosa ou Gibbs)
#   vp: recompensa por um acerto
#   vn: punição por um erro
def qlearn(g, k, alfa, gama, escolha, vp, vn):
    # Gerando os estados
    S = perms(k)
    # Valor estimado das ações
    Q = {s: [0, 0] for s in S}
    # Estado inicial aleatório
    s = random.choice(S)
    
    # Armazenando as previsões do algoritmo
    resps = []
    for a_correta in g:
        # Calculando a ação do agente
        a = escolha(Q, s)
        resps.append(a)
    
        ## Modelo com correção
        #if a != a_correta:
        #  r = rec
        #  Q[(s, 1 - a)] += alfa * (r + gama * max((Q[(s, A[0])], Q[(s, A[1])])) - Q[(s, 1 - a)])
        #  r = 0
        #  Q[(s, a)] += alfa * (r + gama * max((Q[(s, A[0])], Q[(s, A[1])])) - Q[(s, a)])
        #else:
        #  r = rec
        #  Q[(s, a)] += alfa * (r + gama * max((Q[(s, A[0])], Q[(s, A[1])])) - Q[(s, a)])
        
        # recompensa
        r = vp if a == a_correta else vn
        
        # Atualizando Q
        m = max((Q[s][0], Q[s][1]))
        Q[s][a] += alfa * (r + gama * m - Q[s][a])
        # Atualização fictícia
        #r = vp if (1 - a) == a_correta else vn
        #Q[s][1 - a] += alfa * (r + gama * m - Q[s][1 - a])
        # próximo estado
        s = s if k == 0 else s[1:] + (a_correta,)
        assert s in S
    return resps

def qlearn_xy(g, k, alfa, gama, escolha, vp, vn):
    # Gerando os estados
    S = perms(2*k)
    # Valor estimado das ações
    Q = {s: [0, 0] for s in S}
    # Estado inicial aleatório
    s = random.choice(S)
    
    # Armazenando as previsões do algoritmo
    resps = []
    for a_correta in g:
        # Calculando a ação do agente
        a = escolha(Q, s)
        resps.append(a)
        # recompensa
        r = vp if a == a_correta else vn
        
        # Atualizando Q
        m = max((Q[s][0], Q[s][1]))
        Q[s][a] += alfa * (r + gama * m - Q[s][a])
        # próximo estado
        s = s if k == 0 else s[2:] + (a_correta, a)
        assert s in S
    return resps

if __name__ == '__main__':
    # Lendo os parâmetros da simulação
    config = configparser.ConfigParser()
    config.read(sys.argv[1:], encoding='utf8')    
    gama = float(config.get('parâmetros', 'gama', fallback=0.99))
    alfa = float(config.get('parâmetros', 'alfa', fallback=0.5))
    escolha = config.get('parâmetros', 'escolha', fallback='gibbs')
    if escolha == 'gulosa':
        epsilon = float(config.get('parâmetros', 'epsilon', fallback=0.05))
        fesc = escolha_epsilon_gulosa(epsilon)
    else:
        assert escolha == 'gibbs'
        tau = float(config.get('parâmetros', 'tau', fallback=1))
        fesc = escolha_gibbs(tau)
    k = int(config.get('parâmetros', 'k', fallback=0))
    vp = float(config.get('parâmetros', 'valor do acerto', fallback=1))
    vn = float(config.get('parâmetros', 'valor do erro', fallback=0))
    p = float(config.get('parâmetros', 'p', fallback=0.7))
    num_aps = int(config.get('parâmetros', 'número de apresentações', fallback=300))
    reps = int(config.get('parâmetros', 'repetições', fallback=10))
    analisar = int(config.get('parâmetros', 'analisar', fallback=0))
    
    resultados = []
    for rep in range(reps):
        g = tuple(1 if random.random() < p else 0 for i in range(num_aps))
        s = qlearn(g, k, alfa, gama, fesc, vp, vn)
        resultados.append((g, s))
    
    if analisar:
        # Análises
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        mpl.rcParams['axes.formatter.use_locale'] = True
        
        # Resposta média a cada apresentação
        y = np.array([mean([s[i] for g, s in resultados]) for i in range(num_aps)])
        error = np.array([stdev([s[i] for g, s in resultados]) for i in range(num_aps)])
        x = np.arange(num_aps)
        plt.plot(x, y, 'k-')
        plt.xlabel("Apresentação")
        plt.ylabel("Resposta Média")
        plt.ylim(0, 1)
        plt.fill_between(x, y-error, y+error, color=[(1.0, 0, 0, 0.1)])
        plt.savefig('resp_media.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Histograma da resposta média nas últimas 100 apresentações
        x = [mean(s[-100:]) for g, s in resultados]
        plt.xlabel("Resposta Média")
        plt.ylabel("Frequência")
        plt.xlim(0, 1)
        plt.hist(x, np.linspace(0, 1, 10), normed=True)
        plt.savefig('hist.png', dpi=300, bbox_inches='tight')
        plt.close()
    else:
        pass # Salvar dados em um arquivo?