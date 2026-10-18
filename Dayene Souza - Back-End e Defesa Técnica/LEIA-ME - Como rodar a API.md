# API da Plataforma de Acolhimento — parte da Dayene

**Back-end:** estruturação da API e otimização das consultas (Dayene Souza Silva).
O banco de dados (tabelas, cifra, dados iniciais) está na pasta da **Jessica** (`backend_banco`).
As duas pastas precisam ficar **lado a lado**, como estão agora.

## Como rodar no Windows

1. Instale o **Python 3.10 ou mais novo** em <https://www.python.org/downloads/> e marque **"Add python.exe to PATH"**.
2. Dê dois cliques em **`rodar.bat`** (ou, no Linux/Mac: `pip install -r requirements.txt` e `python rodar.py`).
   - Na primeira vez ele prepara tudo sozinho (leva 1 ou 2 minutos).
3. O navegador abre em **http://localhost:8000/docs**, com todas as rotas para testar.
4. Para parar, aperte **Ctrl + C** na janela preta.

Sem configurar nada, o banco é um arquivo **SQLite** (`plataforma.db`, criado na pasta da Jessica).

### Usar PostgreSQL + PostGIS (versão de produção)

```bat
set DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/plataforma
rodar.bat
```

O banco precisa ter a extensão PostGIS instalada. A coluna `location GEOGRAPHY(Point, 4326)` e o índice GiST são criados sozinhos.

## Modo internet (para quando a API for publicada)

A API já vem preparada para produção. Ligue com `MODO_PUBLICO=1` e informe o site em `SITE_OFICIAL`:
- ficam ligadas só as rotas públicas;
- a API aceita chamadas só do site oficial (CORS);
- cada visitante pode fazer no máximo 60 pedidos por minuto (`LIMITE_POR_MINUTO`), e o identificador dele fica só na memória, como hash.

## Rotas

| Acesso | Método e rota | O que faz |
|---|---|---|
| Público | `GET /api/v1/services/nearby?lat=&lon=&raio_m=&tipo=` | Serviços por distância (mais perto primeiro) |
| Público | `GET /api/v1/services/by-cep?cep=` | CEP → região aproximada → serviços (o CEP **não** é salvo) |
| Público | `GET /api/v1/services/types` | Tipos de serviço (DEAM, Defensoria, CRAM...) |
| Público | `GET /api/v1/red-flags/questions` | 12 perguntas de sinais de alerta |
| Público | `POST /api/v1/red-flags/evaluate` | Avalia as respostas **sem salvar** |
| Público | `GET /api/v1/support/contacts` | 190, 180, 192, 100, 188 |
| Público | `POST /api/v1/quick-escape` | Encerra a sessão e limpa dados do site |
| Protegido | `POST /api/v1/auth/register` · `login` · `logout` | Conta opcional (apelido + senha) |
| Protegido | `DELETE /api/v1/auth/account` | Exclui a conta e todos os dados |
| Protegido | `POST/GET/DELETE /api/v1/trusted-contacts` | Contatos de confiança (cifrados) |
| Protegido | `POST/GET/DELETE /api/v1/evidence` | Diário de evidências (cifrado + hash de integridade) |
| Protegido | `POST /api/v1/emergency-alerts` | Alerta consentido com localização **aproximada** |

Nas rotas protegidas, mande o token do login no cabeçalho `Authorization: Bearer <token>`.
Em `/docs`, clique em **Authorize**.

## Como a consulta é otimizada (`consultas.py`)

- **No PostgreSQL:** `ST_DWithin` filtra pelo raio usando o índice GiST, e `ST_Distance` calcula a distância real em metros. O resultado vem ordenado por distância.
- **No SQLite:**
  1. primeiro um filtro barato por uma "caixa" de latitude/longitude em volta do ponto;
  2. depois a fórmula de Haversine, só nos serviços que sobraram.

## Privacidade

- **Logs:** nenhum IP, navegador ou conteúdo é registrado (o log de acesso está desligado).
- **Cabeçalhos de segurança:** `nosniff`, `no-referrer`, `DENY` e `no-store`.
- **Senhas e tokens:**
  - a senha é guardada só como hash scrypt;
  - o token, só como hash SHA-256;
  - o login errado dá a mesma mensagem, exista o apelido ou não.
- **Contatos e relatos:** são cifrados, e a chave fica fora do banco.
- **Alerta:** a localização é arredondada para cerca de 1 km.

## Testes

```bat
.venv\Scripts\python.exe -m pytest -q
```

São 16 testes, que passam com SQLite e com PostgreSQL + PostGIS.

## Limites desta versão (próximas etapas)

- **Serviços:** os cadastrados são **exemplos didáticos**, sem telefone e sem endereço. Antes de publicar, troque pelos serviços reais conferidos em fonte oficial.
- **CEP:** sem internet, a busca por CEP cobre a Grande São Paulo. Para o Brasil todo, ligue um serviço oficial de geocodificação em `cep.py`.
- **Alerta:** ele monta a mensagem e a lista de contatos, mas ainda **não envia** SMS ou e-mail sozinho.
- **Publicação da API (em finalização):** hospedagem definitiva com HTTPS e revisão dos textos por profissionais da rede de proteção.
