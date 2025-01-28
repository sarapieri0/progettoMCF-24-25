import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy import optimize
from modulo_rw import rw_origine
from modulo_rw import rw_riflessione
from modulo_rw import rw_accelerazione
import modulo_rw

def spettro(E, a, K, B):
    return K*E**(-a) + B

conf=int(input('Configurazioni da studiare:\n1: accelerazione attraverso origine\n2: riflessione attraverso origine e barriera xmax, accelerazione su origine\n3: accelerazione e riflessione su origine e barriera xmax\n Selezionare (1,2,3): '))
print('*' * 100)

if conf == 1:
    print("\nParametri da inserire: numero di particelle, g, numero di passi, posizione iniziale.")
    print('\nValori funzionali per 200 particelle e 120 passi:\n- 1.04 < g < 1.15\n- -11 < x0 < 12')
    nP = int(input('\nInserire il numero di particelle per lo studio: '))
    N = int(input('Inserire il numero di passi: '))
    g=float(input('Inserire g: '))
    x0 = float(input('Inserire la posizione iniziale delle particelle: '))

    step0 = 1.1 #altrimenti il random walk non parte, perché le particelle non oltrepassano l'origine, per come è definito l'avanzamento
    
    zero = np.zeros(N)
    E_fin1 = np.empty(0)

    fig, ax = plt.subplots(figsize=(11, 8))
    plt.title('Configurazione 1: accelerazione su origine')
    plt.plot(zero, color='gray')
    for i in range(nP):
        (path, step) = rw_origine(step0, N, x0, g)
        E_fin1 = np.append(E_fin1, step)
        plt.plot(path, marker='+', alpha=0.3)
    plt.xlabel('passi')
    plt.ylabel(r'$\Delta x$')
    plt.show()

    # STUDIO DISTRIBUZIONE DEL PASSO FINALE

    E_fin1 = abs(E_fin1)
    E_fin1.sort()

    n1, bins1 = np.histogram(E_fin1, bins=int(np.sqrt(nP)))
    bincenters1 = (bins1[:-1] + bins1[1:]) / 2

    valid1 = n1 > 0
    bincenters1 = bincenters1[valid1]
    n1 = n1[valid1]
    
    par1, pcov1 = optimize.curve_fit(spettro, xdata=bincenters1, ydata=n1, sigma=np.sqrt(n1), p0=[2, 150, 0], absolute_sigma=True, maxfev=50000)
    yfit1 = spettro(bincenters1, par1[0], par1[1], par1[2])

    print('\na={:} +- {:}'.format(np.around(par1[0], 3), np.around(np.sqrt(pcov1.diagonal()[0]),3)))
    print('K={:} +- {:}'.format(np.around(par1[1], 3), np.around(np.sqrt(pcov1.diagonal()[1]),3)))
    print('B={:} +- {:}'.format(np.around(par1[2], 3), np.around(np.sqrt(pcov1.diagonal()[2]),3)))

    chi = np.sum(((yfit1 - n1) / np.sqrt(n1)) ** 2)
    chir = chi / (len(bincenters1) - 3)
    #print('Chi2: ', chi)
    print('Chi2 ridotto: ', np.around(chir, 3))
    print('Energia finale massima raggiunta: ',  np.around(E_fin1[len(E_fin1)-1], 3))

    fig, ax = plt.subplots(1, 2, figsize=(10, 8))
    n, bins, p = ax[0].hist(E_fin1, bins=int(np.sqrt(nP)), color='teal', alpha=0.7)
    ax[0].plot(bincenters1, yfit1, color='tomato', label='fit')
    ax[0].set_xlabel('Energia finale', fontsize=16)
    ax[0].legend()
    n, bins, p = ax[1].hist(E_fin1, bins=int(np.sqrt(nP)), color='teal', alpha=0.7)
    ax[1].plot(bincenters1, yfit1, color='tomato', label='fit')
    ax[1].legend()
    ax[1].set_xlabel('Energia finale (log)', fontsize=16)
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')
    plt.show()

    if chir>0.5 and chir<1.4:
        print("\nLa simulazione è rappresentativa della legge di potenza studiata.")
    else:
        print("\nLa simulazione non è rappresentativa della legge di potenza studiata.\nA tal fine è necessario inserire parametri diversi.")

