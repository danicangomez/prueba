
import os
import numpy as np
import pandas as pd

#### Vamos al directorio de trabajo####
os.getcwd()
#os.chdir(ubica)
#files = os.listdir(ruta)

with open('GCOM2022_pract2_auxiliar_eng.txt', 'r',encoding="utf8") as file:
      en = file.read()
     
with open('GCOM2022_pract2_auxiliar_esp.txt', 'r',encoding="utf8") as file:
      es = file.read()


#### Contamos cuantas letras hay en cada texto
from collections import Counter
tab_en = Counter(en)
tab_es = Counter(es)

##### Transformamos en formato array de los carácteres (states) y su frecuencia
##### Finalmente realizamos un DataFrame con Pandas y ordenamos con 'sort'
tab_en_states = np.array(list(tab_en))
tab_en_weights = np.array(list(tab_en.values()))
tab_en_probab = tab_en_weights/float(np.sum(tab_en_weights))
distr_en = pd.DataFrame({'states': tab_en_states, 'probab': tab_en_probab})
distr_en = distr_en.sort_values(by='probab', ascending=True)
distr_en.index=np.arange(0,len(tab_en_states))

tab_es_states = np.array(list(tab_es))
tab_es_weights = np.array(list(tab_es.values()))
tab_es_probab = tab_es_weights/float(np.sum(tab_es_weights))
distr_es = pd.DataFrame({'states': tab_es_states, 'probab': tab_es_probab })
distr_es = distr_es.sort_values(by='probab', ascending=True)
distr_es.index=np.arange(0,len(tab_es_states))


## Ahora definimos una función que haga exáctamente lo mismo
def huffman_branch(distr):
    states = np.array(distr['states'])
    probab = np.array(distr['probab'])
    state_new = np.array([''.join(states[[0,1]])])
    probab_new = np.array([np.sum(probab[[0,1]])])
    codigo = np.array([{states[0]: 0, states[1]: 1}])
    states =  np.concatenate((states[np.arange(2,len(states))], state_new), axis=0)
    probab =  np.concatenate((probab[np.arange(2,len(probab))], probab_new), axis=0)
    distr = pd.DataFrame({'states': states, 'probab': probab, })
    distr = distr.sort_values(by='probab', ascending=True)
    distr.index=np.arange(0,len(states))
    branch = {'distr':distr, 'codigo':codigo}
    return(branch) 

def huffman_tree(distr):
    tree = np.array([])
    while len(distr) > 1:
        branch = huffman_branch(distr)
        distr = branch['distr']
        code = np.array([branch['codigo']])
        tree = np.concatenate((tree, code), axis=None)
    return(tree)
 
distr = distr_en 
tree = huffman_tree(distr)
distr1 = distr_es 
tree1 = huffman_tree(distr1)

#Buscar cada estado dentro de cada uno de los dos items
list(tree[0].items())[0][0] ## Esto proporciona un '0'
list(tree[0].items())[1][0] ## Esto proporciona un '1'


ingles = (tree, tab_en_states, tab_en_probab)
español = (tree1, tab_es_states, tab_es_probab)

#Código Huffman    
def ch(array,letra):
    codigo = ''
    for d in range(len(array)-1,-1,-1):
        for clave in list(array[d].keys()):    
            if letra in clave:
                codigo += str(array[d][clave])
    
    return codigo

def alfabeto(idioma):
    d={}
    arbol= idioma[0]
    for letra in idioma[1]:
        d[letra] = ch(arbol,letra)
    return d



def longitud_media(idioma):
    long_med = 0
    alf = alfabeto(idioma)
    pesos = idioma[2]
    i=0
    for letra in alf:
        long_med += len(alf[letra]) * pesos[i]
        i += 1
    return long_med

        
def entropia(idioma):
    suma = 0
    pesos = idioma[2]
    for prob in pesos:
        suma += prob * np.log2(prob)
    return suma * (-1)


print("Codigo SEng: ", alfabeto(ingles),'\n')
print("Codigo SEsp: ", alfabeto(español), '\n')
print("Entropía en inglés: H(eng) = ", entropia(ingles))
print("Entropía en español: H(esp) = ", entropia(español))
print("Longitud media en inglés: L = :", longitud_media(ingles))
print("Longitud media español: L = :", longitud_media(español),'\n')


def codificar(palabra, idioma):
    codigo = ''
    alf = alfabeto(idioma)
    for i in palabra:
        codigo += alf[i]
    return codigo

cod_esp = codificar("medieval", español)
cod_eng = codificar("medieval", ingles)

print("Palabra medieval codificada en español:", cod_esp)
print("Longitud palabra codificada en español:", len(cod_esp)) 
print("Palabra medieval codificada en inglés:", cod_eng)
print("Longitud palabra codificada en inglés:", len(cod_eng), '\n')


def decodifica(codigo,idioma):
    dic_cod = alfabeto(idioma)
    claves = list(dic_cod.keys())
    valores = list(dic_cod.values())
    acumulador = ''
    palabra = ''
    for digito in codigo:
        acumulador += digito
        if acumulador in valores:
            palabra += claves[valores.index(acumulador)]
            acumulador = ''
    return palabra


print("Palabra decodificada:")
print(decodifica('10111101101110110111011111', ingles))