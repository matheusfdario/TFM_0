#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
#import matplotlib.pyplot as plt
#import scipy.io
import math



dados = np.load('/home/matheusfdario/Documentos/LASSIP/rep/TFM_0/dados_tfm.npy', allow_pickle=True).item()
g_ascans = dados.get('ascans')                                  # g: matriz ascans: 1854x64x64 (matriz)
cl_speed_m_s = dados.get('speed_m_s')                           # c: velocidade de deslocamento do som no meio em micro segundos (escalar)
f_sampling_MHz = dados.get('f_sampling_MHz')                    # f: frequência de amostragem em MHz (escalar) -> p/ período de amostragem: T = 1/f
T_period_sampling_microsec = 1/f_sampling_MHz                   # T: Período de amostragem - Cálculo do período de amostragem
samples_t0_init_microsec = dados.get('samples_t_init_microsec') # t0: intante inicial em micro segundos (escalar)
xt_elem_pos_mm = dados.get('elem_positions_mm')                  # xt: posições dos emissores? #? equivalente ao x no saft?
z_pos_vec = []                                                  # z: Conversão para posição /2->ida e volta - Cálculo da posição em termos de tempo e velocidade que o som se propaga no meio analizaso
for i in range(len(g_ascans)):
    time = samples_t0_init_microsec+(1/f_sampling_MHz)*i
    z_pos = (cl_speed_m_s*time)/2
    z_pos_vec.append(z_pos)

#? preciso gerar um vetor t usando samples_t_init_microsec e f_sampling_MHz? 
#?  e usar ele para gerar um vetor z com t e speed_m_s?
#? como delimitar o ROI?


print(len(z),len(ascans))


#Função TMF
def tfm(g, x, z, cl, T):
    N = len(x)
    Nz = len(z)
    f = np.zeros((Nz, N))

    for i in range(N):              #?  relacionada com o nũmero de amostras?
        for j in range(Nz):         #? relacionado com 1 64 da matriz
            for n in range(N):      #? relacionado com o outro 64 da matriz?
                for k in range(?):  #? relacio com elem_positions_mm?
                    tau = (np.sqrt((xt[k] - x[i]) ** 2 + z[j] ** 2)+ np.sqrt((xt[n] - x[i]) ** 2 + z[j] ** 2)) / cl  # Cálculo do atraso (tau) para cada par de transdutores e posição
                    tau_idx = int(np.round(tau / T))  # Conversão do atraso (tau) para índice do array de amostras
                    tau_idx = tau_idx-pi  # Correção do índice do array de amostras para excluir amostras iniciais (pi)
                    if(tau_idx<399):  # Verificação para evitar índices fora do intervalo do array de amostras g
                        f[j, i] += g[tau_idx,n]  # Acumulação do valor de amostra corrigido no resultado final da SAFT
    return f

# Plotagem do B-Scan e do resultado da SAFT
plt.figure()
plt.imshow(g_ascans, aspect="auto")  # Plotagem da imagem do B-Scan
plt.title('B-Scan - Matheus Fortunato Dário')
plt.figure()
#f = saft(g, x, z, cl, T)  # Chamada da função SAFT para processamento dos dados
plt.imshow(f, aspect="auto")  # Plotagem da imagem resultante da SAFT
plt.title('SAFT - Matheus Fortunato Dário')
plt.show()  # Exibição dos gráficos plotados