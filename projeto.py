global stringletras
stringletras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  #Esta string irá ser utilizada para ver qual a coluna da interseção


def eh_territorio(t):       
    """
    Verifica se o território é válido.
    Para o território ser válido tem de ser um tuplo de tuplos, com tamanho positivo inferior a 27 e cujos valores ou é 0 ou 1.

    :param t: tuplo
    :return: boolean
    """

    if type(t) != tuple:    
        return False
    elif len(t)>26 or len(t)<1:
        return False
    for i in t:
        if type(i)!= tuple:
            return False
        elif len(t[len(t)-1]) != len(i):
            return False
        elif len(i)>99 or len(i)<1:
            return False 
        for a in i:
            if a not in [0,1] or type(a)!=int:
                return False
    return True

def obtem_ultima_intersecao(t):      
    """
    Obtem a última interseção do território

    :param t: tuplo
    :return: tuplo
    """

    letra = stringletras[len(t)-1]
    num = len(t[0])
    return (letra,num)

def eh_intersecao(x):       
    """
    Verifica se a interseção é válida.
    Para ser válida, tem de corresponder a um tuplo com uma letra de A a Z e um número de 1 a 99.

    :param x: tuplo
    :return: boolean
    """

    if type(x)!= tuple:
        return False
    if len(x)!=2:
        return False
    letra = x[0]
    num = x[1]
    if type(letra) == str:
        if len(letra)!=1 or letra not in stringletras:
            return False
        if stringletras.index(letra)<=25:
            if type(num)==int:
                if num <100 and num >0:
                    return True
    return False

def eh_intersecao_valida(t,x):      
    """
    Verifica se a interseção é válida e se pertence ao território introduzido.
    Para ser válida, tem de corresponder a um tuplo com uma letra de A a Z e um número de 1 a 99.

    :param t: tuplo
    :param x: tuplo
    :return: boolean
    """

    if eh_intersecao(x)== False:
        return False
    letra = x[0]
    num = x[1]
    if stringletras.index(letra) < len(t):
        if num<= len(t[0]):
            return True
    return False

def eh_intersecao_livre(t,x):       
    """
    Verifica se a interseção corresponde a uma montanha ou não.
    Para corresponder a uma montanha, o seu valor tem de ser 1.
    Para ser uma interseção livre, o seu valor tem de ser 0.

    :param t: tuplo
    :param x: tuplo
    :return: boolean
    """

    letra = x[0]
    coluna = stringletras.index(letra)
    num = x[1]-1
    sitio = t[coluna]
    montanha = sitio[num]
    if montanha == 1:
        return False
    else:
        return True

def obtem_intersecoes_adjacentes(t,x):      
    """
    Obtem as interseções adjacentes por ordem de leitura do território.
    A ordem de leitura do território é: Baixo, Esquerda, Direita, Cima. 

    :param t: tuplo
    :param x: tuplo
    :return: tuplo
    """

    res = ()
    letra = x[0]
    num = x[1]
    coluna = stringletras.index(letra)
    num_max = len(t[0])
    coluna_max = len(t)-1
    if num>1:
        res += ((letra,num-1),)
    if letra != "A":
        res += ((stringletras[coluna-1],num),)
    if coluna < coluna_max:
        res+= ((stringletras[coluna+1],num),)
    if num < num_max:
        res += ((letra,num+1),)
    return res

def ordenacao(x):       
    """
    Função funcional para a chave da função sorted (que se encontra em ordena_intersecoes()).

    :param i: tuplo
    :return: tuplo
    """

    return x[1], x[0]

def ordena_intersecoes(x):     
    """
    Ordena as interseções por ordem de leitura do território.
    A ordem de leitura do território é: Baixo, Esquerda, Direita, Cima. 

    :param x: tuplo
    :return: tuplo
    """

    return tuple(sorted(x, key = ordenacao))

