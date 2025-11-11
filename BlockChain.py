import hashlib
from datetime import datetime

class Bloco:
    def __init__(self, operacao, valor, hash_atual=None):
        self.timestamp = datetime.now()
        self.operacao = operacao  # "instancia_conta", "deposito" ou "saque", so pode ser um desses 2
        self.valor = valor
        self.hash_atual = hash_atual #bloco inicial não tem hash
        self.proximo = None  #apontador pro proximo block

    def gerar_hash(self, hash_anterior):
        
        conteudo = f"{self.operacao}{self.valor}{self.timestamp}{hash_anterior}"
        return hashlib.sha256(conteudo.encode()).hexdigest()

class BlocoInicial(Bloco):
    def __init__(self, proprietario, valor_inicial):
        super().__init__("instancia_conta", valor_inicial, hash_atual="0")
        self.proprietario = proprietario  # dono da conta

class Blockchain:
    def __init__(self, nome_da_conta: str, balanco_inicial=1000):
        # salva o nome, se quiser usar em outros métodos
        self.nome_da_conta = nome_da_conta
        
        # cria o bloco inicial com o nome e o saldo inicial
        self.bloco_inicial = BlocoInicial(nome_da_conta, balanco_inicial)
        
    def adicionar_bloco(self, operacao, valor):
        #adiciona um bloco novo mas faz todas as validacoes pra nao permitir operacoes invalidas
        if operacao not in ["deposito", "saque"]:
            raise Exception(f"OPERACAO INVALIDA: {operacao}. SO EH PERMITIDO 'deposito' ou 'saque'.")
            return

        #usa a funcao de calcular o saldo ao inves de guardar em uma variavel (eh mais legal assim)
        saldo_atual = self.calcular_saldo()

        # validação do saque
        if operacao == "saque" and valor > saldo_atual:
            raise Exeption(f"OPERACAO INVALIDA, SALDO INSUFICIENTE ({saldo_atual}).")
            return

        # percorre até o último bloco pra puxar o ponteiro certo 
        atual = self.bloco_inicial
        while atual.proximo is not None:
            atual = atual.proximo


        # cria novo bloco
        novo_bloco = Bloco(operacao, valor)
        if atual.hash_atual:
            hash_anterior = atual.hash_atual
        else:
            raise Exception("não existe bloco anterior, operacao deu erro")
            
        novo_bloco.hash_atual = novo_bloco.gerar_hash(hash_anterior)
        atual.proximo = novo_bloco


        # cria novo bloco e encadeia na blockchain
        #novo_bloco = Bloco(operacao, valor, atual.hash_atual) versao 1
        # atual.proximo = novo_bloco versao 1 (desconsiderar)

        print(f"BLOCO {operacao} COM {valor} ADICIONADO COM SUCESSO (tem que retornar pro client agora)")

    #util pois a gente quer saber o valor atual da conta... Mas também pra validar a operacao de saque
    def calcular_saldo(self):
        saldo = 0
        atual = self.bloco_inicial

        # percorre toda a lista encadeada
        while atual is not None:
            if atual.operacao == "instancia_conta":
                saldo += atual.valor
            elif atual.operacao == "deposito":
                saldo += atual.valor
            elif atual.operacao == "saque":
                saldo -= atual.valor
            atual = atual.proximo

        return saldo

    def imprimir_cadeia(self):
        atual = self.bloco_inicial
        i = 0
        saida = ""

        while atual:
            saida += f"Bloco {i}:\n"
            if hasattr(atual, "proprietario"):  # apenas no bloco inicial
                saida += f"  Proprietário: {atual.proprietario}\n"
            saida += f"  Operação: {atual.operacao}\n"
            saida += f"  Valor: {atual.valor}\n"
            saida += f"  Hash atual: {atual.hash_atual}\n\n"

            atual = atual.proximo
            i += 1

        if saida:
            return saida
        else:
            return "BlockChainVazia" #nao pode acontecer pq  blockchain ja eh inicializada com valor dentro
