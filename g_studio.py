import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy import optimize
from modulo_rw import rw_accelerazione
from modulo_rw import rw_riflessione
from modulo_rw import rw_origine
import pandas as pd

def spettro(E, a, K, B):
    return K*E**(-a) + B
n_iter=10
nP = 200
N = 120
step0 = 1.1
x0 = 1

graf=input('Visualizzare i grafici delle {:} simulazioni per la prima configurazione?? (2 x {:}) \ny/n: '.format(n_iter, n_iter))



#CONFIGURAZIONE 1
a_arr=np.empty(0)
E_arr=np.empty(0)
chir_arr=np.empty(0)
g_arr=np.empty(0)

print('PRIMA CONFIGURAZIONE: ACCELERAZIONE ATTRAVERSO ORGINE\n')
g1=np.linspace(1.01, 1.2, n_iter)
for i in range(n_iter):
    g=g1[i]
    zero = np.zeros(N)
    passi = np.linspace(0, N, N)
    E_fin3 = np.empty(0)

    fig, ax = plt.subplots(figsize=(11, 8))
    plt.plot(zero, color='gray')
    for i in range(nP):
        (path, step) = rw_origine(step0, N, x0, g)
        plt.plot(path, marker='+', alpha=0.4)
        E_fin3 = np.append(E_fin3, step)  # riempo un array con le energie finali delle particelle
    plt.grid()
    plt.xlabel('passi')
    plt.ylabel(r'$\Delta x$')
    if(graf=='y'):
        plt.show()
    else:
        plt.close()
        
    # STUDIO DISTRIBUZIONE DEL PASSO FINALE di ciascuna delle configurazioni al variare dei parametri
    E_fin3 = abs(E_fin3)
    E_fin3.sort()

    n3, bins3 = np.histogram(E_fin3, bins=int(np.sqrt(nP)))
    bincenters3 = (bins3[:-1] + bins3[1:]) / 2  # centro di ciascun bin

    valid3 = n3 > 0
    bincenters3 = bincenters3[valid3]
    n3 = n3[valid3]

    par3, pcov3 = optimize.curve_fit(
        spettro, 
        xdata=bincenters3, 
        ydata=n3, 
        sigma=np.sqrt(n3),  
        p0=[2, 150, 0], 
        absolute_sigma=True, 
        maxfev=50000
    )
    yfit3 = spettro(bincenters3, par3[0], par3[1], par3[2])

    print('\na={:} +- {:}'.format(np.around(par3[0], 3), np.around(np.sqrt(pcov3.diagonal()[0]), 3)))
    #print('K={:} +- {:}'.format(np.around(par3[1], 3), np.around(np.sqrt(pcov3.diagonal()[1]), 3)))
   # print('B={:} +- {:}'.format(np.around(par3[2], 3), np.around(np.sqrt(pcov3.diagonal()[2]), 3)))

    chi = np.sum(((yfit3 - n3) / np.sqrt(n3)) ** 2)
    chir = chi / (len(bincenters3) - 3)
    #print('Chi2: ', chi)
    print('Chi2 ridotto: ', np.around(chir, 3))
    print('Energia più alta raggiunta: ', np.around(E_fin3[len(E_fin3)-1], 3))

    a_arr=np.append(a_arr, par3[0])
    g_arr=np.append(g_arr, g)
    E_arr=np.append(E_arr, E_fin3[len(E_fin3)-1])
    chir_arr=np.append(chir_arr, chir)
    
    if graf=='y':
        fig, ax = plt.subplots(1, 2, figsize=(10, 8))
        n, bins, p = ax[0].hist(E_fin3, bins=int(np.sqrt(nP)), color='teal', alpha=0.7)
        ax[0].plot(bincenters3, yfit3, color='tomato', label='fit')
        ax[0].set_xlabel('Energia finale', fontsize=16)
        ax[0].legend()
        n, bins, p = ax[1].hist(E_fin3, bins=int(np.sqrt(nP)), color='teal', alpha=0.7)
        ax[1].plot(bincenters3, yfit3, color='tomato', label='fit')
        ax[1].legend()
        ax[1].set_xlabel('Energia finale (log)', fontsize=16)
        ax[1].set_xscale('log')
        ax[1].set_yscale('log')
        plt.show()


