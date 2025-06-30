menu = """
============ MENU ============
|                            |
|   [1] Depositar            |
|   [2] Sacar                |
|   [3] Vizualizar extrato   |
|   [0] Sair                 |
|                            |
==============================

=> """
saldo = 0.0
vezes_sacadas = 0
limite_valor_saque = 500
LIMITE_DIARIO_SAQUE = 3
extrato = ""

while (True):
	cmd = input(menu)
	if cmd == "0":
		break
	elif cmd == "1":
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
	elif cmd == "2":
		if vezes_sacadas < LIMITE_DIARIO_SAQUE:
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
					vezes_sacadas += 1
					saldo -= saque
					extrato += "\n|" + f"- R${saque:.2f}".rjust(38) + "   |"
					print(f"Saque de R${saque:.2f} realizado com sucesso.")
			except ValueError:
				print("Operação falhou! O valor informado é inválido.")
		else:
			print("Operação falhou! O limite de saques diários foi excedido.")
	elif cmd == "3":
		print("\n================= EXTRATO =================")
		print("|                                         |", end="")
		print("\n|   Não foram realizadas movimentações.   |" if not extrato else extrato)
		print("|" + f"TOTAL: R${saldo:.2f}".rjust(38) + "   |")
		print("|                                         |")
		print("===========================================\n")
	else:
		print("Operação inválida, por favor selecione novamente.")