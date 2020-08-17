import re

# Validacao CPF e CNPJ
def validar_cpf(cpf):
    cpf = ''.join(re.findall('\d', str(cpf)))
    
    #Se não tiver numeros já retorna falso
    if (not cpf): # or (len(cpf) < 11):
        return False
    
    #Se só tiver zeros, retorna falso
    if int(cpf) == 0:
        return False

    #Se tiver só números iguais
    if len(set(cpf)) == 1:
        return False

    #000.000.00X-00 o X demarca a regiao.
    if len(cpf) < 3:
        return False
    
    #Completa quantidade de digitos
    while len(cpf) < 11:
        cpf = "0"+cpf
    
    # Pega apenas os 9 primeiros dígitos do CPF e gera os 2 dígitos que faltam
    inteiros = list(map(int, cpf))
    novo = inteiros[:9]

    while len(novo) < 11:
        r = sum([(len(novo)+1-i)*v for i,v in enumerate(novo)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        #return cpf
        return True
    return False

def validar_cnpj(cnpj):

    cnpj = ''.join(re.findall('\d', str(cnpj)))
    
    #Se não tiver numeros já retorna falso
    if (not cnpj):
        return False
    
    #Se só tiver zeros, retorna falso
    if int(cnpj) == 0:
        return False

        #Se tiver só números iguais
    if len(set(cnpj)) == 1:
        return False
    
    # Deve conter pelo menos três digitos - CNPJ BB por exemplo
    if len(cnpj) < 3:
        return False
    
    #Completa quantidade de digitos
    while len(cnpj) < 14:
        cnpj = "0"+cnpj
    
    
    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = list(map(int, cnpj))
    novo = inteiros[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        #return cnpj
        return True
    return False


#Validacao Email

def validar_email(string):
    string = string.lower()
    pos = string.find("@")
    dot = string.rfind(".")
    if pos < 1:
        return False
    if dot < pos + 2:
        return False
    if dot + 2 >= len(string):
        return False
    
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', string)
    if string:
        return True
    return false

#Validacao Titulo
def validar_titulo(titulo):
    
    titulo = ''.join(re.findall('\d', str(titulo)))
    
    # Se não tiver numeros ja retorna False
    if (not titulo): # or (len(cpf) < 11):
        return False
    
    # Se for zero ja retorna
    if int(titulo) == 0:
        return False
    
    #Se tiver só números iguais
    if len(set(titulo)) == 1:
        return False

    #0000 0000 XX00 o X demarca a regiao.
    if len(titulo) < 6:
        return False
    
    # Completa quantidade de digitos
    while len(titulo) < 12:
        titulo = "0"+titulo
    
    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = list(map(int, titulo))
    novo = inteiros[:8]

    #prod = [2, 3, 4, 5, 6, 7, 8, 9]
    prod = list(range(2,10))
    #print(prod)
    
    dv1 = sum([x*y for (x, y) in zip(novo, prod)]) % 11
    if dv1 == 10:
        dv1 = 0
    
    #prod = [7, 8, 9]
    prod = list(range(7,10))
    
    dv2 = sum([x*y for (x, y) in zip(inteiros[8:10]+[dv1], prod)]) % 11
    if dv2 == 10:
        dv2 = 0
        
    if dv1 == inteiros[-2] and dv2 == inteiros[-1]:
        return True
    
    return False

def validar_nit(nit):
    nit = ''.join(re.findall('\d', str(nit)))
    
    # Se não tiver numeros ja retorna False
    if (not nit): 
        return False
    
    # Se for zero ja retorna
    if int(nit) == 0 or int(nit) < 100000:
        return False

    #Se tiver só números iguais
    if len(set(nit)) == 1:
        return False

    if len(str(int(nit))) > 11:
        return False

    #0000 0000 XX00 o X demarca a regiao.
    #if len(nit) < 3:
    #    return False
    
    # Completa quantidade de digitos
    while len(nit) < 11:
        nit = "0"+nit
    
    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = list(map(int, nit))
    novo = inteiros[:10]
    real = inteiros[10]

    #print(real)

    prod = list(reversed(range(2,4)))+list(reversed(range(2,10)))
    #print(prod)

    dv1 = 11-sum([x*y for (x, y) in zip(novo, prod)]) % 11
    #dv1 = 11-sum([x*y for (x, y) in zip(novo, prod)])*10 % 11
    
    #print(dv1)
    if dv1 == 10 or dv1 == 11:
        dv1 = 0

    if dv1 == real:
        return True

    return False

def valida_a_remover(value):
    

    ## Para remover datas (449,94)
    v = ''.join(re.findall('\/', str(value)))
    if v == '//':
        return True
    
    #Remove valor
    v = ''.join(re.findall('^\d+\,\d+', str(value)))
    if v:
        return True
    
      #Remove valor
    #v = ''.join(re.findall('^\d+\.\d+', str(value)))
    #if v:
    #    return True
    
    
    v = ''.join(re.findall('\d\d:\d\d', str(value)))
    if v:
        return True
    
    
    v = ''.join(re.findall('^\d{1,5}$', str(value)))
    #v1 = ''.join(re.findall('^\d\d$', str(value)))
    #v2 = ''.join(re.findall('^\d\d\d$', str(value)))
    
    
    #v = ''.join(re.findall('^\w{1,2}$', str(value)))
    
    if v:# or v1: # or v2:
        return True
    
    return False




def main():
    # Exemplos de validação cpf e cnpj
    print(validar_cpf("893.876.934-81"), validar_cnpj("43.622.215/0001-57"), validar_cnpj("191"))#BB

    # Exemplos de validação email
    print(validar_email("washingtoncunha.dccbr"), validar_email("washingtoncunha@ufmgdccbr"), validar_email("washingtoncunha@ufmg.dcc.br"))

    # Exemplos de validação 
    print(validar_titulo("7781 7961 1538"), validar_titulo("7781 7961 15"))

if __name__ == "__main__":
    main()