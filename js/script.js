/* Plataforma de Acolhimento — interatividade do site */
/* ---------- Dados: tipos de violência ---------- */
const TIPOS = [
 {id:'fisica',nome:'Física',lei:'Art. 7º, inciso I',def:'Qualquer conduta que ofenda a integridade ou a saúde do corpo.',ex:['Empurrões, tapas, socos ou chutes','Queimaduras, cortes ou lesões','Impedir a pessoa de sair de casa ou de receber atendimento'],dica:'Lesões podem ser registradas em exame de corpo de delito.'},
 {id:'psico',nome:'Psicológica',lei:'Art. 7º, inciso II',def:'Qualquer conduta que cause dano emocional, diminua a autoestima ou prejudique o pleno desenvolvimento da mulher.',ex:['Humilhação, insultos e xingamentos','Ameaças e chantagem emocional','Controle de roupas, redes sociais e amizades','Isolamento de familiares e amigos'],dica:'Mesmo sem marcas no corpo, esse tipo de violência causa sofrimento real.'},
 {id:'sexual',nome:'Sexual',lei:'Art. 7º, inciso III',def:'Obrigar a presenciar, manter ou participar de relação sexual não desejada, mediante intimidação, ameaça, coação ou uso da força.',ex:['Forçar relação sexual, mesmo no casamento ou namoro','Impedir o uso de métodos contraceptivos','Forçar gravidez, aborto ou prostituição'],dica:'O consentimento precisa ser livre e pode ser retirado a qualquer momento. Atendimento de saúde é um direito.'},
 {id:'patri',nome:'Patrimonial',lei:'Art. 7º, inciso IV',def:'Reter, subtrair ou destruir objetos, documentos, bens, valores ou recursos econômicos.',ex:['Retirar o cartão, o salário ou o dinheiro da mulher','Destruir documentos pessoais ou objetos de uso','Impedir o acesso a bens da família ou ao próprio trabalho'],dica:'Guardar cópias de documentos importantes pode ajudar em caso de necessidade.'},
 {id:'moral',nome:'Moral',lei:'Art. 7º, inciso V',def:'Qualquer conduta que configure calúnia, difamação ou injúria contra a mulher.',ex:['Espalhar mentiras sobre a vida dela (calúnia)','Atribuir fatos ofensivos à reputação (difamação)','Xingar ou ofender a dignidade (injúria)'],dica:'Registrar prints e datas pode ajudar a comprovar a situação.'},
 {id:'vicaria',nome:'Vicária',lei:'Forma grave de violência psicológica',def:'Quando o agressor usa pessoas queridas, como filhos, familiares ou animais, para atingir, controlar ou causar sofrimento à mulher.',ex:['Ameaçar tirar a guarda ou “sumir” com os filhos','Colocar os filhos contra ela ou usá-los como mensageiros','Ameaçar ou ferir animais de estimação ou familiares'],dica:'Se houver risco para crianças: Disque 100, Conselho Tutelar e Defensoria Pública; em urgência, 190.'}
];
const abas = document.getElementById('abas'), painel = document.getElementById('painel');
function mostraTipo(i){
  [...abas.children].forEach((b,j)=>b.setAttribute('aria-selected', j===i));
  const t = TIPOS[i];
  painel.innerHTML = `<div class="painel"><div><span class="lei">${t.lei}</span><h3>Violência ${t.nome.toLowerCase()}</h3><p>${t.def}</p><p style="margin-top:18px;font-weight:600;color:var(--roxo)">${t.dica}</p></div><div class="caixa"><b>Exemplos</b><ul>${t.ex.map(e=>`<li>${e}</li>`).join('')}</ul></div></div>`;
}
TIPOS.forEach((t,i)=>{const b=document.createElement('button');b.role='tab';b.textContent=t.nome;b.onclick=()=>mostraTipo(i);abas.appendChild(b)});
mostraTipo(0);

