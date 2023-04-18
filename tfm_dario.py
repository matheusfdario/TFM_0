import numpy as np
dados = np.load('/home/matheusfdario/Documentos/LASSIP/rep/TFM_0/dados_tfm.npy', allow_pickle=True).item()
ascans = dados.get('ascans')
speed_m_s = dados.get('speed_m_s')
f_sampling_MHz = dados.get('f_sampling_MHz')
samples_t_init_microsec = dados.get('samples_t_init_microsec')
elem_positions_mm = dados.get('elem_positions_mm')