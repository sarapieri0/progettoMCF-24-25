# progettoMCF-24-25
Repository dedicata alla consegna del progetto svolto ai fini dell'esame di Metodi Computazionali per la Fisica

Questo README contiene le istruzioni per l'esecuzione dei vari file consegnati per il progetto d'esame.

Si consegnano cinque file, di cui:
- "modulo_rw.py" che contiene le funzioni utilizzate per il Random Walk nelle tre configurazioni
- tre file 'studio' ("x0_studio.py", "g_studio.py", "xmax_studio.py") di sola lettura/visualizzazione, in cui si analizza lo spettro d'energia delle varie configurazioni tenendo fissi dei parametri, e facendone variare solo uno (rispettivamente x0, g e xmax)
- "simulazioni.py" che permette di inserire a piacimento tutti i parametri ed osservare andamenti e spettri diversi

I file studio dovrebbero essere eseguiti prima, dal momento che servono per stabilire dei valori funzionali dei parametri in esame, tenendo fissi tutti gli altri. Questo serve a dare un'idea di quanto una distribuzione sia sensibile alla variazione di quel parametro, e cioè come varia l'indice spettrale e il Chi2 ridotto associato alla bontà del fit.
All'inizio del file è stabilito il numero di simulazioni da generare per ogni configurazione, che è di default pari a 10, di conseguenza ogni file contiene lo studio associato al parametro in tutte le configurazioni in cui compare, sulla base di 10 simulazioni ciascuna.
Il parametro in esame viene fatto variare in un range tale per cui, fissati il resto dei parametri, il fit riesce ad estrarre l'indice spettrale.
Viene chiesto se visualizzare tutti i grafici o meno dal momento che sono molti.

Il file "simulazioni.py" permette di studiare ciascuna configurazione separatamente in casi differenti da quelli già analizzati nei file 'studio', suggerendo soltanto i valori funzionali (in media) già trovati per le configurazioni fissate.

Ogni simulazione ha come output in sequenza:
- grafico della traiettoria delle particelle
- parametri di fit (tra cui l'indice spettrale)
- Chi^2 ridotto associato ai dati rispetto al modello
- Energia massima raggiunta dalle particelle alla fine della traiettoria (passo più grande)
- grafico (in scala lineare e logaritmica) della distribuzione studiata applicata ai dati della simulazione, con fit


Essendo tutto simulato e di carattere stocastico, potrebbero verificarsi delle fluttuazioni che non permettono alla funzione di fit di trovare i parametri, creando problemi all'esecuzione. Dovrebbe bastare ri-eseguire il codice con gli stessi parametri per risolvere il problema
