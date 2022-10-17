def funkcija(lista):
    assert(isinstance(lista,list) and all(isinstance(x,dict) for x in lista))
    return 0

