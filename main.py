# Estabelecer um limite de 10 transacoes diarias para uma conta -> informar quando o user tiver atingido o limite; ele excedeu o numero de transacoes permitidas para aquele dia
# Mostrar data e hora de todas as transacoes no extrato

# ALTERAR PARA SO RECEBER MENSAGEM DE ACAO QUANDO TEM SUCESSO

import textwrap
import functools
from abc import ABC, abstractmethod
from datetime import datetime, date

class ContaIterador:
	def __init__(self, contas):
		self.contas = contas
		self.counter = 0

	def __iter__(self):
		return self

	def __next__(self):
		try:
			conta = self.contas[self.counter]
			self.counter += 1
			return ("|   " + f"AGENCIA: {conta.agencia}".ljust(35) + "|\n" +
			"|   " + f"CONTA: {conta.numero}".ljust(35) + "|\n" +
			"|   " + f"TITULAR: {conta.cliente.nome}".ljust(35) + "|\n" +
			"|   " + f"SALDO: {conta.saldo}".ljust(35) + "|\n" +
			"|                                      |")
		except IndexError:
			raise StopIteration

class Cliente:
	def __init__(self, endereco, limite_transacoes=10):
		self.endereco = endereco
		self.contas = []
		self._limite_transacoes = limite_transacoes

	def realizar_transacao(self, conta, transacao):
		numero_transacoes = len(conta.historico.transacoes_do_dia())

		if numero_transacoes >= self._limite_transacoes:
			print("Operação falhou! Limite de transações diárias excedido.")
		else:
			sucesso = transacao.registrar(conta)
			return sucesso
		return False

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
		if not self.contas:
			print("|       Não foram criadas contas       |")
			print("|          para este usuario.          |")
			print("|                                      |")
		else:
			for conta in ContaIterador(self.contas):
				print(conta)
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
		elif valor > self._limite:
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
				"valor": transacao.valor,
				"data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
			}
		)

	def gerar_relatorio(self, tipo_transacao=None):
		for transacao in self._transacoes:
			if tipo_transacao is None or transacao["tipo"] == tipo_transacao:
				yield transacao

	def transacoes_do_dia(self):
		transacoes_do__dia = []
		for transacao in self._transacoes:
			if datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date() == date.today():
				transacoes_do__dia.append(transacao)
		return transacoes_do__dia


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
		return sucesso_transacao

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
		return sucesso_transacao

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

def log_transacao(func):
	@functools.wraps(func)
	def envelope(*args, **kwargs):
		result = func(*args, **kwargs)
		if result:
			tipo = func.__name__.upper()
			data = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
			print(f"{data} {tipo}")

	return envelope

def buscar_conta(cpf, numero_conta, contas):
	for conta in contas:
		if conta.cliente.cpf == cpf and conta.numero == numero_conta:
			return conta
	print("Conta não encontrada ou não pertence ao usuário.")
	return None

@log_transacao
def sacar(user, contas):
	n_conta = input("\nDigite o número da conta para o saque: ").strip()
	try:
		n_conta = int(n_conta)
	except ValueError:
		print("Operação falhou! O número informado é inválido.")
		return False
	conta = buscar_conta(user.cpf, n_conta, contas)
	if not conta:
		return False

	saque = input("Informe o valor do saque: ")
	try:
		saque = float(saque)
		transacao = Saque(saque)
		sucesso = user.realizar_transacao(conta=conta, transacao=transacao)
		if not sucesso:
			return False
	except ValueError:
		print("Operação falhou! O valor informado é inválido.")
		return False
	return True

@log_transacao
def depositar(user, contas):
	n_conta = input("\nDigite o número da conta para o depósito: ").strip()
	try:
		n_conta = int(n_conta)
	except ValueError:
		print("Operação falhou! O número informado é inválido.")
		return False
	conta = buscar_conta(user.cpf, n_conta, contas)
	if not conta:
		return False

	deposito = input("Valor a ser depositado: ")
	try:
		deposito = float(deposito)
		transacao = Deposito(deposito)
		sucesso = user.realizar_transacao(conta=conta, transacao=transacao)
		if not sucesso:
			return False
	except ValueError:
		print("Operação falhou! O valor informado é inválido.")
		return False
	return True