/* ---------- Demonstração da M.A.R.I.A. ---------- */
const corpo = document.getElementById('chat-corpo'), opcoes = document.getElementById('opcoes');
const ROTEIRO = {
  inicio:{m:['Oi, eu sou a M.A.R.I.A. 💜','Estou aqui para te ouvir, sem julgamentos. Como você está agora?'],o:[['Estou em perigo agora','perigo'],['Quero entender o que estou vivendo','tipos'],['Quero os telefones de ajuda','tel'],['Prefiro só conversar','conversa']]},
  perigo:{m:['Sua segurança vem primeiro.','Se você puder, ligue agora para o 190 (Polícia Militar).\nSe não puder falar, tente ir para um lugar seguro ou peça para alguém de confiança ligar.'],o:[['Ver outros telefones','tel'],['Voltar ao início','inicio']]},
  tipos:{m:['Obrigada por confiar em mim.','A violência pode ser física, psicológica, sexual, patrimonial, moral ou vicária. Uma mesma situação pode ter mais de uma.','Quer que eu te leve para a explicação de cada tipo?'],o:[['Sim, pode ser','ir-orientacao'],['Agora não','conversa']]},
  tel:{m:['Telefones gratuitos:\n190 · Polícia Militar (emergência)\n180 · Central de Atendimento à Mulher (24h, sigiloso)\n192 · SAMU\n100 · Direitos Humanos\n188 · CVV, apoio emocional'],o:[['Como fica minha privacidade?','priv'],['Voltar ao início','inicio']]},
  priv:{m:['Nesta conversa nada é salvo: ela some quando você fecha a página.','O botão rosa “Sair rápido” (ou Esc duas vezes) abre um site neutro na hora. Se puder, use uma aba anônima ou um aparelho de confiança.'],o:[['Voltar ao início','inicio']]},
  conversa:{m:['Tudo bem. A gente pode só conversar, no seu tempo.','Você não tem culpa pelo que está vivendo. Quando quiser, eu posso te mostrar caminhos de ajuda.'],o:[['Quero os telefones de ajuda','tel'],['Voltar ao início','inicio']]}
};
let ocupado=false;
function bolha(txt,cls){const d=document.createElement('div');d.className='msg '+cls;d.textContent=txt;corpo.appendChild(d);corpo.scrollTop=corpo.scrollHeight}
async function passo(id){
  if(id==='ir-orientacao'){document.getElementById('orientacao').scrollIntoView({behavior:'smooth'});return}
  ocupado=true; opcoes.innerHTML='';
  for(const m of ROTEIRO[id].m){
    const t=document.createElement('div');t.className='digitando';t.innerHTML='<i></i><i></i><i></i>';corpo.appendChild(t);corpo.scrollTop=corpo.scrollHeight;
    await new Promise(r=>setTimeout(r,matchMedia('(prefers-reduced-motion: reduce)').matches?0:650));
    t.remove(); bolha(m,'bot');
  }
  ROTEIRO[id].o.forEach(([txt,dest])=>{const b=document.createElement('button');b.textContent=txt;b.onclick=()=>{if(ocupado)return;bolha(txt,'eu');passo(dest)};opcoes.appendChild(b)});
  ocupado=false;
}
let chatIniciado=false;
new IntersectionObserver((es,o)=>{if(es[0].isIntersecting&&!chatIniciado){chatIniciado=true;passo('inicio');o.disconnect()}},{threshold:.3}).observe(document.getElementById('chat'));