print('\n')
g_arr = np.around(g_arr, 3)
E_arr = np.around(E_arr, 3)
a_arr = np.around(a_arr, 3)
chir_arr = np.around(chir_arr, 3)


print(f"{'g':<10}{'E finali':<15}{'a':<10}{'Chi2 ridotti':<10}")
print("-" * 45)
for g, E, a, chir in zip(g_arr, E_arr, a_arr, chir_arr):
    print(f"{g:<10}{E:<15}{a:<10}{chir:<10}")
    
g_fin=np.empty(0)
for i in range(len(chir_arr)):
    if chir_arr[i]<1.3 and chir_arr[i]>0.6:
        g_fin=np.append(g_fin, g_arr[i])
if len(g_fin)>0:
    print('\nValori accettabili per g:\n ')

    for i in range(len(g_fin)):
        print("{:}\n".format(np.around(g_fin[i], 3)))
    
    print("\n\nConsiderando una configurazione di {:} particelle che compiono {:} passi, si può dedurre dalle {:} simulazioni appena svolte che i valori iniziali migliori (con Chi2 ridotto <1.3 e >0.6) dell'incremento del passo si collocano in un intorno di ({:} < g < {:}).\n".format(nP, N, n_iter, np.around(g_fin.min(), 2), np.around(g_fin.max(), 2)))
else:
    print('\n\nNon sono stati trovati valori accettabili per g in questa configurazione\n')
        
print("-" * 100)

graf=input('Visualizzare i grafici delle {:} simulazioni per la seconda configurazione? (2 x {:}) \ny/n: '.format(n_iter, n_iter))

print("-" * 100)

#CONFIGURAZIONE 2: RIFLESSIONE E ACCELERAZIONE ATTRAVERSO ORIGINE, RIFLESSIONE SU BARRIERA X_MAX
a_arr=np.empty(0)
E_arr=np.empty(0)
chir_arr=np.empty(0)
g1=np.linspace(1.01, 1.15, n_iter)
g_arr=np.empty(0)
print("-" * 100)

print('\nCONFIGURAZIONE 2: RIFLESSIONE E ACCELERAZIONE ATTRAVERSO ORIGINE, RIFLESSIONE SU BARRIERA X_MAX\n')
for i in range(n_iter):
    xmax = 30
    b = xmax/(2*N)
    g=g1[i]
    zero = np.zeros(N)
    E_fin3 = np.empty(0)

    fig, ax = plt.subplots(figsize=(11, 8))
    plt.plot(zero, color='gray')
    for i in range(nP):
        (path, mas, step) = rw_riflessione(step0, N, x0, g, xmax, b)
        plt.plot(path, marker='+', alpha=0.4)
        E_fin3 = np.append(E_fin3, step)  # riempo un array con le energie finali delle particelle
    plt.plot(mas, color='tomato', label='xmax')
    plt.grid()
    plt.legend()
    plt.xlabel('passi')
    plt.ylabel(r'$\Delta x$')
    if graf=='y':
        plt.show()
    else:
        plt.close(fig)

    # STUDIO DISTRIBUZIONE DEL PASSO FINALE di ciascuna delle configurazioni al variare dei parametri
    E_fin3 = abs(E_fin3)
    E_fin3.sort()

    n3, bins3= np.histogram(E_fin3, bins=int(np.sqrt(nP)))
    bincenters3 = (bins3[:-1] + bins3[1:]) / 2  # centro di ciascun bin

    valid3 = n3 > 0
    bincenters3 = bincenters3[valid3]
    n3 = n3[valid3]

    par3, pcov3 = optimize.curve_fit(
        spettro, 
        xdata=bincenters3, 
        ydata=n3, 
        sigma=np.sqrt(n3),  
        p0=[2, 150, 0], 
        absolute_sigma=True, 
        maxfev=50000
    )
    yfit3 = spettro(bincenters3, par3[0], par3[1], par3[2])

    print('\na={:} +- {:}'.format(np.around(par3[0], 3), np.around(np.sqrt(pcov3.diagonal()[0]), 3)))
    #print('K={:} +- {:}'.format(np.around(par3[1], 3), np.around(np.sqrt(pcov3.diagonal()[1]), 3)))
   # print('B={:} +- {:}'.format(np.around(par3[2], 3), np.around(np.sqrt(pcov3.diagonal()[2]), 3)))

    chi = np.sum(((yfit3 - n3) / np.sqrt(n3)) ** 2)
    chir = chi / (len(bincenters3) - 3)
    #print('Chi2: ', chi)
    print('Chi2 ridotto: ', np.around(chir, 3))
    print('Energia più alta raggiunta: ', np.around(E_fin3[len(E_fin3)-1], 3))

    a_arr=np.append(a_arr, par3[0])
    g_arr=np.append(g_arr, g)
    E_arr=np.append(E_arr, E_fin3[len(E_fin3)-1])
    chir_arr=np.append(chir_arr, chir)

    if graf=='y':
        fig, ax = plt.subplots(1, 2, figsize=(10, 8))
        n, bins, p = ax[0].hist(E_fin3, bins=int(np.sqrt(nP)), color='teal', alpha=0.7)
        ax[0].plot(bincenters3, yfit3, color='tomato', label='fit')
        ax[0].set_xlabel('Energia finale', fontsize=16)
        ax[0].legend()
        n, bins, p = ax[1].hist(E_fin3, bins=int(np.sqrt(nP)), color='teal', alpha=0.7)
        ax[1].plot(bincenters3, yfit3, color='tomato', label='fit')
        ax[1].legend()
        ax[1].set_xlabel('Energia finale (log)', fontsize=16)
        ax[1].set_xscale('log')
        ax[1].set_yscale('log')
        plt.show()