def territorio_para_str(t):      
    """
    Altera o território para uma string verificando se é um território válido.
    Para o território ser válido tem de ser um tuplo de tuplos, com tamanho positivo inferior a 27 e cujos valores ou é 0 ou 1.

    :param t: tuplo
    :return: string
    """

    if eh_territorio(t) == False:
        raise ValueError ("territorio_para_str: argumento invalido")
    num_letras = len(t)
    str = "   "
    for i in range(num_letras-1):           #Coloca as letras que aparecem na parte de cima por ordem
        str+= f"{stringletras[i]} "
    str += f"{stringletras[num_letras-1]}"
    fim = str
    str += "\n"
    num_colunas = len(t[0])
    while num_colunas >= 10:                #Alinha o algarismo das unidades dos números com algarismos com os números de apenas um algarismo
        str += f"{num_colunas} "
        for i in range(num_letras):
            if t[i][num_colunas-1]== 0:
                str += ". "
            else:
                str += "X "
        str += f"{num_colunas}"
        str += "\n"
        num_colunas -=1

    while num_colunas > 0:                  #Alinha os números de apenas um algarismo
        str += f" {num_colunas} "
        for i in range(num_letras):
            if t[i][num_colunas-1]== 0:
                str += ". "
            else:
                str += "X "
        str += f" {num_colunas}"
        str += "\n"
        num_colunas -=1
    str += fim
    return str

def obtem_cadeia(t,x):          
    """
    Obtem a cadeia correspondente à respetiva interseção no respetivo território, verificando os seus argumentos.
    Os argumentos são: t- território; x- interseção.
    Para o território ser válido tem de ser um tuplo de tuplos, com tamanho positivo inferior a 27 e cujos valores ou é 0 ou 1.
    Para ser válida, tem de corresponder a um tuplo com uma letra de A a Z e um número de 1 a 99. Além disso, tem de pertencer ao território.

    :param t: tuplo
    :param x: tuplo
    :return: tuplo
    """

    if eh_territorio(t) == False or eh_intersecao_valida(t,x) == False or eh_intersecao(x) == False:
        raise ValueError ("obtem_cadeia: argumentos invalidos")  
    cadeia = eh_intersecao_livre(t,x)
    porvisitar = [x]
    vistas = []
    res = ()
    while len(porvisitar) != 0:
        i = porvisitar[0]
        porvisitar.remove(i)
        if i not in vistas: 
            vistas += [i,]
            if eh_intersecao_livre(t,i) == cadeia:
                res += (i,)
                adjacentes = obtem_intersecoes_adjacentes(t,i)
                for a in adjacentes:
                    if a not in vistas:
                        porvisitar += [a,]
                    
    return ordena_intersecoes(res)

def obtem_vale(t,x):        
    """
    Obtem o vale da cadeia de montanhas correspondente no respetivo território, verificando os argumentos.
    Os argumentos são: t- território; x- interseção.
    Para o território ser válido tem de ser um tuplo de tuplos, com tamanho positivo inferior a 27 e cujos valores ou é 0 ou 1.
    Para ser válida, tem de corresponder a um tuplo com uma letra de A a Z e um número de 1 a 99. Além disso, tem de pertencer ao território.

    :param t: tuplo
    :param x: tuplo
    :return: tuplo
    """

    if eh_territorio(t) == False or eh_intersecao_valida(t,x) == False or eh_intersecao(x) == False or eh_intersecao_livre(t,x) == True:
        raise ValueError ('obtem_vale: argumentos invalidos')
    montanha = obtem_cadeia(t,x)
    res = ()
    for i in montanha:
        adjacentes = obtem_intersecoes_adjacentes(t,i)
        for a in adjacentes:
            if a not in montanha and a not in res:
                res += (a,)
    return ordena_intersecoes(res)