/* ---------- Trabalhos dos alunos ---------- */
const P = {
 brayan:'Brayan da Cruz Souza - Chatbot M.A.R.I.A',
 dayene:'Dayene Souza - Back-End e Defesa Técnica',
 jessica:'Jessica Paola - Banco de Dados e Defesa Técnica',
 grazielle:'Grazielle de Lima Oliveira Machado - Rede de Apoio e Proteção',
 miguel:'Miguel Felipi Lima - Front-End e Proposta de MVP',
 priscila:'Priscila Rodrigues - Guia de Acolhimento e Prompt do Chatbot',
 sol:'Solafago (Solange Maria Morais) - Imagens e Tipos de Violência',
 talita:'Talita Monteiro - README da Equipe',
 helloa:'Helloa Sousa - Documentação'
};
const TRABALHOS = [
 {k:'brayan',nome:'Brayan da Cruz Souza',area:'Chatbot',titulo:'M.A.R.I.A. — assistente de acolhimento',desc:'Prompt completo da M.A.R.I.A., apresentação do chatbot e README com princípios de acolhimento, segurança e privacidade.',ok:true,arq:['MARIA-acolhimento-para-quem-precisa-de-ajuda.pptx','Prompt Chat Bot M.A.R.I.A..docx','README.md']},
 {k:'dayene',nome:'Dayene Souza Silva',area:'Back-End',titulo:'Defesa técnica do back-end',desc:'Arquitetura com FastAPI, PostgreSQL e PostGIS, endpoints públicos e protegidos e privacidade por concepção. Trabalho em dupla com Jessica.',ok:true,arq:['PP_Plataforma-de-Acolhimento-Orientacao-e-Resposta-Rapida.pptx','Readme.pdf']},
 {k:'jessica',nome:'Jessica Paola Miranda Vitorino',area:'Back-End',titulo:'Banco de dados e defesa técnica',desc:'Modelagem do banco (users, services, trusted_contacts, evidence_entries) e consultas espaciais. Trabalho em dupla com Dayene.',ok:true,arq:['PP_Plataforma-de-Acolhimento-Orientacao-e-Resposta-Rapida.pptx','Readme.pdf']},
 {k:'grazielle',nome:'Grazielle de Lima Oliveira Machado',area:'Front-End · CSS e JavaScript',titulo:'Rede de Apoio e Proteção',desc:'Estilos (CSS) e interatividade (JavaScript) da plataforma. Apresentação interativa com slides e gráficos (ECharts), organizada em HTML, CSS e JS, mais README de organização do projeto em grupo.',ok:true,arq:['Rede de Apoio e Proteção curso de inteligencia artificial.html','README_Rede_de_Apoio_e_Protecao.docx']},
 {k:'miguel',nome:'Miguel Felipi da Silva',area:'Front-End',titulo:'Proposta de MVP e organograma',desc:'Visão do produto, organograma das seis frentes e proposta de modelo de dados para o front-end; esqueleto original deste site.',ok:true,arq:['Plataforma-de-acolhimento-e-resposta-rapida.pptx','index-2.html']},
 {k:'priscila',nome:'Priscila Rodrigues',area:'Chatbot',titulo:'Guia de acolhimento e prompt do chatbot',desc:'Apresentação “Acolhimento e Orientação para Mulheres” e ajustes do prompt: violência vicária e busca de serviços por CEP.',ok:true,arq:['acolhimento-orientacao-mulheres.pptx','Prompt - VCM.docx']},
 {k:'sol',nome:'Solange Maria Morais (Solafago)',area:'Imagens',titulo:'Série fotográfica e tipos de violência',desc:'Quatro imagens em formatos diferentes (usadas neste site), README do material visual e apresentação educativa sobre a Lei Maria da Penha.',ok:true,arq:['Como-a-equipe-transforma-dados-em-acolhimento.pptx','README SOL.docx','FOTO 1.jpg','FOTO 2.jpg','FOTO 3.jpg','FOTO 4.jpeg']},
 {k:'talita',nome:'Talita Monteiro dos Santos',area:'Documentação',titulo:'README da equipe',desc:'Documento que apresenta cada integrante e o que ficou sob sua responsabilidade no projeto. Trabalho em dupla com Helloa.',ok:true,arq:['README_Combate a Violencia Contra a Mulher_Projeto Afago.docx']},
 {k:'helloa',nome:'Helloa Sousa Monteiro',area:'Documentação',titulo:'README da equipe',desc:'Documento que apresenta cada integrante e o que ficou sob sua responsabilidade no projeto. Trabalho em dupla com Talita.',ok:true,arq:['README_Combate a Violencia Contra a Mulher_Projeto Afago.docx']}
];
const lt = document.getElementById('lista-trabalhos');
const ext = f => (f.split('.').pop()||'').toLowerCase().replace('jpeg','jpg');
const enc = s => s.split('/').map(encodeURIComponent).join('/');
TRABALHOS.forEach((t,i)=>{
  const ini=t.nome.split(' ').filter(w=>w.length>2).map(w=>w[0]).slice(0,2).join('').toUpperCase();
  const el=document.createElement('article');el.className='trab rev'+(i%3?' rev-d'+(i%3):'');
  el.innerHTML=`<div class="topo-t"><span class="ini">${ini}</span><div><span class="area">${t.area}</span><h3>${t.nome}</h3></div></div>
  <div><span class="estado ${t.ok?'':'pend'}">${t.ok?'Entregue':'Pendente no Classroom'}</span></div>
  <p><b style="color:var(--txt)">${t.titulo}.</b> ${t.desc}</p>
  <ul class="arqs">${t.arq.map(f=>`<li><a href="${enc(P[t.k]+'/'+f)}" target="_blank" rel="noopener"><span class="tipo ${ext(f)}">${ext(f).toUpperCase()}</span>${f}</a></li>`).join('')||'<li style="font-size:.88rem;color:var(--mut)">Sem arquivos enviados.</li>'}</ul>`;
  lt.appendChild(el);
});

