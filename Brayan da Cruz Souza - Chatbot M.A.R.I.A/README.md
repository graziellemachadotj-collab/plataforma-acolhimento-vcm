# M.A.R.I.A.
**Módulo de Acolhimento, Respeito e Informação à Assistida**

Assistente virtual de acolhimento para mulheres em situação de violência doméstica e outras formas de violência contra a mulher. O nome é uma homenagem à Lei Maria da Penha (Lei 11.340/2006).

> **Em perigo agora, ligue 190. Para orientação gratuita, sigilosa e 24h, ligue 180.**

---

## Sobre o projeto

A M.A.R.I.A. escuta, ajuda a mulher a entender o que está vivendo e mostra caminhos de ajuda, sempre no tempo e do jeito dela. Ela **não substitui** atendimento psicológico, jurídico, policial ou médico, e **não faz diagnóstico**.

### O que ela faz

- Acolhe sem julgar, em linguagem simples e com mensagens curtas.
- Explica os seis tipos de violência reconhecidos pela lei: física, psicológica, sexual, patrimonial, moral e vicária.
- Faz 12 perguntas de identificação, uma por vez, que podem ser puladas.
- Identifica sinais de alto risco e aciona o protocolo de emergência.
- Informa telefones de ajuda rápida (180, 190, 192, 100 e 188).
- Ajuda a localizar serviços de apoio pela cidade e pelo estado, com permissão da usuária.
- Orienta sobre plano de segurança, como contar para a rede de apoio, como denunciar e o passo a passo para sair de uma relação com violência.

### Princípios de acolhimento

1. **Segurança primeiro.** Perigo imediato sempre vem antes de qualquer etapa.
2. **Não revitimizar.** Não pede provas, não duvida do relato e não exige detalhes do trauma.
3. **Não pressionar a separação.** O período da separação é o de maior risco. A decisão é da mulher, e a M.A.R.I.A. ajuda com informação e plano de segurança, seja qual for a escolha.
4. **Autonomia.** Oferece opções, nunca ordens. Cada assunto é oferecido com permissão ("Sim, pode ser", "Agora não", "Prefiro só conversar").
5. **Presença contínua.** A conversa é aberta, sem menu fixo, e a M.A.R.I.A. pergunta como a usuária está se sentindo ao fim de cada assunto.
6. **Privacidade.** Não pede nome completo, CPF, endereço exato nem dados do agressor.
7. **Nunca inventar informação.** Telefones, endereços e serviços só aparecem se forem confirmados.

---

## Versões incluídas

| Versão | Arquivos | Quando usar |
|---|---|---|
| **Autônoma (recomendada)** | `maria.html` | Funciona sozinha, offline, sem servidor, sem conta e sem custo. As respostas seguem um roteiro próprio e são sempre as mesmas. |
| **Com IA e busca na internet** | `maria-interface.html`, `server.js`, `maria-prompt.txt` | Conversa mais livre, com busca de serviços locais em fontes oficiais. Exige servidor, chave de API e cuidados extras. |

O prompt completo da versão com IA fica em `maria-prompt.txt`.

---

## Como usar

### Versão autônoma

1. Baixe o arquivo `maria.html`.
2. Abra no navegador com duplo clique, ou publique em qualquer hospedagem de páginas estáticas.

Não há instalação nem dependências. Para publicar, use **HTTPS**.

### Versão com IA

Requisitos: Node.js 18 ou superior e uma chave de API da Anthropic.

```bash
# 1. Coloque na mesma pasta: server.js, maria-interface.html e maria-prompt.txt
# 2. Rode o servidor
ANTHROPIC_API_KEY=sua_chave node server.js
# 3. Abra no navegador
http://localhost:3000
```

Variáveis opcionais:

| Variável | Função | Padrão |
|---|---|---|
| `PORT` | Porta do servidor | `3000` |
| `MARIA_MODEL` | Modelo usado | `claude-sonnet-5-5` |

> A chave da API fica apenas no servidor. Nunca a coloque dentro do HTML.

---

## Segurança e privacidade

O agressor pode vigiar o aparelho da vítima. Por isso a interface inclui:

