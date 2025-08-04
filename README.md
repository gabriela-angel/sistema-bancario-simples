# 💰 Sistema Bancário em Python

Este é um projeto de sistema bancário simples feito em Python, com funcionalidades para criação de usuários, múltiplas contas por usuário, saques, depósitos e visualização de extrato bancário.

## 🧠 Sobre o Projeto

O sistema simula operações bancárias comuns com um menu interativo via terminal. O projeto foi criado com fins educacionais e visa praticar os fundamentos de programação em Python, como:

- Estruturas condicionais
- Funções com parâmetros nomeados e posicionais
- Estruturas de dados (listas e dicionários)
- Modularização e organização de código

## ⚙️ Funcionalidades

- 📌 Criar novo usuário (com CPF, nome, nascimento e endereço)
- 🧾 Entrar no sistema com CPF
- 🏦 Criar novas contas bancárias
- 💸 Realizar depósitos e saques
- 📃 Visualizar extrato individual ou de todas as contas do usuário
- 🗂️ Listar todas as contas associadas a um usuário

## 📋 Regras de Negócio

- Cada CPF pode ter **várias contas bancárias**, mas um CPF não pode se repetir entre usuários.
- O limite de saques diários por conta é de **3 saques**.
- O valor máximo por saque é de **R$ 500,00**.
- O extrato mostra os lançamentos realizados e o saldo total.

## 💻 Como Executar

1. Certifique-se de ter o Python 3 instalado.
2. Clone este repositório:

```bash
git clone https://github.com/gabriela-angel/sistema-bancario-simples-otimizado.git
cd sistema-bancario-simples-otimizado
```

3. Execute o script:

```bash
python3 banco.py
```

## 🧪 Exemplo de Uso

```text
========= BEM VINDO! =========
|                            |
|   [1] Entrar               |
|   [2] Criar usuario        |
|   [0] Sair                 |
|                            |
==============================

=> 
```

Após o login, o usuário pode acessar o menu principal com todas as operações bancárias disponíveis.

## 🧼 Organização do Código

- Funções puras com tratamento de erros via `try/except`
- Separação clara de responsabilidades:
  - `menu()` → exibição de menus
  - `depositar()`, `sacar()`, `visualizar_extrato()` → operações financeiras
  - `criar_conta()`, `listar_contas()` → gerenciamento de contas
  - `novo_user()` → cadastro de usuários