print('\n')
g_arr = np.around(g_arr, 3)
E_arr = np.around(E_arr, 3)
a_arr = np.around(a_arr, 3)
chir_arr = np.around(chir_arr, 3)

print(f"{'g':<10}{'E finali':<15}{'a':<10}{'chi ridotti':<10}")
print("-" * 45)
for g, E, a, chir in zip(g_arr, E_arr, a_arr, chir_arr):
    print(f"{g:<10}{E:<15}{a:<10}{chir:<10}")

g_fin=np.empty(0)
for i in range(len(chir_arr)):
    if chir_arr[i]<1.3 and chir_arr[i]>0.6:
        g_fin=np.append(g_fin, g_arr[i])

if len(g_fin)>0:
    print('\nValori accettabili per g:\n ')

    for i in range(len(g_fin)):
        print("{:}\n".format(np.around(g_fin[i], 3)))
    
    print("\n\nConsiderando una configurazione di {:} particelle che compiono {:} passi, si può dedurre dalle {:} simulazioni appena svolte che i valori iniziali migliori (con Chi2 ridotto <1.3 e >0.6) dell'incremento del passo si collocano in un intorno di ({:} < g < {:}).\n".format(nP, N, n_iter, np.around(g_fin.min(), 2), np.around(g_fin.max(), 2)))

else:
    print('\n\nNon sono stati troavti valori accettabili di g in questa simulazione\n')
print("-" * 100)

graf=input('Visualizzare i grafici delle {:} simulazioni per la terza configurazione? (2 x {:}) \ny/n: '.format(n_iter, n_iter))

print("-" * 100)

#CONFIGURAZIONE 3
a_arr=np.empty(0)
E_arr=np.empty(0)
chir_arr=np.empty(0)
g1=np.linspace(1.01, 1.15, n_iter) #più di 1.15 non mi trova i paramteri
g_arr=np.empty(0)

