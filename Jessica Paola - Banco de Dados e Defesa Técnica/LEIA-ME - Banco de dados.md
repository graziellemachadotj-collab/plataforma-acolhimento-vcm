# Banco de dados da Plataforma de Acolhimento — parte da Jessica

**Back-end:** arquitetura do banco de dados e robustez (Jessica Paola Miranda Vitorino).
A API que usa este banco está na pasta da **Dayene** (`backend_api`). Para rodar tudo, use o `rodar.bat` de lá.

## Arquivos

| Arquivo | O que tem |
|---|---|
| `backend_banco/database.py` | Conexão: SQLite (local) ou PostgreSQL + PostGIS (`DATABASE_URL`). Cria tabelas, coluna geográfica e índice GiST |
| `backend_banco/models.py` | As tabelas |
| `backend_banco/seguranca.py` | Senha (scrypt), cifra (Fernet), hash de integridade, localização aproximada |
| `backend_banco/seed.py` | Tipos de serviço, canais oficiais e serviços de **exemplo** |
| `backend_banco/sql/schema_postgis.sql` | O mesmo schema em SQL puro, com a consulta espacial do README |
| `tests/test_banco.py` | 4 testes |

## Tabelas

| Tabela | Conteúdo principal |
|---|---|
| `users` | ID pseudônimo, apelido, senha derivada (scrypt), consentimento, datas |
| `sessions` | Hash do token de login e validade |
| `services` | Nome, tipo, telefone, site, endereço do **serviço**, latitude/longitude, `location` (PostGIS), `exemplo`, `verificado_em` |
| `service_types` | DEAM, Defensoria, CRAM, CREAS, Casa da Mulher Brasileira, saúde, abrigo, ONG, Conselho Tutelar |
| `support_contacts` | 190, 180, 192, 100, 188 |
| `trusted_contacts` | Usuária, nome, canal, **contato cifrado**, consentimento |
| `evidence_entries` | **Relato cifrado**, hash SHA-256 de integridade, tipo de violência, datas |
| `emergency_alerts` | Localização **aproximada** (~1 km), mensagem, quantos contatos |

## Decisões de segurança

1. **O endereço da usuária nunca é guardado.** O CEP é usado só na hora da busca.
2. **Relatos e contatos são cifrados.** A chave fica fora do banco: na variável `CHAVE_DADOS` ou no arquivo `.chave_dados`, criado na primeira execução. Não envie esse arquivo para o GitHub. Quem tiver só o banco não consegue ler nada.
3. **Senha e token só como hash.** Se o banco vazar, não dá para entrar nas contas.
4. **Excluir a conta apaga tudo** (`ON DELETE CASCADE`).
5. **Serviços têm `verificado_em`.** Telefones e endereços mudam, então revise a cada 3 a 6 meses.

## Testes

Na pasta da Dayene, depois de rodar o `rodar.bat` uma vez:

```bat
cd "..\Jessica Paola - Banco de Dados e Defesa Técnica"
"..\Dayene Souza - Back-End e Defesa Técnica\.venv\Scripts\python.exe" -m pytest -q
```