- **Aviso de privacidade** antes da conversa, em linguagem simples.
- **Botão vermelho "Sair agora"** (ou tecla `Esc` pressionada duas vezes): apaga a conversa da tela, abre um site neutro e troca a aba atual.
- **Título de aba neutro** ("Receitas e Bem-estar"), para não revelar o assunto a quem olhar a tela. Altere no `<title>` se desejar.
- **Nada salvo no navegador:** a conversa existe só em memória e some ao fechar a página.
- **Sem rastreadores, contas ou fontes externas** na versão autônoma.
- **Barra fixa com 190 e 180** sempre visível.

**Limitações importantes**

- Nenhuma página consegue apagar o histórico do navegador. O aviso orienta usar aba anônima ou um aparelho de confiança.
- Ao tocar em um link de busca de locais, o celular abre o Google Maps com a cidade informada.
- O servidor da versão com IA registra apenas erros técnicos, nunca o conteúdo das mensagens. Antes de publicar na internet, é preciso adicionar limite de requisições por pessoa.

---

## Estrutura do projeto

```
.
├── README.md
├── maria.html              # versão autônoma (roteiro próprio)
├── maria-interface.html    # interface da versão com IA
├── server.js               # servidor da versão com IA
└── maria-prompt.txt        # prompt completo da versão com IA
```

### Como editar o conteúdo (versão autônoma)

Todos os textos ficam no início do `<script>` de `maria.html`, em blocos de dados:

| Bloco | O que contém |
|---|---|
| `T` | Os seis tipos de violência |
| `Q` | As 12 perguntas de identificação, com marcação de risco |
| `N` | Telas e mensagens (telefones, plano de segurança, denúncia, etc.) |
| `SAIR` | Passo a passo para sair da relação |
| `ACK`, `FOLLOW`, `SOFT` | Frases de acolhimento e convites para continuar a conversa |
| `OFFER` e `ORDER` | Ofertas de assunto e a ordem em que são feitas |
| `SUIC`, `EMERG`, `SPECIAL` | Palavras-chave que acionam emergência e atalhos |

É possível mudar uma frase ou uma pergunta sem mexer na lógica.

---

## Telefones de ajuda

| Número | Serviço |
|---|---|
| **180** | Central de Atendimento à Mulher (24h, gratuito, sigiloso) |
| **190** | Polícia Militar (emergência) |
| **192** | SAMU |
| **100** | Disque Direitos Humanos |
| **188** | CVV, apoio emocional 24h |

O número de WhatsApp do 180 não está fixo no código. Confirme-o no site oficial do governo antes de divulgar.

---

## Limitações conhecidas

- A versão autônoma reconhece apenas as palavras-chave programadas. Frases fora do esperado recebem acolhimento genérico, sem perder o contato.
- Ela não confirma endereços nem horários de serviços. Orienta a confirmar pelo 180.
- A versão com IA depende de serviço externo e pode errar. A regra de nunca inventar dados reduz esse risco, mas não o elimina.
- Os prazos legais citados (medida protetiva decidida em até 48 horas e prevenção após violência sexual em até 72 horas) devem ser revisados periodicamente.

---

## Antes de publicar

- [ ] Revisão dos textos por psicólogas, assistentes sociais e advogadas da rede de atendimento à mulher.
- [ ] Teste de cenários de risco: ameaça de morte, ideação suicida e uso do chat pelo próprio agressor.
- [ ] Teste em celulares e computadores, com diferentes navegadores.
- [ ] Hospedagem com HTTPS.
- [ ] Limite de requisições e monitoramento de erros (versão com IA).
- [ ] Revisão de telefones, leis e prazos.

---

## Contribuição

Sugestões são bem-vindas, principalmente de profissionais da rede de proteção à mulher. Abra uma *issue* ou envie um *pull request* descrevendo a mudança e o motivo. Alterações que mexam no protocolo de emergência ou nos princípios de acolhimento devem ser revisadas por pelo menos uma profissional da área.

## Aviso legal

Este projeto tem caráter informativo e de acolhimento. Não presta atendimento psicológico, jurídico, policial ou médico e não substitui a rede de proteção. Em situação de risco, ligue **190**.

## Licença

A definir. *(Escolha a licença antes de publicar o repositório.)*

## Créditos

Criada em homenagem a Maria da Penha Maia Fernandes e à Lei 11.340/2006.