print("-" * 100)
N=120
print('\nCONFIGURAZIONE3: RIFLESSIONE E ACCELERAZIONE SU ORIGINE E BARRIERA X_MAX\n')
for i in range(n_iter):
    xmax = 30
    b = xmax/(2*N)
    g=g1[i]
    zero = np.zeros(N)
    E_fin3 = np.empty(0)

    fig, ax = plt.subplots(figsize=(11, 8))
    plt.plot(zero, color='gray')
    for i in range(nP):
        (path, mas, step) = rw_accelerazione(step0, N, x0, g, xmax, b)
        plt.plot(path, marker='+', alpha=0.4)
        E_fin3 = np.append(E_fin3, step)  # riempo un array con le energie finali delle particelle
    plt.plot(mas, color='tomato', label='xmax')
    plt.grid()
    plt.legend()
    plt.xlabel('passi')
    plt.ylabel(r'$\Delta x$')
    if graf=='y':
        plt.show()
    else:
        plt.close(fig)

    # STUDIO DISTRIBUZIONE DEL PASSO FINALE di ciascuna delle configurazioni al variare dei parametri
    E_fin3 = abs(E_fin3)
    E_fin3.sort()

    n3, bins3= np.histogram(E_fin3, bins=int(np.sqrt(nP)))
    bincenters3 = (bins3[:-1] + bins3[1:]) / 2  # centro di ciascun bin

    valid3 = n3 > 0
    bincenters3 = bincenters3[valid3]
    n3 = n3[valid3]

    par3, pcov3 = optimize.curve_fit(
        spettro, 
        xdata=bincenters3, 
        ydata=n3, 
        sigma=np.sqrt(n3),  
        p0=[2, 150, 0], 
        absolute_sigma=True, 
        maxfev=50000
    )
    yfit3 = spettro(bincenters3, par3[0], par3[1], par3[2])

    print('\na={:} +- {:}'.format(np.around(par3[0], 3), np.around(np.sqrt(pcov3.diagonal()[0]), 3)))
    #print('K={:} +- {:}'.format(np.around(par3[1], 3), np.around(np.sqrt(pcov3.diagonal()[1]), 3)))
   # print('B={:} +- {:}'.format(np.around(par3[2], 3), np.around(np.sqrt(pcov3.diagonal()[2]), 3)))

    chi = np.sum(((yfit3 - n3) / np.sqrt(n3)) ** 2)
    chir = chi / (len(bincenters3) - 3)
    #print('Chi2: ', chi)
    print('Chi2 ridotto: ', np.around(chir, 3))
    print('Energia più alta raggiunta: ', np.around(E_fin3[len(E_fin3)-1], 3))

    a_arr=np.append(a_arr, par3[0])
    g_arr=np.append(g_arr, g)
    E_arr=np.append(E_arr, E_fin3[len(E_fin3)-1])
    chir_arr=np.append(chir_arr, chir)

    if graf=='y':
        fig, ax = plt.subplots(1, 2, figsize=(10, 8))
        n, bins, p = ax[0].hist(E_fin3, bins=int(np.sqrt(nP)), color='teal', alpha=0.7)
        ax[0].plot(bincenters3, yfit3, color='tomato', label='fit')
        ax[0].set_xlabel('Energia finale', fontsize=16)
        ax[0].legend()
        n, bins, p = ax[1].hist(E_fin3, bins=int(np.sqrt(nP)), color='teal', alpha=0.7)
        ax[1].plot(bincenters3, yfit3, color='tomato', label='fit')
        ax[1].legend()
        ax[1].set_xlabel('Energia finale (log)', fontsize=16)
        ax[1].set_xscale('log')
        ax[1].set_yscale('log')
        plt.show()

print('\n')
g_arr = np.around(g_arr, 3)
E_arr = np.around(E_arr, 3)
a_arr = np.around(a_arr, 3)
chir_arr = np.around(chir_arr, 3)


print(f"{'g':<10}{'E finali':<15}{'a':<10}{'chi ridotti':<10}")
print("-" * 45)
for g, E, a, chir in zip(g_arr, E_arr, a_arr, chir_arr):
    print(f"{g:<10}{E:<15}{a:<10}{chir:<10}")

g_fin=np.empty(0)
for i in range(len(chir_arr)):
    if chir_arr[i]<1.3 and chir_arr[i]>0.6:
        g_fin=np.append(g_fin, g_arr[i])
if len(g_fin)>0:
    print('\nValori accettabili per g:\n ')

    for i in range(len(g_fin)):
        print("{:}\n".format(np.around(g_fin[i], 3)))
    
    print("\n\nConsiderando una configurazione di {:} particelle che compiono {:} passi, si può dedurre dalle {:} simulazioni appena svolte che i valori iniziali migliori (con Chi2 ridotto <1.3 e >0.6) dell'incremento del passo si collocano in un intorno di ({:} < g < {:}.\n".format(nP, N, n_iter, np.around(g_fin.min(), 2), np.around(g_fin.max(), 2)))
else:
    print('\n\nNon sono stati trovati valori accettabili per g in questa configurazione\n')

print("-" * 100)


