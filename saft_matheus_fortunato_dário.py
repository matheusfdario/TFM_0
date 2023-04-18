#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import math

file = "DadosEnsaio.mat"    # Atribuindo variável com o nome do arquivo de dados disponibilizado

mat = scipy.io.loadmat(file)

# Definindo parâmetros
pi = 500  # Amostra inicial do A-Scan
pf = 900  # Amostra final do A-Scan
zmax = 0 
g = mat["ptAco40dB_1"]["AscanValues"][0][0][pi:pf]  # B-Scan - Extração dos dados do arquivo .mat (matriz) disponibilizado
cl = mat["ptAco40dB_1"]["CscanData"][0][0]["Cl"][0][0][0][0]  # Velocidade - Extração da velocidade do arquivo .mat
t = mat["ptAco40dB_1"]["timeScale"][0][0][pi:pf]*1e-6  # Tempo - Extração do tempo do arquivo .mat 
T = t[1][0]-t[0][0]  # Período de amostragem - Cálculo do período de amostragem
z = cl*t/2  # Conversão para posição /2->ida e volta - Cálculo da posição em termos de tempo e velocidade que o som se propaga no meio analizaso
x = mat["ptAco40dB_1"]["CscanData"][0][0]["X"][0][0]*1e-3  # Posições do transdutor - Extração das posições dos transdutores do arquivo .mat

# Função SAFT
def saft(g, x, z, cl, T):
    N = len(x)
    Nz = len(z)
    f = np.zeros((Nz, N))

    for i in range(N):
        for j in range(Nz):
            for n in range(N):
                tau = (2 * np.sqrt((x[n] - x[i]) ** 2 + z[j] ** 2)) / cl  # Cálculo do atraso (tau) para cada par de transdutores e posição
                tau_idx = int(np.round(tau / T))  # Conversão do atraso (tau) para índice do array de amostras
                tau_idx = tau_idx-pi  # Correção do índice do array de amostras para excluir amostras iniciais (pi)
                if(tau_idx<399):  # Verificação para evitar índices fora do intervalo do array de amostras g
                    f[j, i] += g[tau_idx,n]  # Acumulação do valor de amostra corrigido no resultado final da SAFT
    return f

# Plotagem do B-Scan e do resultado da SAFT
plt.figure()
plt.imshow(g, aspect="auto")  # Plotagem da imagem do B-Scan
plt.title('B-Scan - Matheus Fortunato Dário')
plt.figure()
f = saft(g, x, z, cl, T)  # Chamada da função SAFT para processamento dos dados
plt.imshow(f, aspect="auto")  # Plotagem da imagem resultante da SAFT
plt.title('SAFT - Matheus Fortunato Dário')
plt.show()  # Exibição dos gráficos plotados
