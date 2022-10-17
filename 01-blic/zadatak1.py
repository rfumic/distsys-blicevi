def funkcija(lista):
    assert(isinstance(lista,list) and all(isinstance(x,str) for x in lista))
    return { k:lista[k][::-1] for k in range(len(lista))   }