def verifica_conexao(t,x1,x2):      
    """
    Verifica se as interseções estão conectadas, ou seja, se estão na mesma cadeia no respetivo território, verificando os seus argumentos.
    Os argumentos são: t- território; x1- interseção; x2- interseção.
    Para o território ser válido tem de ser um tuplo de tuplos, com tamanho positivo inferior a 27 e cujos valores ou é 0 ou 1.
    Para ser válida, tem de corresponder a um tuplo com uma letra de A a Z e um número de 1 a 99. Além disso, tem de pertencer ao território.

    :param t: tuplo
    :param x1: tuplo
    :param x2: tuplo
    :return: boolean
    """

    if eh_territorio(t) == False or eh_intersecao_valida(t,x1) == False or eh_intersecao(x1) == False or eh_intersecao_valida(t,x2) == False or eh_intersecao(x2) == False:
        raise ValueError ('verifica_conexao: argumentos invalidos')
    cadeiax1 = eh_intersecao_livre(t,x1)
    cadeiax2 = eh_intersecao_livre(t,x2)
    if cadeiax1 == cadeiax2:
        if cadeiax1 == False:
            cadeia = obtem_cadeia(t,x1)
            if x2 in cadeia:
                return True
        else:
            porvisitar = [x1]
            vistas = []
            res = ()
            while len(porvisitar) != 0:
                i = porvisitar[0]
                porvisitar.remove(i)
                if i not in vistas: 
                    if i != x2:
                        vistas += [i,]
                        if eh_intersecao_livre(t,i) == cadeiax1:
                            res += (i,)
                            adjacentes = obtem_intersecoes_adjacentes(t,i)
                            for a in adjacentes:
                                if a not in vistas:
                                    porvisitar += [a,]
                    else:
                        return True
            if x2 not in res:
                return False
    return False

def calcula_numero_montanhas(t):        
    """
    Calcula o número de montanhas de um território, verificando o seu argumento.
    O argumento é: t- território.
    Para o território ser válido tem de ser um tuplo de tuplos, com tamanho positivo inferior a 27 e cujos valores ou é 0 ou 1.
    
    :param t: tuplo
    :return: integer
    """

    if eh_territorio(t) == False:
        raise ValueError ("calcula_numero_montanhas: argumento invalido")
    num = 0
    for i in t:
        for a in i:
            if a == 1:
                num +=1
    return num

def calcula_numero_cadeias_montanhas(t):        
    """
    Calcula o número de cadeias de montanhas do respetivo território, verificando o seu argumento.
    O argumento é: t- território.
    Para o território ser válido tem de ser um tuplo de tuplos, com tamanho positivo inferior a 27 e cujos valores ou é 0 ou 1.

    :param t: tuplo
    :return: integer
    """

    if eh_territorio(t) == False:
        raise ValueError ("calcula_numero_cadeias_montanhas: argumento invalido")
    porvisitar = []
    visitadas = []
    num = 0
    for i in range(len(t)):
        letra = stringletras[i]
        a = 0
        while a < len(t[0]):
            if t[i][a] == 1:
                posicao = (letra,a+1)
                porvisitar += [posicao,]
            a +=1
    for i in porvisitar:
        if i not in visitadas:
            cadeia = obtem_cadeia(t,i)
            for a in cadeia:
                visitadas += [a,] 
            num += 1
    return num

def calcula_tamanho_vales(t):       
    """
    Calcula o tamanho dos vales do respetivo território, verificando o seu argumento
    O argumento é: t- território.
    Para o território ser válido tem de ser um tuplo de tuplos, com tamanho positivo inferior a 27 e cujos valores ou é 0 ou 1.

    :param t: tuplo
    :return: integer
    """

    if eh_territorio(t) == False:
        raise ValueError ('calcula_tamanho_vales: argumento invalido')
    porvisitar = []
    visitadas = []
    vales = []
    tamanho = 0
    i = 0
    while i<len(t):
        letra = stringletras[i]
        a = 0
        while a < len(t[i]):
            if t[i][a] == 1:
                posicao = (letra,a+1)
                porvisitar += [posicao,]
            a +=1
        i +=1
    for i in porvisitar:
        if i not in visitadas:
            cadeia = obtem_cadeia(t,i)
            for a in cadeia:
                visitadas += [a,] 
            vales += [obtem_vale(t,i)]
    valevisto = [] 
    for i in vales:
        for a in i:
            if a not in valevisto:
                tamanho += 1
                valevisto +=[a,]          
    return tamanho
