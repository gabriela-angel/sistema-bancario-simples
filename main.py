import textwrap
from abc import ABC, abstractmethod

class Cliente:
	def __init__(self, endereco):
		self.endereco = endereco
		self.contas = []

	def realizar_transacao(self, conta, transacao):
		transacao.registrar(conta)

	def adicionar_conta(self, conta):
		self.contas.append(conta)

class PessoaFisica(Cliente):
	def __init__(self, endereco, cpf, nome, data_nascimento):
		super().__init__(endereco)
		self.cpf = cpf
		self.nome = nome
		self.data_nascimento = data_nascimento

	def listar_contas(self):
		print("\n================ CONTAS ================")
		print("|                                      |")
		for conta in self.contas:
			print(conta)
		if not self.contas:
			print("|       Não foram criadas contas       |")
			print("|          para este usuario.          |")
			print("|                                      |")
		print("========================================")

class Conta:
	def __init__(self, numero, cliente):
		self._saldo = 0
		self._numero = numero
		self._agencia = "0001"
		self._cliente = cliente
		self._historico = Historico()

	@property
	def saldo(self):
		return self._saldo
	
	@property
	def numero(self):
		return self._numero
	
	@property
	def agencia(self):
		return self._agencia
	
	@property
	def cliente(self):
		return self._cliente
	
	@property
	def historico(self):
		return self._historico

	@classmethod
	def nova_conta(cls, cliente, numero):
		return cls(numero, cliente)

	def sacar(self, valor):
		if valor <= 0:
			print("Operação falhou! O valor informado é inválido.")
		elif valor > self._saldo:
			print("Operação falhou! Saldo insuficiente.")
		else:
			self._saldo -= valor
			print(f"Saque de R${valor:.2f} realizado com sucesso.")
			return True
		return False

	def depositar(self, valor):
		if valor <= 0:
			print("Operação falhou! O valor informado é inválido.")
			return False 
		else:
			self._saldo += valor
			print(f"Depósito de R${valor:.2f} realizado com sucesso.")
		return True

class ContaCorrente(Conta):
	def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
		super().__init__(numero, cliente)
		self._limite = limite
		self._limite_saques = limite_saques

	def sacar(self, valor):
		numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])

		if numero_saques >= self._limite_saques:
			print("Operação falhou! Limite de saques diários excedido.")
		elif valor >= self._limite:
			print("Operação falhou! O valor do saque excede o limite.")
		else:
			return super().sacar(valor)
		return False
	
	def __str__(self):
		return (
			"|   " + f"AGENCIA: {self.agencia}".ljust(35) + "|\n" +
			"|   " + f"CONTA: {self.numero}".ljust(35) + "|\n" +
			"|   " + f"TITULAR: {self.cliente.nome}".ljust(35) + "|\n" +
			"|                                      |")

class Historico:
	def __init__(self):
		self._transacoes = []

	@property
	def transacoes(self):
		return self._transacoes

	def adicionar_transacao(self, transacao):
		self.transacoes.append(
			{
				"tipo": transacao.__class__.__name__,
				"valor": transacao.valor
			}
		)

class Transacao(ABC):
	@property
	def valor(self):
		pass

	@abstractmethod
	def registrar(self, conta: Conta):
		pass

class Deposito(Transacao):
	def __init__(self, valor: float):
		self._valor = valor

	@property
	def valor(self):
		return self._valor

	def registrar(self, conta: Conta):
		sucesso_transacao = conta.depositar(self.valor)
		if sucesso_transacao:
			conta.historico.adicionar_transacao(self)

class Saque(Transacao):
	def __init__(self, valor: float):
		self._valor = valor

	@property
	def valor(self):
		return self._valor

	def registrar(self, conta: Conta):
		sucesso_transacao = conta.sacar(self.valor)
		if sucesso_transacao:
			conta.historico.adicionar_transacao(self)

def menu(option):
	welcome_menu = """
	========= BEM VINDO! =========
	|                            |
	|   [1] Entrar               |
	|   [2] Criar usuario        |
	|   [0] Sair                 |
	|                            |
	==============================

	=> """
	main_menu = """
	============ MENU ============
	|                            |
	|   [1] Depositar            |
	|   [2] Sacar                |
	|   [3] Vizualizar extrato   |
	|   [4] Criar conta          |
	|   [5] Listar contas        |
	|   [0] Sair                 |
	|                            |
	==============================

	=> """
	if option == "welcome":
		return textwrap.dedent(welcome_menu)
	elif option == "main":
		return textwrap.dedent(main_menu)
	else:
		return "NULL"

def buscar_conta(cpf, numero_conta, contas):
	for conta in contas:
		if conta.cliente.cpf == cpf and conta.numero == numero_conta:
			return conta
	print("Conta não encontrada ou não pertence ao usuário.")
	return None