/* ---------- Equipe ---------- */
const EQUIPE = [
 ['orientacao','Orientação','Álvaro Machado Júnior','Professor orientador, especialista em Inteligência Artificial e Aprendizagem Interativa.'],
 ['backend','Back-End','Dayene Souza Silva','Estruturação do back-end e otimização das consultas de dados.'],
 ['backend','Back-End','Jessica Paola Miranda Vitorino','Arquitetura do banco de dados e robustez das funcionalidades.'],
 ['frontend','Front-End','Miguel Felipi da Silva','Interfaces responsivas focadas na melhor experiência da usuária.'],
 ['frontend','Front-End','Grazielle de Lima Oliveira Machado','Estilos (CSS) e interatividade (JavaScript) da plataforma.'],
 ['chatbot','Chatbot','Priscila Rodrigues','Lógica e estruturação do chatbot de apoio.'],
 ['chatbot','Chatbot','Brayan da Cruz Souza','Automação de fluxos e integração do suporte técnico do chatbot.'],
 ['chatbot','Chatbot','Lavinia Rodrigues Vieira','Funcionalidades inteligentes e experiência da usuária no chatbot.'],
 ['imagens','Imagens','Julia Maria Morais Cardoso','Criação, geração e curadoria do conteúdo visual.'],
 ['imagens','Imagens','Solange Maria Morais','Processamento e tratamento das imagens nos formatos de cada uso.'],
 ['readme','Readme','Helloa Sousa Monteiro','Documentação técnica e organização do repositório.'],
 ['readme','Readme','Talita Monteiro dos Santos','Guias técnicos e registro detalhado das funcionalidades.']
];
const le=document.getElementById('lista-equipe'), fi=document.getElementById('filtros');
EQUIPE.forEach(([a,f,n,d])=>{
  const ini=(n.split(' ')[0][0]+n.split(' ').slice(-1)[0][0]).toUpperCase();
  const el=document.createElement('article');el.className='membro';el.dataset.area=a;
  el.innerHTML=`<span class="avatar" aria-hidden="true">${ini}</span><div><span class="funcao">${f}</span><h3>${n}</h3><p>${d}</p></div>`;le.appendChild(el);
});
[['todos','Todos'],['orientacao','Orientação'],['backend','Back-End'],['frontend','Front-End'],['chatbot','Chatbot'],['imagens','Imagens'],['readme','Readme']].forEach(([k,r],i)=>{
  const b=document.createElement('button');b.textContent=r;if(!i)b.className='on';
  b.onclick=()=>{[...fi.children].forEach(x=>x.classList.remove('on'));b.classList.add('on');[...le.children].forEach(m=>m.classList.toggle('oculto',k!=='todos'&&m.dataset.area!==k))};
  fi.appendChild(b);
});

/* ---------- Interações gerais ---------- */
document.getElementById('ano').textContent=new Date().getFullYear();
const sair=()=>window.location.replace('https://www.google.com/search?q=previs%C3%A3o+do+tempo');
document.getElementById('saida').onclick=sair;
let ultEsc=0;
const luz=document.getElementById('luz');
document.addEventListener('keydown',e=>{if(e.key!=='Escape')return; if(luz.classList.contains('aberta')){luz.classList.remove('aberta');return} const t=Date.now(); if(t-ultEsc<800)sair(); ultEsc=t;});
const menu=document.getElementById('menu'),burger=document.getElementById('burger');
burger.onclick=()=>{menu.classList.toggle('aberto');burger.setAttribute('aria-expanded',menu.classList.contains('aberto'))};
menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.classList.remove('aberto');burger.setAttribute('aria-expanded','false')}));
const header=document.getElementById('header'),topo=document.getElementById('topo'),prog=document.getElementById('progresso');
topo.onclick=()=>scrollTo({top:0,behavior:'smooth'});
function rolagem(){const y=scrollY,h=document.documentElement.scrollHeight-innerHeight;header.classList.toggle('solido',y>40);topo.classList.toggle('visivel',y>700);prog.style.width=(h>0?y/h*100:0)+'%'}
addEventListener('scroll',rolagem,{passive:true});rolagem();
// Galeria em tela cheia
document.querySelectorAll('.galeria figure').forEach(f=>f.addEventListener('click',()=>{luz.querySelector('img').src=f.querySelector('img').src;luz.querySelector('img').alt=f.querySelector('img').alt;luz.querySelector('p').textContent=f.dataset.leg;luz.classList.add('aberta')}));
document.getElementById('luz-x').onclick=()=>luz.classList.remove('aberta');
luz.onclick=e=>{if(e.target===luz)luz.classList.remove('aberta')};
// Aparecer ao rolar, contadores e menu ativo
function conta(el){const alvo=+el.dataset.conta,suf=el.dataset.suf||'',t0=performance.now();(function f(t){const p=Math.min((t-t0)/1400,1);el.textContent=Math.round(alvo*(1-Math.pow(1-p,3)))+suf;if(p<1)requestAnimationFrame(f)})(t0)}
if('IntersectionObserver' in window){
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('on');e.target.querySelectorAll('[data-conta]').forEach(conta);io.unobserve(e.target)}}),{threshold:.12});
  document.querySelectorAll('.rev').forEach(el=>io.observe(el));
  const links=[...menu.querySelectorAll('a')];
  const so=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)links.forEach(l=>l.classList.toggle('ativo',l.getAttribute('href')==='#'+e.target.id))}),{rootMargin:'-45% 0px -50% 0px'});
  links.forEach(l=>{const s=document.querySelector(l.getAttribute('href'));if(s)so.observe(s)});
}else{document.querySelectorAll('.rev').forEach(el=>el.classList.add('on'));document.querySelectorAll('[data-conta]').forEach(conta)}

