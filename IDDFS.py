class No:
    def __init__(self, estado, pai=None, acao=None, custo=0, nivel=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
        self.nivel = nivel
        self.filhos = []
    
    def caminho(self):
        """Retorna o caminho do estado inicial até este nó"""
        caminho = []
        no_atual = self
        while no_atual:
            caminho.append((no_atual.estado, no_atual.acao))
            no_atual = no_atual.pai
        return list(reversed(caminho))

def gerar_sucessores(no):
    """Gera os sucessores de um nó aplicando as ações possíveis"""
    sucessores = []
    estado = no.estado
    
    # Ação: +1
    filho1 = No(estado + 1, no, "+1", no.custo + 1, no.nivel + 1)
    no.filhos.append(filho1)
    sucessores.append(filho1)
    
    # Ação: *2
    filho2 = No(estado * 2, no, "*2", no.custo + 1, no.nivel + 1)
    no.filhos.append(filho2)
    sucessores.append(filho2)
    
    return sucessores

def desenhar_arvore(raiz, objetivo, nos_solucao):
    """Desenha a árvore de busca de forma visual"""
    print(f"\n{'='*80}")
    print(f"ARVORE DE BUSCA GERADA")
    print(f"{'='*80}\n")
    
    # Conjunto de estados que levam à solução
    estados_solucao = set()
    for no_sol in nos_solucao:
        no_atual = no_sol
        while no_atual:
            estados_solucao.add(id(no_atual))
            no_atual = no_atual.pai
    
    def imprimir_no(no, prefixo="", eh_ultimo=True, eh_solucao=False):
        """Imprime um nó e seus filhos recursivamente"""
        # Define os símbolos da árvore
        conector = "└── " if eh_ultimo else "├── "
        
        # Marca se o nó faz parte da solução
        eh_caminho_solucao = id(no) in estados_solucao
        
        # Define a cor/símbolo do nó
        if no.estado == objetivo:
            simbolo = "[*]"
            marcador = " <<< OBJETIVO!"
        elif eh_caminho_solucao:
            simbolo = "[+]"
            marcador = " (caminho solucao)"
        else:
            simbolo = "[ ]"
            marcador = ""
        
        # Monta a linha do nó
        if no.acao:
            linha = f"{prefixo}{conector}{simbolo} [{no.acao}] -> {no.estado}{marcador}"
        else:
            linha = f"{simbolo} RAIZ: {no.estado} (Estado Inicial)"
        
        print(linha)
        
        # Prepara prefixo para os filhos
        if no.acao:  # Se não for a raiz
            if eh_ultimo:
                novo_prefixo = prefixo + "    "
            else:
                novo_prefixo = prefixo + "|   "
        else:
            novo_prefixo = ""
        
        # Imprime os filhos
        for i, filho in enumerate(no.filhos):
            eh_ultimo_filho = (i == len(no.filhos) - 1)
            imprimir_no(filho, novo_prefixo, eh_ultimo_filho)
    
    imprimir_no(raiz)
    print()

def busca_profundidade_limitada_com_arvore(no_inicial, objetivo, limite):
    """Busca em profundidade com limite - constrói a árvore completa"""
    nos_visitados = 0
    pilha = [(no_inicial, 0, set())]
    solucoes = []
    
    while pilha:
        no_atual, profundidade, visitados_caminho = pilha.pop()
        nos_visitados += 1
        
        # Verifica se chegou ao objetivo
        if no_atual.estado == objetivo:
            solucoes.append(no_atual)
            continue
        
        # Verifica se atingiu o limite de profundidade
        if profundidade < limite:
            novos_visitados = visitados_caminho | {no_atual.estado}
            
            # Gera sucessores
            sucessores = gerar_sucessores(no_atual)
            
            # Adiciona sucessores à pilha
            for sucessor in reversed(sucessores):
                if sucessor.estado not in novos_visitados:
                    pilha.append((sucessor, profundidade + 1, novos_visitados))
    
    return solucoes, nos_visitados, no_inicial

def mostrar_caminhos_detalhados(solucoes):
    """Mostra todos os caminhos encontrados de forma detalhada"""
    print(f"{'='*80}")
    print(f"TODOS OS CAMINHOS ENCONTRADOS ({len(solucoes)} caminho(s))")
    print(f"{'='*80}\n")
    
    for idx, solucao in enumerate(solucoes, 1):
        caminho = solucao.caminho()
        print(f"Caminho #{idx}:")
        print("-" * 80)
        
        # Monta a visualização em linha
        passos = []
        for i, (estado, acao) in enumerate(caminho):
            if i == 0:
                passos.append(f"[{estado}]")
            else:
                passos.append(f"--{acao}--> [{estado}]")
        
        print("  " + " ".join(passos))
        print(f"  Custo total: {solucao.custo} | Passos: {len(caminho) - 1}\n")

def aprofundamento_iterativo(estado_inicial, estado_objetivo, limite_maximo=50):
    """Implementa a busca com aprofundamento iterativo"""
    print(f"\n{'='*80}")
    print(f"BUSCA COM APROFUNDAMENTO ITERATIVO")
    print(f"{'='*80}")
    print(f"Estado Inicial: {estado_inicial}")
    print(f"Estado Objetivo: {estado_objetivo}")
    print(f"Acoes disponiveis: +1 (somar 1) e *2 (multiplicar por 2)")
    print(f"{'='*80}\n")
    
    total_visitados = 0
    
    # Itera aumentando o limite de profundidade
    for profundidade in range(limite_maximo):
        print(f"Explorando profundidade {profundidade}...", end=" ")
        
        no_inicial = No(estado_inicial, nivel=0)
        solucoes, nos_visitados, raiz = busca_profundidade_limitada_com_arvore(
            no_inicial, estado_objetivo, profundidade
        )
        
        total_visitados += nos_visitados
        
        if solucoes:
            print(f"Solucao encontrada!\n")
            
            # Desenha a árvore
            desenhar_arvore(raiz, estado_objetivo, solucoes)
            
            # Mostra os caminhos detalhados
            mostrar_caminhos_detalhados(solucoes)
            
            # Encontra o melhor caminho
            melhor_caminho = min(solucoes, key=lambda x: x.custo)
            
            print(f"{'='*80}")
            print(f"MELHOR CAMINHO (Menor Custo)")
            print(f"{'='*80}\n")
            
            caminho_melhor = melhor_caminho.caminho()
            
            print("Detalhamento passo a passo:")
            print("-" * 80)
            for i, (estado, acao) in enumerate(caminho_melhor):
                if acao:
                    print(f"  Passo {i}: Aplica '{acao}' -> Estado resultante: {estado}")
                else:
                    print(f"  Inicio: Estado = {estado}")
            
            print(f"\n{'='*80}")
            print(f"ESTATISTICAS FINAIS")
            print(f"{'='*80}")
            print(f"  Total de caminhos validos: {len(solucoes)}")
            print(f"  Total de nos explorados: {total_visitados}")
            print(f"  Custo do melhor caminho: {melhor_caminho.custo}")
            print(f"  Profundidade da solucao: {profundidade}")
            print(f"{'='*80}\n")
            
            return melhor_caminho
        else:
            print("Nenhuma solucao neste nivel")
    
    print(f"\nNenhuma solucao encontrada ate profundidade {limite_maximo}")
    return None

def main():
    print("\n" + "="*80)
    print("ALGORITMO DE BUSCA EM ARVORE - APROFUNDAMENTO ITERATIVO")
    print("="*80)
    
    try:
        estado_inicial = int(input("\nDigite o ESTADO INICIAL (numero inteiro positivo): "))
        estado_objetivo = int(input("Digite o ESTADO OBJETIVO (numero inteiro positivo): "))
        
        if estado_inicial <= 0 or estado_objetivo <= 0:
            print("\nErro: Digite apenas numeros positivos!")
            return
        
        if estado_inicial > estado_objetivo:
            print("\nErro: O estado inicial nao pode ser maior que o objetivo!")
            print("      Com as operacoes +1 e *2, nao e possivel diminuir valores.")
            return
        
        if estado_inicial == estado_objetivo:
            print("\nOs estados sao iguais! Nenhuma acao necessaria.")
            print("Custo: 0")
            return
        
        # Executa a busca
        aprofundamento_iterativo(estado_inicial, estado_objetivo)
        
    except ValueError:
        print("\nErro: Digite apenas numeros inteiros validos!")
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuario!")

if __name__ == "__main__":
    main()