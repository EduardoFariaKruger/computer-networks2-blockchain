import hashlib
from datetime import datetime

class Bloco:
    def __init__(self, operacao, valor, hash_anterior="0"):
        self.timestamp = datetime.now()
        self.operacao = operacao  # "instancia_conta", "deposito" ou "saque", so pode ser um desses 2
        self.valor = valor
        self.hash_anterior = hash_anterior
        self.hash_atual = self.gerar_hash()
        self.proximo = None  #apontador pro proximo block

    def gerar_hash(self):
        conteudo = f"{self.operacao}{self.valor}{self.timestamp}{self.hash_anterior}"
        return hashlib.sha256(conteudo.encode()).hexdigest()

class Blockchain:
    def __init__(self, balanco_inicial=1000):
        # bloco inicial
        self.bloco_inicial = Bloco("instancia_conta", balanco_inicial, "0")

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

        # cria novo bloco e encadeia na blockchain
        novo_bloco = Bloco(operacao, valor, atual.hash_atual)
        atual.proximo = novo_bloco

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

    #serve mais pra debugging
    def imprimir_cadeia(self):
        atual = self.bloco_inicial
        i = 0
        while atual:
            print(f"Bloco {i}:")
            print(f"  Operação: {atual.operacao}")
            print(f"  Valor: {atual.valor}")
            print(f"  Hash atual: {atual.hash_atual}")
            print(f"  Hash anterior: {atual.hash_anterior}\n")
            atual = atual.proximo
            i += 1
