# 💰 Sistema Bancário Simples

Este é um sistema bancário simples desenvolvido em **Python**, com interface de linha de comando, que permite ao usuário realizar operações básicas como **depósitos**, **saques** e **visualizar o extrato da conta**.

## 📋 Funcionalidades

🔹 **[1] Depositar**  
Permite adicionar um valor positivo ao saldo da conta.

🔹 **[2] Sacar**  
Permite retirar um valor do saldo, respeitando os seguintes limites:
- Saques de no máximo **R$500** por operação
- Até **3 saques por sessão**

🔹 **[3] Visualizar Extrato**  
Exibe todas as movimentações realizadas, além do saldo atual formatado.

🔹 **[0] Sair**  
Encerra o programa.

---

## 💻 Como Executar

1. Certifique-se de ter o Python 3 instalado.
2. Clone este repositório:

```bash
git clone https://github.com/gabriela-angel/sistema-bancario-simples.git
cd sistema-bancario-simples
```

3. Execute o script:

```bash
python3 banco.py
```

4. Utilize o menu interativo para navegar pelas opções.

---

## 🧪 Exemplo de uso

```text
============ MENU ============
|                            |
|   [1] Depositar            |
|   [2] Sacar                |
|   [3] Visualizar extrato   |
|   [0] Sair                 |
|                            |
==============================

=> 1
Valor a ser depositado: 100
Depósito de R$100.00 realizado com sucesso.

=> 2
Informe o valor do saque: 50
Saque de R$50.00 realizado com sucesso.

=> 3
================= EXTRATO =================
|                                         |
|                           + R$ 100.00   |
|                             - R$50.00   |
|                        TOTAL: R$50.00   |
|                                         |
===========================================
```

---

## 🚫 Restrições

⚠️ Não é possível:
- Depositar ou sacar valores negativos ou nulos
- Sacar mais do que **R$500** por operação
- Realizar mais de **3 saques por sessão**
- Salvar o extrato após encerrar o programa (sem persistência)

---

## 🧑‍💻 Autor

Desenvolvido por **Gabriela Angel** 🧠  
Este projeto é um exercício educacional para treinar estruturas de controle, tratamento de erros e manipulação de strings em Python.
