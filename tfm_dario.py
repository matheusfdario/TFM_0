#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import math



dados = np.load('/home/matheusfdario/Documentos/LASSIP/rep/TFM_0/dados_tfm.npy', allow_pickle=True).item()
g_ascans = dados.get('ascans')                                  # g: matriz ascans: 1854x64x64 (matriz)
cl_speed_m_s = dados.get('speed_m_s')                           # c': velocidade de deslocamento do som no meio em m/s (escalar)
f_sampling_MHz = dados.get('f_sampling_MHz')                    # f': frequência de amostragem em MHz (escalar) -> p/ período de amostragem: T = 1/f
samples_t0_init_microsec = dados.get('samples_t_init_microsec') # t0': intante inicial em micro segundos (escalar)
xt_elem_pos_mm = dados.get('elem_positions_mm')                 # xt: posições dos emissores? #? equivalente ao x no saft?
cl_speed_s = cl_speed_m_s*1e3                                   # c: velocidade de deslocamento do som no meio em mm/s (escalar)
f_sampling_Hz = f_sampling_MHz*1e6                              # f: frequência de amostragem em Hz (escalar) -> p/ período de amostragem: T = 1/f
T_period_sampling_s = 1/f_sampling_Hz                           # T: Período de amostragem - Cálculo do período de amostragem em segundos
samples_t0_init_s = samples_t0_init_microsec*1e-6               # t0: intante inicial em segundos (escalar)

# x_roi = np.linspace(-20,40,64)                                  #? Desnecessário?
z_roi = np.linspace(10,30,500)                                 # z: Conversão para posição /2->ida e volta - Cálculo da posição em termos de tempo e velocidade que o som se propaga no meio analizado
g_sfat = g_ascans.diagonal(0,1,2)

# Função SAFT
def saft(g, x, z, cl, T):
    N = len(x)
    Nz = len(z)
    f = np.zeros((Nz, N))
    xt = x
    for i,xi in enumerate(x):
        for j,zj in enumerate(z):
            for n in range(N):        
                tau = ((2 * np.sqrt((xt[n] - xi) ** 2 + zj ** 2)) / cl)-samples_t0_init_s  # Cálculo do atraso (tau) para cada par de transdutores e posição
                tau_idx = int(np.round(tau / T))  # Conversão do atraso (tau) para índice do array de amostras
                if(tau_idx<=Nz):  # Verificação para evitar índices fora do intervalo do array de amostras g
                    f[j, i] += g[tau_idx,n]  # Acumulação do valor de amostra corrigido no resultado final da SAFT
    return f

# Função TFM

def tfm(g, x, z, cl, T):
    N = len(x)
    Nz = len(z)
    f = np.zeros((Nz, N))
    xt = x
    for i,xi in enumerate(x):
        for j,zj in enumerate(z):
            for n,xtn in enumerate(xt):
                for k,xtk in enumerate(xt):        
                    tau = ((np.sqrt((xtk - xi) ** 2 + zj ** 2) + np.sqrt((xtn - xi) ** 2 + zj ** 2)) / cl)-samples_t0_init_s  # Cálculo do atraso (tau) para cada par de transdutores e posição
                    tau_idx = int(np.round(tau / T))  # Conversão do atraso (tau) para índice do array de amostras
                    if(tau_idx<=Nz):  # Verificação para evitar índices fora do intervalo do array de amostras g
                        f[j, i] += g[tau_idx,n,k]  # Acumulação do valor de amostra corrigido no resultado final da SAFT
    return f

# Plotagem do B-Scan e do resultado da SAFT
plt.figure()
plt.imshow(g_sfat, aspect="auto")  # Plotagem da imagem do B-Scan
plt.title('B-Scan - Matheus Fortunato Dário')
plt.figure()
f = saft(g_sfat, xt_elem_pos_mm, z_roi, cl_speed_s, T_period_sampling_s)  # Chamada da função SAFT para processamento dos dados
plt.imshow(f, aspect="auto")  # Plotagem da imagem resultante da SAFT
plt.title('SAFT - Matheus Fortunato Dário')
e = tfm(g_ascans, xt_elem_pos_mm, z_roi, cl_speed_s, T_period_sampling_s)  # Chamada da função TFM para processamento dos dados
plt.imshow(e, aspect="auto")  # Plotagem da imagem resultante da SAFT
plt.title('TFM - Matheus Fortunato Dário')
plt.show()  # Exibição dos gráficos plotados

#mashgrid np