/* ---------- Teste ao vivo da API (rodar.bat na pasta da Dayene) ---------- */
// No computador (index.html aberto direto ou localhost) usa a API local.
// No site oficial, a API roda em servidor local seguro mantido pelo Prof. Álvaro Machado Júnior.
// O endereço não é publicado neste repositório: informe o seu em API_PUBLICA.
const API_PUBLICA = '';
const LOCAL = location.protocol === 'file:' || ['localhost','127.0.0.1'].includes(location.hostname);
const API = (LOCAL ? 'http://localhost:8000' : API_PUBLICA) + '/api/v1';
const apiStatus = document.getElementById('api-status');
async function verificarApi(){
  if (!LOCAL && !API_PUBLICA) {
    apiStatus.className = 'api-status off';
    apiStatus.querySelector('b').textContent = 'API disponível no site oficial';
    return false;
  }
  try{
    const r = await fetch(API.replace('/api/v1','/'), {cache:'no-store'});
    const d = await r.json();
    apiStatus.className = 'api-status on';
    apiStatus.querySelector('b').textContent = 'API conectada · ' + d.banco;
    return true;
  }catch(e){
    apiStatus.className = 'api-status off';
    apiStatus.querySelector('b').textContent = 'API desligada';
    return false;
  }
}
verificarApi();
const cepInput = document.getElementById('api-cep');
cepInput.addEventListener('input', () => {
  const d = cepInput.value.replace(/\D/g,'').slice(0,8);
  cepInput.value = d.length > 5 ? d.slice(0,5) + '-' + d.slice(5) : d;
});
const fmtDist = m => m < 1000 ? m + ' m' : (m/1000).toFixed(1).replace('.',',') + ' km';
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
document.getElementById('api-form').addEventListener('submit', async ev => {
  ev.preventDefault();
  const out = document.getElementById('api-resultado');
  out.innerHTML = '<div class="api-msg">Buscando…</div>';
  if (!(await verificarApi())) {
    out.innerHTML = LOCAL
      ? '<div class="api-msg">A API está desligada. Dê dois cliques em <b>rodar.bat</b> na pasta da Dayene. Enquanto isso, ligue <b>180</b> para saber os serviços da sua região.</div>'
      : '<div class="api-msg">Esta cópia não tem o endereço da API. Teste a busca no site oficial (acolhimento.prof.alvaromjunior.com) ou ligue <b>180</b> (gratuito, 24h) para saber os serviços da sua região. Em perigo, ligue <b>190</b>.</div>';
    return;
  }
  const q = new URLSearchParams({cep: cepInput.value, limite: 6});
  const tipo = document.getElementById('api-tipo').value; if (tipo) q.set('tipo', tipo);
  try{
    const r = await fetch(API + '/services/by-cep?' + q);
    const d = await r.json();
    if (!r.ok) { out.innerHTML = `<div class="api-msg">${esc(d.detail)}</div>`; return; }
    if (!d.total) { out.innerHTML = `<div class="api-msg">Nenhum serviço cadastrado perto de ${esc(d.regiao)}. Ligue 180 para orientação.</div>`; return; }
    out.innerHTML = `<div class="api-msg">Região aproximada: <b>${esc(d.regiao)}</b> · ${d.total} serviço(s). ${esc(d.privacidade)}</div>` +
      d.servicos.map(s => `<div class="api-item"><div><b>${esc(s.nome)}</b><small>${esc(s.cidade)}/${esc(s.uf)}${s.funciona_24h ? ' · 24 horas' : ''}${s.exemplo ? ' · dado de exemplo' : ''}</small></div><span class="dist">${fmtDist(s.distancia_m)}</span></div>`).join('');
  }catch(e){
    out.innerHTML = '<div class="api-msg">Não foi possível falar com a API agora.</div>';
  }
});
