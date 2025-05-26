# Sistema Bancário 🏦

Um projeto de terminal em Python que simula um sistema bancário funcional, com suporte a múltiplos usuários, autenticação segura e operações típicas de um banco — como saques, depósitos, transferências e rendimentos.

## 🚀 Objetivo

Este projeto foi criado com o intuito de:
- Aprimorar habilidades em **Programação Orientada a Objetos**
- Praticar a organização de **módulos Python**
- Trabalhar com **persistência de dados** usando JSON
- Simular, de forma simples e funcional, a estrutura lógica de um **banco digital**

---

## 📦 Funcionalidades

- [x] Cadastro de usuários com CPF único  
- [x] Autenticação com senha criptografada (hash + salt)  
- [x] Contas digitais com métodos bancários (depósito, saque, transferência, etc)
- [x] Sistema de persistência de dados com JSON  
- [x] Arquitetura modular para escalabilidade futura  
- [ ] Sistema de **logs** por usuário (em desenvolvimento)  
- [ ] Aplicação automática de **rendimentos** em contas digitais  

---

## 📂 Estrutura do Projeto

Sistema-Bancario/

│

├── main.py # Arquivo principal para execução do programa

├── auth.py # Módulo responsável pela autenticação (hash de senha e verificação de CPF)

├── account.py # Cadastro e login de usuários

├── user.py # Classe Conta com métodos bancários (em construção)

├── utils.py # Funções auxiliares

├── bank_data/

│ └── users.json # Base de dados local com os usuários cadastrados

└── README.md # Este arquivo