def filtrar_extrato():
	while True:
		filtro = input("\nDeseja filtrar por tipo de transação? [Y/N] => ").strip()
		if filtro.upper() == 'Y':
			filtro = input("\nFiltrar por:\n\t[0]Apenas saques\n\t[1]Apenas depósitos\n\n\t=> ").strip()
			if filtro == '0':
				filtro = "Saque"
			elif filtro == '1':
				filtro = "Deposito"
			else:
				print("Operação inválida, por favor selecione novamente.")
				continue
			return filtro
		elif filtro.upper() == 'N':
			filtro = None
			return filtro
		else:
			print("Operação inválida, por favor selecione novamente.")

@log_transacao
def visualizar_extrato(user, contas):
	n_conta = input("\nDigite o número da conta, ou digite \"0\" para ver o extrato de todas as contas: ").strip()
	try:
		n_conta = int(n_conta)
	except ValueError:
		print("Operação falhou! O número informado é inválido.")
		return False
	if n_conta != 0:
		conta = buscar_conta(user.cpf, n_conta, contas)
		if conta:
			conta_escolhida = [conta]
		else:
			return False
	else:
		if not user.contas:
			print("\nNenhuma conta encontrada.")
			return False
		conta_escolhida = user.contas

	filtro = filtrar_extrato()
	for conta in conta_escolhida:
		tem_transacao = False
		extrato = ""
		for transacao in conta.historico.gerar_relatorio(tipo_transacao=filtro):
			tem_transacao = True
			extrato += "\n|" + f"{transacao['data']}".rjust(38) + "   |"
			if transacao["tipo"] == "Deposito":
				extrato += "\n|" + f"+ R$ {transacao['valor']:.2f}".rjust(38) + "   |"
			else:
				extrato += "\n|" + f"- R$ {transacao['valor']:.2f}".rjust(38) + "   |"
			extrato += "\n|                                         |"
		if not tem_transacao:
			extrato = "\n|   Não foram realizadas movimentações.   |"
		print("\n================= EXTRATO =================")
		print("|                                         |")
		print("|" + f"CONTA: {conta.numero}".rjust(38) + "   |")
		print("|                                         |", end="")
		print(extrato)
		print("|" + f"TOTAL: R${conta.saldo:.2f}".rjust(38) + "   |")
		print("|                                         |")
		print("===========================================\n")
	return True

@log_transacao
def criar_conta(user, contas):
	numero_conta = len(contas) + 1
	conta = ContaCorrente.nova_conta(cliente=user, numero=numero_conta)
	contas.append(conta)
	user.adicionar_conta(conta)

	print(f"Conta criada com sucesso!")
	return True

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

@log_transacao
def adicionar_user(users):
	nome = input("Digite o nome do usuário: ").strip()
	if not nome:
		print("Todos os campos são obrigatórios.")
		return False

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
		return False
	try:
		nascimento = datetime.strptime(nascimento, "%d/%m/%Y")
	except ValueError:
		print("\nData de nascimento inválida. Por favor, use o formato DD/MM/AAAA e insira uma data válida.")
		return False

	cpf = input("Digite o CPF do usuário (apenas números): ").strip()
	if not cpf or not cpf.isdigit() or len(cpf) != 11:
		print("\nCPF inválido. Deve conter apenas números e ter 11 dígitos.")
		return False
	for user in users:
		if user.cpf == cpf:
			print("\nUsuário já cadastrado com esse CPF.")
			return False

	endereco = input("Digite o endereço do usuário (formato: Logradouro, Número - Bairro - Cidade/UF): ").strip()
	if not endereco:
		print("\nTodos os campos são obrigatórios.")
		return False

	novo_cliente = PessoaFisica(
		endereco=endereco,
		cpf=cpf,
		nome=nome,
		data_nascimento=nascimento)
	users.append(novo_cliente)
	print("\nUsuário cadastrado com sucesso!")
	return True

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