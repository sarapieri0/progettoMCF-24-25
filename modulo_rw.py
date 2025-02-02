import numpy as np

#PRIMA CONFIGURAZIONE
def rw_origine(step0, N, x0, g):
    '''
    Funzione che incrementa il passo del
    random walk di un fattore costante g, ogni volta che la particella test
    passa per l'origine (da x>0 a x<0 e viceversa), e restituisca
    posizione e lunghezza del passo finale dopo il numero deciso di N passi'''
    if x0==0:
        x0=1
    deltax=[]
    x=x0
    check=np.random.random(N) #array di numeri distribuiti normalmente in (0,1)
    step=step0
    count=0
    for c in check:
        if c >= 0.5:
            x=x+step
        else:
            x=x-step
        deltax.append(x)

        '''
        condizioni per la modifica del passo in corrispondenza dell'origine'''
        if(count>0):
            if ((x*deltax[count-1])<0):
                step=g*step
        count+=1
    return np.array(deltax), step


#SECONDA CONFIGURAZIONE
def rw_riflessione(step0, N, x0, g, xmax, b):
    '''
    Funzione che incrementa il passo del random walk (accelerazione) e inverte la direzione
    della particella (riflessione) ogni volta che attraversa l'origine,mentre in corrispondenza della barriera xmax
    la particella è solo riflessa.
    La barriera decresce costantemente con passo b.
    '''
    if x0==0:
        x0=1
    deltax = [x0]  
    mas = [xmax]   
    x = x0        
    step = step0 
    i = 0
    
    check = np.random.random(N)
    

    while (i < N-1):
        if (x < 0) or (x >= xmax):
            if x < 0 and deltax[i - 1] > 0:  # Passaggio attraverso l'origine
                x += step
                step=step* g  # Accelerazione
            elif x >= xmax:  # Riflesso contro xmax
                x -= step
                
            i += 1  # Incremento del contatore
            mas.append(xmax)
            xmax -= b  # Aggiornamento della barriera
            deltax.append(x)

        else:
            # Passo casuale della particella
            if check[i] >= 0.5:
                x += step
            else:
                x -= step
            deltax.append(x)
            i += 1
            xmax -= b  # Aggiornamento della barriera
            mas.append(xmax)

    return np.array(deltax), np.array(mas), step


#TERZA CONFIGURAZIONE
def rw_accelerazione(step0, N, x0, g, xmax, b):
    '''
    Funzione che incrementa il passo del random walk (accelerazione) e inverte la direzione
    della particella (riflessione) ogni volta che
    questa attraversa l'origine, passando da x>0 a x<0 (e viceversa) e
    quando intercetta la barriera costituita dalla retta descrescente xmax,
    la quale parte da una quota predefinita e descresce costantemente con
    passo determinato (b)'''
    
    if(x0==0):
        x0=1
    deltax=[x0]
    x=x0
    step=step0
    i=0
    check=np.random.random(N)
    mas=[xmax]
    while(i<N-1):
        if ((x<0)or(x>=xmax)):
            if((x<0)and(deltax[i-1]>0)): #passaggio attraverso l'origine
                x=x+step
            if(x>=xmax):
                x=x-step
            xmax-=b
            i+=1
            step=step*g
            mas.append(xmax)
            deltax.append(x)

        else:
            if check[i]>=0.5: 
                x=x+step
            else:
                x=x-step
            deltax.append(x)
            i+=1
            xmax=xmax-b
            mas.append(xmax)

    return np.array(deltax), np.array(mas), step
    
