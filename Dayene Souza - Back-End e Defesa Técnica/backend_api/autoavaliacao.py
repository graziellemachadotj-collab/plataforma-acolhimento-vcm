"""
Autoavaliação de sinais de alerta (rota pública).

- NÃO salva as respostas em lugar nenhum.
- Serve para orientar, não para diagnosticar nem culpar a vítima.
- Perguntas de alto risco acionam a orientação de emergência (190).
"""
PERGUNTAS = [
    {"id": "medo", "texto": "Você sente medo de como essa pessoa vai reagir?", "tipo": "psicologica", "risco": False},
    {"id": "controle", "texto": "Ela controla suas roupas, seu celular, suas redes sociais ou com quem você fala?", "tipo": "psicologica", "risco": False},
    {"id": "isolamento", "texto": "Você foi afastada da sua família ou dos seus amigos?", "tipo": "psicologica", "risco": False},
    {"id": "humilhacao", "texto": "Ela te humilha, xinga ou diminui, em casa ou na frente de outras pessoas?", "tipo": "moral", "risco": False},
    {"id": "dinheiro", "texto": "Ela pega seu dinheiro, cartão ou documentos, ou te impede de trabalhar?", "tipo": "patrimonial", "risco": False},
    {"id": "fisica", "texto": "Ela já te empurrou, bateu, apertou ou machucou de alguma forma?", "tipo": "fisica", "risco": True},
    {"id": "sexual", "texto": "Ela já te forçou a ter relação sexual ou a fazer algo que você não queria?", "tipo": "sexual", "risco": True},
    {"id": "ameaca_morte", "texto": "Ela já ameaçou te matar ou matar alguém próximo?", "tipo": "psicologica", "risco": True},
    {"id": "arma", "texto": "Ela tem acesso a arma de fogo ou já te ameaçou com faca ou outro objeto?", "tipo": "fisica", "risco": True},
    {"id": "piora", "texto": "As agressões estão ficando mais frequentes ou mais graves?", "tipo": "fisica", "risco": True},
    {"id": "filhos", "texto": "Ela usa seus filhos, familiares ou animais para te ameaçar ou controlar?", "tipo": "vicaria", "risco": False},
    {"id": "separacao", "texto": "Você está pensando em se separar ou se separou recentemente?", "tipo": None, "risco": True},
]
POR_ID = {p["id"]: p for p in PERGUNTAS}

NOMES = {"fisica": "física", "psicologica": "psicológica", "sexual": "sexual",
         "patrimonial": "patrimonial", "moral": "moral", "vicaria": "vicária"}


def avaliar(respostas: dict[str, bool]) -> dict:
    sim = [POR_ID[k] for k, v in respostas.items() if v and k in POR_ID]
    tipos = sorted({NOMES[p["tipo"]] for p in sim if p["tipo"]})
    alto_risco = any(p["risco"] for p in sim)

    if alto_risco:
        nivel = "alto"
        mensagem = ("O que você contou mostra sinais de risco. A sua segurança vem primeiro. "
                    "Se estiver em perigo agora, ligue 190. Para orientação sigilosa, ligue 180.")
    elif sim:
        nivel = "atencao"
        mensagem = ("O que você descreve pode ser uma forma de violência. A culpa não é sua, "
                    "e existem caminhos de ajuda. O 180 orienta de forma gratuita e sigilosa.")
    else:
        nivel = "sem_sinais"
        mensagem = ("Pelas respostas, não apareceram sinais de alerta. Se algo mudar ou você "
                    "quiser conversar, o 180 está disponível 24 horas.")

    return {
        "nivel": nivel,
        "formas_identificadas": tipos,
        "mensagem": mensagem,
        "proximos_passos": ["Ligar 190 em perigo imediato", "Ligar 180 para orientação",
                            "Buscar serviços próximos", "Montar um plano de segurança"] if sim else [],
        "aviso": "Esta avaliação não é diagnóstico e as respostas não foram salvas.",
    }
