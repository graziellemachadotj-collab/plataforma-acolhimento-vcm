"""
Parte do BANCO DE DADOS da Plataforma de Acolhimento, Orientação e Resposta Rápida.
Responsável: Jessica Paola Miranda Vitorino (arquitetura do banco e robustez).

Conteúdo:
  database.py   conexão (SQLite local ou PostgreSQL + PostGIS) e criação das tabelas
  models.py     tabelas: service_types, services, users, sessions, trusted_contacts,
                evidence_entries, emergency_alerts
  seguranca.py  senha com scrypt, cifra dos dados sensíveis, hash de integridade,
                localização aproximada
  seed.py       tipos de serviço, canais oficiais e serviços de EXEMPLO
  sql/          schema PostgreSQL + PostGIS documentado (índice GiST e consulta espacial)

A API (rotas e consultas) fica na pasta da Dayene: backend_api.
"""
