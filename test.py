import functools
from datetime import datetime

def log_transacao(func):
	@functools.wraps(func)
	def envelope():
		tipo = func.__name__
		data = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		func()
		print(f"{data} {tipo}")

	return envelope

@log_transacao
def deposito():
	pass

deposito()