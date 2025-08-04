import textwrap

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

def sacar(*, saldo, saques_realizados, extrato, limite_valor_saque, limite_diario_saque):
	if saques_realizados < limite_diario_saque:
		saque = input("Informe o valor do saque: ")
		try:
			saque = float(saque)
			if saque <= 0:
				print("Operação falhou! O valor informado é inválido.")
			elif saque > limite_valor_saque:
				print("Operação falhou! O valor do saque excede o limite.")
			elif saque > saldo:
				print("Operação falhou! Saldo insuficiente.")
			else:
				saques_realizados += 1
				saldo -= saque
				extrato += "\n|" + f"- R${saque:.2f}".rjust(38) + "   |"
				print(f"Saque de R${saque:.2f} realizado com sucesso.")
		except ValueError:
			print("Operação falhou! O valor informado é inválido.")
	else:
		print("Operação falhou! O limite de saques diários foi excedido.")
	return saldo, saques_realizados, extrato

def depositar(saldo, extrato):
	deposito = input("Valor a ser depositado: ")
	try:
		deposito = float(deposito)
		if deposito <= 0:
			print("Operação falhou! O valor informado é inválido.")
		else:
			saldo += deposito
			extrato += "\n|" + f"+ R$ {deposito:.2f}".rjust(38) + "   |"
			print(f"Depósito de R${deposito:.2f} realizado com sucesso.")
	except ValueError:
		print("Operação falhou! O valor informado é inválido.")
	return saldo, extrato

def visualizar_extrato(saldo, /, numero, *, extrato_text):
	print("\n================= EXTRATO =================")
	print("|                                         |")
	print("|" + f"CONTA: {numero}".rjust(38) + "   |")
	print("|                                         |", end="")
	print("\n|   Não foram realizadas movimentações.   |" if not extrato_text else extrato_text)
	print("|" + f"TOTAL: R${saldo:.2f}".rjust(38) + "   |")
	print("|                                         |")
	print("===========================================\n")

def validar_conta(nome, numero_conta, contas):
	if not numero_conta.isdigit():
		print("Número da conta inválido. Deve conter apenas números.")
		return False
	numero_conta = int(numero_conta)
	for conta in contas:
		if conta["numero"] == numero_conta and conta["usuario"] == nome:
			return True
	if numero_conta != 0:
		print("Conta não encontrada ou não pertence ao usuário.")
	return False

def criar_conta(nome, contas, dados_contas, agencia):
	numero_conta = len(contas) + 1
	conta = {
		"agencia": agencia,
		"numero": numero_conta,
		"usuario": nome
	}
	contas.append(conta)
	dodos_nova_conta = {
		"numero": numero_conta,
		"saldo": 0.0,
		"extrato": "",
		"saques_realizados": 0
	}
	dados_contas.append(dodos_nova_conta)
	print(f"Conta criada com sucesso!")

def listar_contas(nome, contas):
	contas_user = [conta for conta in contas if conta["usuario"] == nome]
	print("\n================ CONTAS ================")
	print("|                                      |")
	for conta in contas_user:
		if conta["usuario"] == nome:
			print("|   " + f"AGENCIA: {conta["agencia"]}".ljust(35) + "|")
			print("|   " + f"CONTA: {conta["numero"]}".ljust(35) + "|")
			print("|   " + f"USUARIO: {conta["usuario"]}".ljust(35) + "|")
			print("|                                      |")
	if not contas_user:
		print("|       Não foram criadas contas       |")
		print("|          para este usuario.          |")
		print("|                                      |")
	print("========================================")

def perfil_usuario(user, contas, dados_contas):
	LIMITE_DIARIO_SAQUE = 3
	AGENCIA = "0001"
	limite_valor_saque = 500

	while (True):
		cmd = input(menu("main")).strip()
		if cmd == "0":
			break
		elif cmd == "1":
			conta = input("\nDigite o número da conta para o deposito: ").strip()
			if validar_conta(user["nome"], conta, contas):
				conta = int(conta)
			else:
				continue
			saldo, extrato = depositar(saldo=dados_contas[conta - 1]["saldo"], extrato=dados_contas[conta - 1]["extrato"])
			dados_contas[conta - 1]["saldo"] = saldo
			dados_contas[conta - 1]["extrato"] = extrato
		elif cmd == "2":
			conta = input("\nDigite o número da conta para o saque: ").strip()
			if validar_conta(user["nome"], conta, contas):
				conta = int(conta)
			else:
				continue
			saldo, saques_realizados, extrato = sacar(
				saldo=dados_contas[conta - 1]["saldo"],
				saques_realizados=dados_contas[conta - 1]["saques_realizados"],
				extrato=dados_contas[conta - 1]["extrato"],
				limite_valor_saque=limite_valor_saque,
				limite_diario_saque=LIMITE_DIARIO_SAQUE
			)
			dados_contas[conta - 1]["saldo"] = saldo
			dados_contas[conta - 1]["saques_realizados"] = saques_realizados
			dados_contas[conta - 1]["extrato"] = extrato
		elif cmd == "3":
			conta = input("\nDigite o número da conta, ou digite \"0\" para ver o extrato de todas as contas: ").strip()
			if validar_conta(user["nome"], conta, contas) or conta == "0":
				conta = int(conta)
			else:
				continue
			if conta == 0:
				contas_user = [conta["numero"] for conta in contas if conta["usuario"] == user["nome"]]
				for conta_info in dados_contas:
					if conta_info["numero"] in contas_user:
						visualizar_extrato(conta_info["saldo"], conta_info["numero"], extrato_text=conta_info["extrato"])
			else:
				visualizar_extrato(dados_contas[conta - 1]["saldo"], dados_contas[conta - 1]["numero"], extrato_text=dados_contas[conta - 1]["extrato"])
		elif cmd == "4":
			criar_conta(user["nome"], contas, dados_contas, AGENCIA)
		elif cmd == "5":
			listar_contas(user["nome"], contas)
		else:
			print("Operação inválida, por favor selecione novamente.")

def novo_user(users):
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
		if user["cpf"] == cpf:
			print("\nUsuário já cadastrado com esse CPF.")
			return
	endereco = input("Digite o endereço do usuário (formato: Logradouro, Número - Bairro - Cidade/UF): ").strip()
	if not endereco:
		print("\nTodos os campos são obrigatórios.")
		return
	new_user = {
		"nome": nome,
		"nascimento": nascimento,
		"cpf": cpf,
		"endereco": endereco
	}
	users.append(new_user)
	print("\nUsuário cadastrado com sucesso!")

def main():
	users = []
	contas = []
	# List adicionada para armazenar informarções especificas de cada conta, sem ir contra o enuciado do exercicio
	dados_contas = []

	while (True):
		cmd = input(menu("welcome"))
		if cmd == "0":
			break
		elif cmd == "1":
			print("Digite o CPF do usuário. Não inclua espaços, pontos ou traços no CPF.\n")
			login = input("=> ").strip()
			for user in users:
				if login == user["cpf"]:
					print(f"\nBem vindo/a, {user["nome"]}!")
					perfil_usuario(user, contas, dados_contas)
					break
			else:
				print("Usuário não encontrado. Por favor, tente novamente.")
		elif cmd == "2":
			novo_user(users)
		else:
			print("Operação inválida, por favor selecione novamente.")

main()