elif conf == 2:
    print("\nParametri da inserire: numero di particelle, numero di passi, g, valore iniziale della barriera xmax, x0.")
    print("\nValori funzionali per 200 particelle e 120 passi:\n- 1.06 < g < 1.13 \n- 10 < xmax < 40 (La retta descresce con un valore di xmax/2*N_passi) \n- 1 < x0 < 15 ")
    nP = int(input('\nInserire il numero di particelle per lo studio: '))
    N = int(input('Inserire il numero di passi che ciascuna particella deve compiere nella traiettoria: '))
    g=float(input('Inserire g: '))
    xmax = int(input('Inserire altezza iniziale della barriera: '))
    x0=float(input('Inserire la posizione iniziale delle particelle: '))
    b = xmax/(N*2)
    step0 = 1.1
    
    zero = np.zeros(N)
    passi = np.linspace(0, N, N)
    E_fin2 = np.empty(0)

    fig, ax = plt.subplots(figsize=(11, 8))
    plt.title('Configurazione 2: accelerazione e riflessione su origine, riflessione su xmax')
    plt.plot(zero, color='gray')
    for i in range(nP):
        (path, mas, step) = rw_riflessione(step0, N, x0, g, xmax, b)
        plt.plot(path, marker='+', alpha=0.3)
        E_fin2 = np.append(E_fin2, step)  # riempo un array con le energie finali delle particelle
    plt.plot(mas, color='tomato', label='xmax')
    plt.grid()
    plt.xlabel('passi')
    plt.ylabel(r'$\Delta x$')
    plt.show()

    # STUDIO DISTRIBUZIONE DEL PASSO FINALE
    E_fin2 = abs(E_fin2)
    E_fin2.sort()

    n2, bins2= np.histogram(E_fin2, bins=int(np.sqrt(nP)))
    bincenters2 = (bins2[:-1] + bins2[1:]) / 2  # centro di ciascun bin

    valid = n2 > 0
    bincenters2 = bincenters2[valid]
    n2 = n2[valid]
 
    par2, pcov2 = optimize.curve_fit(
        spettro,
        xdata=bincenters2,
        ydata=n2,
        sigma=np.sqrt(n2),
        p0=[2, 150, 0],
        absolute_sigma=True,
        maxfev=50000
    )
    yfit2 = spettro(bincenters2, par2[0], par2[1], par2[2])

    print('\na={:} +- {:}'.format(np.around(par2[0],3), np.around(np.sqrt(pcov2.diagonal()[0]),3)))
    print('K={:} +- {:}'.format(np.around(par2[1],3), np.around(np.sqrt(pcov2.diagonal()[1]),3)))
    print('B={:} +- {:}'.format(np.around(par2[2],3), np.around(np.sqrt(pcov2.diagonal()[2]),3)))

    chi = np.sum(((yfit2 - n2) / np.sqrt(n2))**2)
    chir = chi / (len(bincenters2) - 3)
    #print('Chi2: ', chi)
    print('Chi2 ridotto: ', np.around(chir, 3))
    print('Energia finale massima: ', np.around(E_fin2[len(E_fin2)-1], 3))


    fig, ax = plt.subplots(1, 2, figsize=(10, 8))
    n, bins, p = ax[0].hist(E_fin3, bins=int(np.sqrt(nP)), color='teal', alpha=0.7)
    ax[0].plot(bincenters3, yfit2, color='tomato', label='fit')
    ax[0].set_xlabel('Energia finale', fontsize=16)
    ax[0].legend()
    n, bins, p = ax[1].hist(E_fin2, bins=int(np.sqrt(nP)), color='teal', alpha=0.7)
    ax[1].plot(bincenters2, yfit2, color='tomato', label='fit')
    ax[1].legend()
    ax[1].set_xlabel('Energia finale (log)', fontsize=16)
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')
    plt.show()

    if chir>0.5 and chir<1.4:
        print("\nLa simulazione è rappresentativa della legge di potenza studiata.")
    else:
        print("\nLa simulazione non è rappresentativa della legge di potenza studiata.\nA tal fine è necessario inserire parametri migliori.")

elif conf == 3:
    print("\nParametri da inserire: numero di particelle, numero di passi, g, valore iniziale della barriera xmax, x0.")
    print("\nValori funzionali per 200 particelle e 120 passi:\n- 1.04 < g < 1.13 \n- 14 < xmax < 50 (La retta descresce con un valore di xmax/2*N_passi) \n- 1 < x0 < 22")
    nP = int(input('\nInserire il numero di particelle per lo studio: '))
    N = int(input('Inserire il numero di passi che ciascuna particella deve compiere nella traiettoria: '))
    g=float(input('Inserire g: '))
    xmax = int(input('Inserire altezza iniziale della barriera: '))
    x0=float(input('Inserire la posizione iniziale delle particelle: '))
    b = xmax/(N*2)
    step0 = 1.1
    
    zero = np.zeros(N)
    passi = np.linspace(0, N, N)
    E_fin3 = np.empty(0)

    fig, ax = plt.subplots(figsize=(11, 8))
    plt.title('Configurazione 3: accelerazione e riflessione su origine e su xmax')
    plt.plot(zero, color='gray')
    for i in range(nP):
        (path, mas, step) = rw_accelerazione(step0, N, x0, g, xmax, b)
        plt.plot(path, marker='+', alpha=0.3)
        E_fin3 = np.append(E_fin3, step)  # riempo un array con le energie finali delle particelle
    plt.plot(mas, color='tomato', label='xmax')
    plt.grid()
    plt.xlabel('passi')
    plt.ylabel(r'$\Delta x$')
    plt.show()

    # STUDIO DISTRIBUZIONE DEL PASSO FINALE
    E_fin3 = abs(E_fin3)
    E_fin3.sort()

    n3, bins3= np.histogram(E_fin3, bins=int(np.sqrt(nP)))
    bincenters3 = (bins3[:-1] + bins3[1:]) / 2  # centro di ciascun bin

    valid = n3 > 0
    bincenters3=bincenters3[valid]
    n3=n3[valid]
 
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

    print('\na={:} +- {:}'.format(np.around(par3[0],3), np.around(np.sqrt(pcov3.diagonal()[0]),3)))
    print('K={:} +- {:}'.format(np.around(par3[1],3), np.around(np.sqrt(pcov3.diagonal()[1]),3)))
    print('B={:} +- {:}'.format(np.around(par3[2],3), np.around(np.sqrt(pcov3.diagonal()[2]),3)))

    chi = np.sum(((yfit3 - n3) / np.sqrt(n3))**2)
    chir = chi / (len(bincenters3) - 3)
    #print('Chi2: ', chi)
    print('Chi2 ridotto: ', np.around(chir, 3))
    print('Energia finale massima: ', np.around(E_fin3[len(E_fin3)-1], 3))


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

    if chir>0.5 and chir<1.4:
        print("\nLa simulazione è rappresentativa della legge di potenza studiata.")
    else:
        print("\nLa simulazione non è rappresentativa della legge di potenza studiata.\nA tal fine è necessario inserire parametri migliori.")




else:
    print('\nNessuna configurazione corrisponde al numero selezionato.\nPer favore ritentare.')
