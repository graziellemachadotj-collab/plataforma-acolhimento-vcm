# Plataforma de Acolhimento, Orientação e Resposta Rápida

**Combate à violência contra a mulher · Projetão IA · OSC AFAGO · turma manhã · 2026**
Orientação: **Prof. Álvaro Machado Júnior**

🌐 **Site:** [acolhimento.prof.alvaromjunior.com](https://acolhimento.prof.alvaromjunior.com)

> 🔒 **Sobre a API:** a API **funciona no site publicado**. Ela roda em um **servidor local seguro, desenvolvido e mantido pelo Prof. Álvaro Machado Júnior**. Por segurança, o endereço e a configuração desse servidor **não** são publicados neste repositório. O código da API está aqui completo e pode ser rodado em qualquer computador (veja abaixo).

> **Em perigo agora, ligue 190.** Central de Atendimento à Mulher: **180** (gratuito, sigiloso, 24h).

---

## O problema

Muitas mulheres em situação de violência não sabem reconhecer os sinais, a quem recorrer nem onde fica o serviço de apoio mais próximo. Elas precisam de uma informação rápida, acolhedora e segura, que não deixe rastro no aparelho.

## A solução

Uma plataforma web que **acolhe, orienta e aponta caminhos**:

- **Tipos de violência e sinais de alerta**, em linguagem simples, de acordo com a Lei Maria da Penha;
- **Autoavaliação de risco** com 12 perguntas, sem salvar respostas;
- **Busca de serviços de apoio por CEP**, ordenados pela distância (Delegacia da Mulher, Defensoria, CRAM, CREAS, saúde e rede de apoio);
- **Chatbot de acolhimento (M.A.R.I.A.)**, com prompt pensado para segurança e privacidade;
- **Saída rápida**: um botão (ou Esc duas vezes) troca a página na hora por uma busca comum.

## Tecnologias

| Camada | Tecnologias |
|---|---|
| Front-End | HTML5, CSS3, JavaScript, layout responsivo, animações ao rolar |
| Back-End | Python, FastAPI, Pydantic, Uvicorn |
| Banco de dados | SQLAlchemy 2, SQLite (desenvolvimento), PostgreSQL + PostGIS (produção) |
| Segurança | Hash scrypt para senhas, cifra Fernet para contatos e relatos, SHA-256 para integridade, CORS restrito, limite de pedidos, cabeçalhos de segurança |
| Qualidade | Pytest: 20 testes automatizados |
| IA | Engenharia de prompt para o chatbot de acolhimento |
| Publicação | GitHub, Cloudflare Pages (site) e servidor local seguro (API), mantido pelo Prof. Álvaro Machado Júnior |

## Estrutura do repositório

| Pasta / arquivo | O que é |
|---|---|
| `index.html`, `css/`, `js/`, `img/` | Site principal |
| `Dayene Souza - …/backend_api` | API: rotas, consultas por distância, autoavaliação e CEP |
| `Jessica Paola - …/backend_banco` | Banco de dados: modelos, cifra, schema PostGIS e dados iniciais |
| `Grazielle … /rede-de-apoio-protecao` | Apresentação web interativa (HTML, CSS e JavaScript separados) |
| `Brayan …`, `Priscila …` | Chatbot: prompts, fluxos e apresentações |
| `Solafago (Solange …)` | Série fotográfica e material sobre os tipos de violência |
| `Miguel …` | Proposta de MVP, organograma e esqueleto original do site |
| `Helloa …`, `Talita …` | README da equipe e documentação |

## Como rodar a API no computador

Pré-requisito: Python 3.10 ou mais novo.

```bash
cd "Dayene Souza - Back-End e Defesa Técnica"
pip install -r requirements.txt
python rodar.py            # abre http://localhost:8000/docs
python -m pytest -q        # testes
```

No Windows também dá para usar dois cliques em `rodar.bat`. Mais detalhes estão nos LEIA-ME da pasta da Dayene e da pasta da Jessica.

## Status e próximos passos

| Item | Status |
|---|---|
| Site responsivo publicado | ✅ Concluído |
| API com rotas públicas e protegidas, testes automatizados | ✅ Concluído |
| API funcionando no site, em servidor local seguro do Prof. Álvaro Machado Júnior | ✅ Em operação |
| Banco com PostGIS e criptografia | ✅ Concluído |
| Prompt e fluxos do chatbot | ✅ Concluído |
| Migração da API para hospedagem definitiva na nuvem | 🚧 Em finalização |
| Cadastro dos serviços reais, conferidos em fonte oficial | 🔜 Próxima etapa |
| Envio automático do alerta (SMS ou e-mail) e revisão por profissionais da rede de proteção | 🔜 Próxima etapa |

> Os serviços cadastrados na API são **exemplos didáticos**, sem telefone e sem endereço.

## Equipe

| Integrante | Área | Responsabilidade principal |
|---|---|---|
| Álvaro Machado Júnior | Orientação | Orientação técnica, gestão da equipe e integração do produto |
| Dayene Souza Silva | Back-End | Estrutura do back-end e consultas de dados |
| Jessica Paola Miranda Vitorino | Back-End | Arquitetura do banco de dados |
| Miguel Felipi da Silva | Front-End | Interfaces responsivas e proposta de MVP |
| Grazielle de Lima Oliveira Machado | Front-End | Estilos (CSS) e interatividade (JavaScript) |
| Priscila Rodrigues | Chatbot | Lógica e estrutura do chatbot |
| Brayan da Cruz Souza | Chatbot | Chatbot M.A.R.I.A.: prompt e automação de fluxos |
| Lavinia Rodrigues Vieira | Chatbot | Funcionalidades inteligentes e experiência da usuária |
| Julia Maria Morais Cardoso | Imagens | Criação e curadoria do conteúdo visual |
| Solange Maria Morais | Imagens | Processamento e tratamento das imagens |
| Helloa Sousa Monteiro | Documentação | Documentação técnica e repositório |
| Talita Monteiro dos Santos | Documentação | Guias técnicos e registro das funcionalidades |

### Como o projeto foi conduzido

A turma trabalhou como uma equipe de produto, dividida em cinco frentes, e cada integrante ficou com uma entrega clara. As entregas foram feitas pelo Google Classroom. O orientador acompanhou cada frente, ajudou a resolver os bloqueios e integrou as partes em um produto único, versionado no GitHub e publicado na internet. Além da técnica, a equipe trabalhou **colaboração, comunicação e responsabilidade**, e tratou **privacidade e ética** como requisitos do sistema.

## Privacidade

- Nenhum telefone ou contato pessoal da equipe é publicado neste repositório.
- A API não registra IP, navegador nem conteúdo, e o CEP pesquisado não é salvo.
- Banco local, chaves de criptografia e ambientes virtuais ficam fora do repositório (`.gitignore`).

---

Projeto acadêmico, sem fins lucrativos, desenvolvido na OSC AFAGO.
