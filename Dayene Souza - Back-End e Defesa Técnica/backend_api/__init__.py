"""
Parte da API (back-end) da Plataforma de Acolhimento, Orientação e Resposta Rápida.
Responsável: Dayene Souza Silva (estruturação do back-end e otimização das consultas).

Conteúdo:
  main.py              aplicação FastAPI, segurança dos cabeçalhos, sem logs de IP
  consultas.py         busca de serviços por distância (PostGIS ou cálculo em Python)
  cep.py               CEP -> região aproximada (sem guardar o CEP)
  autoavaliacao.py     perguntas de sinais de alerta e avaliação SEM salvar respostas
  autenticacao.py      login opcional com token
  rotas_publicas.py    rotas sem cadastro
  rotas_protegidas.py  rotas com conta (contatos, diário, alertas)

O banco de dados (tabelas, cifra, dados iniciais) fica na pasta da Jessica: backend_banco.
"""