def sacar(user, contas):
	n_conta = int(input("\nDigite o número da conta para o saque: ").strip())
	conta = buscar_conta(user.cpf, n_conta, contas)
	if not conta:
		return

	saque = input("Informe o valor do saque: ")
	try:
		saque = float(saque)
		transacao = Saque(saque)
		user.realizar_transacao(conta=conta, transacao=transacao)
	except ValueError:
		print("Operação falhou! O valor informado é inválido.")

def depositar(user, contas):
	n_conta = int(input("\nDigite o número da conta para o depósito: ").strip())
	conta = buscar_conta(user.cpf, n_conta, contas)
	if not conta:
		return

	deposito = input("Valor a ser depositado: ")
	try:
		deposito = float(deposito)
		transacao = Deposito(deposito)
		user.realizar_transacao(conta=conta, transacao=transacao)
	except ValueError:
		print("Operação falhou! O valor informado é inválido.")

def visualizar_extrato(user, contas):
	n_conta = int(input("\nDigite o número da conta, ou digite \"0\" para ver o extrato de todas as contas: ").strip())
	if n_conta != 0:
		conta = buscar_conta(user.cpf, n_conta, contas)
		if conta:
			conta_escolhida = [conta]
		else:
			return
	else:
		if not user.contas:
			print("\nNenhuma conta encontrada.")
			return
		conta_escolhida = user.contas

	for conta in conta_escolhida:
		transacoes = conta.historico.transacoes
		extrato = ""
		if not transacoes:
			extrato = "\n|   Não foram realizadas movimentações.   |"
		else:
			for transacao in transacoes:
				if transacao["tipo"] == "Deposito":
					extrato += "\n|" + f"+ R$ {transacao['valor']:.2f}".rjust(38) + "   |"
				else:
					extrato += "\n|" + f"- R$ {transacao['valor']:.2f}".rjust(38) + "   |"
		print("\n================= EXTRATO =================")
		print("|                                         |")
		print("|" + f"CONTA: {conta.numero}".rjust(38) + "   |")
		print("|                                         |", end="")
		print(extrato)
		print("|" + f"TOTAL: R${conta.saldo:.2f}".rjust(38) + "   |")
		print("|                                         |")
		print("===========================================\n")

def criar_conta(user, contas):
	numero_conta = len(contas) + 1
	conta = ContaCorrente.nova_conta(cliente=user, numero=numero_conta)
	contas.append(conta)
	user.adicionar_conta(conta)

	print(f"Conta criada com sucesso!")

def perfil_user(user, contas):
	while (True):
		cmd = input(menu("main")).strip()
		if cmd == "0":
			break
		elif cmd == "1":
			depositar(user, contas)
		elif cmd == "2":
			sacar(user, contas)
		elif cmd == "3":
			visualizar_extrato(user, contas)
		elif cmd == "4":
			criar_conta(user, contas)
		elif cmd == "5":
			user.listar_contas()
		else:
			print("Operação inválida, por favor selecione novamente.")

def adicionar_user(users):
	nome = input("Digite o nome do usuário: ").strip()
	if not nome:
		print("Todos os campos são obrigatórios.")
		return

	nascimento = input("Digite a data de nascimento do usuário (DD/MM/AAAA): ").strip()
	if (
		not nascimento or
		not nascimento[:2].isdigit() or
		not nascimento[3:5].isdigit() or
		not nascimento[6:].isdigit() or
		len(nascimento) != 10 or
		nascimento[2] != '/' or
		nascimento[5] != '/'
	):
		print("\nData de nascimento inválida. Por favor, use o formato DD/MM/AAAA.")
		return

	cpf = input("Digite o CPF do usuário (apenas números): ").strip()
	if not cpf or not cpf.isdigit() or len(cpf) != 11:
		print("\nCPF inválido. Deve conter apenas números e ter 11 dígitos.")
		return
	for user in users:
		if user.cpf == cpf:
			print("\nUsuário já cadastrado com esse CPF.")
			return

	endereco = input("Digite o endereço do usuário (formato: Logradouro, Número - Bairro - Cidade/UF): ").strip()
	if not endereco:
		print("\nTodos os campos são obrigatórios.")
		return

	novo_cliente = PessoaFisica(
		endereco=endereco,
		cpf=cpf,
		nome=nome,
		data_nascimento=nascimento)
	users.append(novo_cliente)
	print("\nUsuário cadastrado com sucesso!")

def main():
	users = []
	contas = []

	while (True):
		cmd = input(menu("welcome"))
		if cmd == "0":
			break
		elif cmd == "1":
			print("Digite o CPF do usuário. Não inclua espaços, pontos ou traços no CPF.\n")
			cpf = input("=> ").strip()
			for user in users:
				if cpf == user.cpf:
					print(f"\nBem vindo/a, {user.nome}!")
					perfil_user(user, contas)
					break
			else:
				print("Usuário não encontrado. Por favor, tente novamente.")
		elif cmd == "2":
			adicionar_user(users)
		else:
			print("Operação inválida, por favor selecione novamente.")

main()