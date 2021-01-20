cadena='/newblognote Minota;nota tiene otros; como aqui'
c=cadena[12:]
print(c)
lista=c.split(';')
blog=lista[0]
lista.pop(0)
nota=";".join(lista)
print(blog)
print(nota)

print(len('/simplenote'[11:].split(';')))