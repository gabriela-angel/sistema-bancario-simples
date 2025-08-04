# 🏦 Sistema Bancário em Python (POO)

Este é um projeto de sistema bancário desenvolvido em Python, utilizando os princípios de **Programação Orientada a Objetos (POO)**. O sistema permite o gerenciamento de usuários, contas bancárias, operações financeiras e exibição de extratos de maneira estruturada e modular.

## 🧠 Sobre o Projeto

Este sistema simula operações bancárias simples por meio de um menu de terminal interativo. Ele foi desenvolvido com fins educacionais para praticar conceitos fundamentais de POO em Python, como:

- Criação e herança de classes
- Encapsulamento de atributos
- Composição entre objetos (Cliente → Conta → Transações)
- Uso de classes abstratas
- Métodos de classe e propriedades

## ⚙️ Funcionalidades

- 👤 Criar novo usuário (CPF, nome, data de nascimento e endereço)
- 🔐 Fazer login via CPF
- 🏦 Criar múltiplas contas bancárias por usuário
- 💸 Realizar depósitos e saques em contas específicas
- 📃 Visualizar extrato de uma conta ou de todas as contas do usuário
- 📂 Listar todas as contas associadas ao usuário logado

## 📋 Regras de Negócio

- Cada usuário (CPF) pode ter **várias contas bancárias**.
- O limite de saques por conta é de **3 saques diários**.
- Cada saque tem um limite máximo de **R$ 500,00**.
- O extrato mostra todas as movimentações financeiras e o saldo atual da conta.

## 🧾 Exemplo de Uso

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

Após o login, o usuário pode acessar o menu principal com opções para movimentar contas e visualizar extratos.

## 🧪 Executando o Projeto

1. Certifique-se de ter o **Python 3** instalado na sua máquina.
2. Clone este repositório:

```bash
git clone https://github.com/gabriela-angel/sistema-bancario-simples-oop.git
cd sistema-bancario-simples-oop
```

3. Execute o script principal:

```bash
python3 main.py
```

## 🖼️ Diagrama de Classes (UML)

O projeto segue um modelo UML com as seguintes entidades:

```
Cliente (abstract)  ◄──── PessoaFisica
        ▲
        │
      Conta ◄──── ContaCorrente
        │
    Historico
        │
    Transacao (abstract) ◄──── Deposito
                         ◄──── Saque
```

## ✅ Pontos de Aprendizado

- Utilização de composição em vez de herança onde aplicável
- Abstração com classes abstratas (`Transacao`)
- Encapsulamento com propriedades (`@property`)
- Controle de fluxo, validações e tratamento de entrada do usuário

## 🧼 Organização e Boas Práticas

- Código modular e separado por responsabilidades
- Sem uso de variáveis globais
- Utilização de `try/except` para tratar entradas inválidas
- Métodos como `__str__()` personalizados para impressão amigável
