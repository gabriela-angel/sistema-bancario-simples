# 🏦 Sistema Bancário em Python

Este é um projeto de sistema bancário desenvolvido em Python, utilizando os princípios de **Programação Orientada a Objetos (POO)**. O sistema permite o gerenciamento de usuários, contas bancárias, operações financeiras e exibição de extratos de maneira estruturada e modular, com persistência de dados em arquivos CSV.

## 🧠 Sobre o Projeto

O sistema simula um banco simples com menu interativo, usando princípios de **POO** e mecanismos modernos do Python:

- Criação e herança de classes
- Encapsulamento de atributos
- Composição entre objetos (Cliente → Conta → Transações)
- Uso de classes abstratas
- Métodos de classe e propriedades
- **Decorador** para log de transações
- **Iterador** para listar contas de forma eficiente
- **Gerador** para filtrar transações no extrato
- **Persistência**: usuários, contas e transações são gravados e carregados via CSV

## ⚙️ Funcionalidades

- 👤 Criar novo usuário (CPF, nome, data de nascimento e endereço)
- 🔐 Fazer login via CPF
- 🏦 Criar múltiplas contas bancárias por usuário
- 💸 Realizar depósitos e saques em contas específicas
- 📃 Visualizar extrato de uma conta ou de todas as contas do usuário
- 📂 Listar todas as contas associadas ao usuário logado

## 📋 Regras de Negócio

- Cada usuário (CPF) pode ter **várias contas bancárias**.
- O limite de transações por conta é de **10 transações diárias**.
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
git clone https://github.com/gabriela-angel/sistema-bancario-simples.git
cd sistema-bancario-simples
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
- Decoradores para log de transações, aplicando a funcionalidade de forma transparente
- Iteradores para facilitar a exibição das contas de um cliente de maneira eficiente
- Geradores para filtrar transações ao exibir extratos, permitindo um uso mais eficiente da memória

## 🧼 Organização e Boas Práticas

- Código modular e separado por responsabilidades
- Utilização de `try/except` para tratar entradas inválidas
- Métodos como `__repr()__` e `__str__()` personalizados para impressão amigável
- Persistência simples via CSV, com consistência entre execuções

---

> **Observação:** Para reiniciar os dados, basta remover os arquivos usuarios.csv, contas.csv, transacoes.csv e log.txt. O sistema irá recriá-los na próxima execução.