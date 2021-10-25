class Poli:
    # padroniza metodos uteis para um polinomio
    def __init__(self, poli_fat:str):
        """recebe um polinomio na forma fatorada como '(x)*(x+1)'"""
        self.poli_fat = poli_fat
        self.grupos = None
        self.expandido = None
        self.derivada = None
    
    def agrupar(self):
        """agrupa os binomios (incognita-raiz), organizando-os em uma lista"""
        grupos = []
        grupo = ""
        dentro = False 
        for letra in self.poli_fat: # analiza letra por letra do polinomio
            if letra == ")": # avalia se esta dentro ou fora de um binomio pela posição dos parenteses
                dentro = False
                grupos.append(grupo) # organiza o monimio na lista
                grupo = ""
            
            if dentro: # armazena o que esta no interior do binomio
                grupo += letra

            if letra == "(":
                dentro = True

        return grupos
    
    def avaliar_inicial(self, grupo: str):
        """recebe um monomio como 'incognita-raiz' e retorna um dicionario
        de onde cada valor v na chave c equivale a parcela v*x**c"""
        fator = "1"
        parcela = "0"
        num = ""
        for i, letra in enumerate(grupo): # analiza cada letra para identificar os numeros e sinais
            if letra in "0123456789.j":
                num += (letra)
            
            if letra == "*":
                fator = num
            
            if letra == "+" or letra == "-":
                parcela = grupo[i:]
                break
        
        return {0: complex(parcela), 1: complex(fator), 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
    
    def preparar_inicial(self):
        """agrupa e avalia o polinomio armazenado, tornando-o usavel. depois
        gera sua versão expandida e sua derivada (ambas em forma de dicionario)"""
        lista_grupos = []
        grupos_str = self.agrupar()
        for grupo in grupos_str:
            lista_grupos.append(self.avaliar_inicial(grupo))

        self.grupos = lista_grupos
        self.expandido = self.mult_grupos(self.grupos)
        self.derivada = self.deriv_grupos(self.grupos)
    
    def somar_grupos(self, grupos):
        """recebe uma lista de dicionarios representando polinomios, os soma
        e retorna um dicionario"""
        novo = {}
        for grupo in grupos: # percorre a lista somando cada elemento em cada chave
            for chave in grupo:
                if chave not in novo.keys():
                    novo[chave] = 0
                
                novo[chave] += grupo[chave]
        
        return novo
    
    def mult_grupos(self, grupos):
        """recebe uma lista de dicionarios representando polinomios, os multiplica
        e retorna um dicionario"""
        copia = grupos[:]
        g1 = copia.pop(0)
        g2 = copia.pop(0) # seleciona 2 polinomios para serem multiplicados primeiro
        resultado = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
        for c1, f1 in g1.items(): # percorre cada valor de cada polinomio, multiplicando cada par individualmente
            if f1 != 0:
                for c2, f2 in g2.items():
                    if f2 != 0:
                        nova_chave = c1 + c2
                        resultado[nova_chave] += f1 * f2
        
        if len(copia) >= 1: # a função reduz em 1 o numero de polinomios da lista cada vez q é rodada, ate que reste apenas 1
            copia.append(resultado)
            return self.mult_grupos(copia) # recursão para reduzir a lista a apenas um polinomio
        
        else:
            return resultado
    
    def deriv_grupo(self, grupo):
        """recebe uma lista de dicionarios representanto polinomios. se houver
        apenas um, ele é derivado de forma trivial. se houver mais de um, ele é
        usado em outra função com o objetivo de diminuir o numero de polinomios"""
        if len(grupo) == 1:
            novo = {}
            for chave, item in grupo[0].items(): # derivada de um polinomio (a*x**b)' = (a*b*x**(b-1))
                if chave > 0:
                    novo[chave - 1] = chave * item
            
            novo[10] = 0
            return novo
        
        else:
            return self.deriv_grupos(grupo)
    
    def deriv_grupos(self, grupos):
        """recebe uma lista de dicionarios representando um produto de polinomios,
        os deriva usando a derivada do produto e retorna um dicionario"""
        copia = grupos[:]
        g1 = copia.pop(0) # usa o primeiro polinomio como termo fixo, com derivada trivial
        g2 = copia[:] # usa o resto da lista como termo para recursão, ja que a derivada não é trivial
        dg1 = self.deriv_grupo([g1]) # o primeiro polinomio é passado como uma lista unitaria
        dg2 = self.deriv_grupo(g2) # o resto tem menos polinomios em relação a lista inicial, sera reduzida ainda mais por recursao
        #(a.b)' = a'.b + a.b' onde ' representa a derivada
        mult1 = [g1, dg2] # primeiro termo a ser multiplicado e posteriormente usado na soma
        mult2 = g2[:] # segund termo a ser multiplicado e posteriormente usado na soma
        mult2.append(dg1)
        resultado = self.somar_grupos([self.mult_grupos(mult1), self.mult_grupos(mult2)]) # efetuando multiplicações e somas
        return resultado
    
    def resolver(self, grupo, x:complex):
        """recebe um dicionario representando um polinomio e um complexo x, usado como input
        e retorna o valor do polinomio para esse x"""
        resultado = 0
        for chave, item in grupo.items(): # utiliza a formula para cada parcela do polinomio que não for nula
            if item != 0:
                if chave > 0:
                    resultado += item * x ** chave
                
                else: # evita problemas com 0**0
                    resultado += item
        
        return resultado
    
    def __call__(self, x:complex):
        """chama o objeto como uma função. recebe um input x e retorna o valor
        do polinomio para esse x"""
        return self.resolver(self.mult_grupos(self.grupos), x)
    
    def show(self, grupo):
        texto = ""
        for chave, item in grupo.items():
            if item != 0:
                if chave == 0:
                    texto += str(item)
                
                else:
                    texto += str(item) + "*" + "x" + "**" + str(chave)
                
                texto += " + "
            
        return texto[:-2]


def main():
    equa1 = "(x+2)*(x+2j)*(x-2j)*(x-2-1j)*(x+2+1j)"
    func = Poli(equa1)
    func.preparar_inicial()
    print(func.show(func.expandido))
    print(func.show(func.derivada))

if __name__ == "__main__":
    main()
