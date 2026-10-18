/* Rede de Apoio e Proteção — interatividade: slides, contador, gráficos (ECharts), tooltips, imagens */
/* ---------- conteúdo gerado (blocos repetidos) ---------- */
const $ = s => document.querySelector(s);
const toc = [
  ['shield-halved','Acolhimento e Segurança Imediata (Lei Maria da Penha)'],
  ['hand-holding-medical','Saúde Mental e Apoio Psicológico via SUS'],
  ['heart-crack','Superação da Dependência e Estatísticas Atuais'],
  ['bullhorn','Conscientização e Campanhas Nacionais'],
  ['user-shield','Defesa Pessoal e Proteção Ativa'],
  ['arrow-trend-up','Reinserção Social e Autonomia Financeira'],
  ['phone-flip','Canais de Apoio e Emergência no Brasil (180, 190, DEAM)']
];
$('#toc').innerHTML = toc.map(([ic,t],i)=>{
  const last = i===toc.length-1;
  return `<button type="button" data-go="${i+2}" class="text-left bg-cardBg rounded-2xl p-4 border ${last?'border-accent border-dashed col-span-2':'border-divider'} flex items-center gap-4 hover:border-accent transition-colors">
    <div class="w-10 h-10 rounded-full ${last?'bg-accent text-white':'bg-accentPale text-iconColor'} flex items-center justify-center shrink-0"><i class="fa-solid fa-${ic} text-lg"></i></div>
    <div><span class="text-[10px] font-bold text-accent uppercase tracking-wider block mb-0.5">Capítulo ${String(i+1).padStart(2,'0')}</span>
    <h3 class="text-sm font-bold leading-tight">${t}</h3></div></button>`;
}).join('');

const s3 = [
  {k:'Eixo de Atendimento',t:'Atendimento Humanizado',id:'c3a',d:'Protocolos ágeis aplicados logo após a ocorrência da violência física ou psicológica.',
   rows:[['heart-pulse','Escuta Ativa','Prioritária'],['user-doctor','Triagem Médica','Imediata'],['hands-holding-child','Apoio Emocional','Contínuo']]},
  {k:'Eixo de Abrigo',t:'Casas e Espaços Seguros',id:'c3b',d:'Ambientes protegidos e sigilosos voltados à preservação total da integridade física.',
   rows:[['shield-halved','Segurança Física','Integral'],['house-chimney','Acomodação','Emergencial'],['location-dot','Localização','Sigilosa']]},
  {k:'Lei Maria da Penha',t:'Suporte Jurídico',id:'c3c',d:'A lei prevê o afastamento imediato do agressor e a proibição de contato para proteção da vítima.',
   rows:[['gavel','Medidas Concedidas','+600 mil/ano'],['scale-balanced','Afastamento','Imediato'],['file-contract','Proibição de Contato','Garantida']]}
];
$('#s3grid').innerHTML = s3.map(c=>`<div class="bg-cardBg rounded-2xl p-6 flex flex-col justify-between border border-divider">
  <div class="mb-2"><p class="text-secondaryText text-xs font-semibold uppercase tracking-wider mb-1">${c.k}</p><h2 class="text-xl font-bold">${c.t}</h2></div>
  <div class="w-full h-[160px]" id="${c.id}"></div>
  <div class="mt-4"><p class="text-secondaryText text-xs mb-3">${c.d}</p><ul class="flex flex-col gap-3">
  ${c.rows.map((r,i)=>`<li class="flex items-center justify-between ${i<2?'border-b border-divider pb-2':''}"><div class="flex items-center gap-2"><i class="fa-solid fa-${r[0]} text-iconColor text-xs w-4"></i><span class="text-secondaryText text-sm">${r[1]}</span></div><b class="${i===2?'text-accent':''} text-sm">${r[2]}</b></li>`).join('')}
  </ul></div></div>`).join('') + `
  <div class="bg-cardBg rounded-2xl p-6 flex flex-col justify-between border border-divider">
    <div class="text-center mb-2"><p class="text-secondaryText text-xs font-medium mb-1">Proteção e Apoio</p><h2 class="text-accent text-3xl font-bold tracking-tight">Rompa o Ciclo</h2></div>
    <div class="w-full h-[190px]" id="c3d"></div>
    <div class="mt-2">
      <div class="flex justify-center gap-2 mb-3"><div class="bg-accent text-white text-[10px] px-2 py-1 rounded-full font-bold">Denuncie</div><div class="bg-accentSoft text-white text-[10px] px-2 py-1 rounded-full font-bold">Apoio</div><div class="bg-accentPale text-accent text-[10px] px-2 py-1 rounded-full font-bold">Vida</div></div>
      <div class="flex justify-between items-center mb-3 px-1">
        <div class="text-center"><p class="text-[11px] text-secondaryText">Central</p><b class="text-xs">Ligue 180</b></div><div class="w-px h-6 bg-divider"></div>
        <div class="text-center"><p class="text-[11px] text-secondaryText">Polícia</p><b class="text-xs">Ligue 190</b></div><div class="w-px h-6 bg-divider"></div>
        <div class="text-center"><p class="text-[11px] text-secondaryText">SAMU</p><b class="text-xs">Ligue 192</b></div>
      </div>
      <div class="bg-bgMain rounded-lg py-2 text-center"><p class="text-secondaryText text-[11px]">Não se cale: <b class="text-primaryText">Sua vida é prioridade absoluta.</b></p></div>
    </div>
  </div>`;

const s4 = [
  ['Pilar 01','Teleatendimento SUS',[
    ['headset','Oferta Mensal','<span class="src" tabindex="0" data-href="https://www.gov.br/saude/pt-br/assuntos/noticias-ms/2026/agosto/sus-oferece-100-mil-teleatendimentos-mensais-de-saude-mental-para-mulheres-em-situacao-de-violencia-e-maes-atipicas/" data-sum="Oferta mensal de 100 mil teleatendimentos em saúde mental pelo SUS.">100 mil teleatendimentos</span>','text-2xl'],
    ['hospital','Modalidade de Rede','Sistema Público Unificado','text-base'],
    ['globe','Alcance do Atendimento','Acolhimento clínico de forma descentralizada e gratuita.']]],
  ['Pilar 02','Canais Digitais',[
    ['user-doctor','Especialidades Conectadas','Psicólogos e Psiquiatras','text-2xl'],
    ['laptop-medical','Interface de Entrada','Plataformas Digitais','text-base'],
    ['hand-holding-heart','Facilidade de Encaminhamento','Redução de barreiras de locomoção com suporte remoto ágil.']]],
  ['Pilar 03','Cuidado Especializado',[
    ['shield-halved','Público Prioritário','<span class="src" tabindex="0" data-href="https://www.gov.br/saude/pt-br/assuntos/noticias-ms/2026/agosto/sus-oferece-100-mil-teleatendimentos-mensais-de-saude-mental-para-mulheres-em-situacao-de-violencia-e-maes-atipicas/" data-sum="Acesso digital especializado para vítimas de violência e mães atípicas.">Vítimas de Agressão e Mães Atípicas</span>','text-xl'],
    ['heart-pulse','Abordagem Terapêutica','Acompanhamento Contínuo','text-base'],
    ['users','Impacto Social','Apoio psicossocial direcionado para recuperação e fortalecimento.']]]
];
$('#s4grid').innerHTML = s4.map(([k,t,rows])=>`<div class="bg-cardBg border border-divider rounded-3xl p-6 flex flex-col justify-between h-full">
  <div class="text-center"><p class="text-xs text-secondaryText uppercase tracking-widest mb-1">${k}</p><h2 class="text-lg font-bold">${t}</h2></div>
  ${rows.map((r,i)=>`<div class="flex flex-col gap-1 ${i<2?'py-4 border-b border-divider':'pt-4'}">
    <div class="flex items-center gap-2 text-secondaryText text-xs mb-1"><i class="fa-solid fa-${r[0]} text-iconColor"></i><p>${r[1]}</p></div>
    ${i<2?`<p class="${r[3]} font-bold text-accent tracking-tight">${r[2]}</p>`:`<p class="text-sm font-medium text-secondaryText">${r[2]}</p>`}</div>`).join('')}
  </div>`).join('');

const s5 = [
  ['heart-pulse','Orientação Emocional','Orientação e regulação emocional contínua para o fortalecimento da autoestima e do equilíbrio psicológico individual.'],
  ['link-slash','Rompimento do Ciclo','Tratamento psicológico focado na quebra definitiva do ciclo de dependência com o agressor e na prevenção de recidivas.'],
  ['shield-halved','Autonomia Afetiva','<span class="src" tabindex="0" data-href="https://br.elmadrid.es/outubro-rosa-amplia-debate-sobre-prevencao-e-saude-emocional-das-mulheres/" data-sum="Rompendo o ciclo de violência e desenvolvendo autonomia afetiva.">Rompendo o ciclo de violência e desenvolvendo autonomia afetiva</span> para estabelecer relações interpessoais saudáveis.'],
  ['seedling','Resiliência Pessoal','Desenvolvimento progressivo de resiliência e autoconfiança para a retomada segura e plena do projeto de vida.']
];
$('#s5grid').innerHTML = s5.map(([ic,t,d])=>`<div class="bg-cardBg rounded-[24px] p-6 border border-divider">
  <div class="w-12 h-12 rounded-2xl bg-accentPale flex items-center justify-center mb-4 text-accent"><i class="fa-solid fa-${ic} text-xl"></i></div>
  <h3 class="text-lg font-bold mb-2">${t}</h3><p class="text-secondaryText text-sm leading-relaxed">${d}</p></div>`).join('');

const s8 = [
  ['Eixo de Formação','Mercado de Trabalho','Programas de encaminhamento ao mercado de trabalho e capacitação profissional, ampliando habilidades práticas para geração de renda sustentável.','Iniciativa Central','Capacitação'],
  ['Articulação Direta','Parcerias com Empresas','Apoiamos a <span class="src" tabindex="0" data-href="https://www.calendarr.com/brasil/dia-nacional-de-luta-contra-a-violencia-a-mulher/" data-sum="Apoio à reinserção social e autonomia econômica com capacitação e parcerias, viabilizando vagas exclusivas.">reinserção social e autonomia econômica com capacitação e parcerias</span>, viabilizando vagas exclusivas para a independência financeira de mulheres assistidas.','Oportunidades','Vagas Exclusivas'],
  ['Ruptura do Ciclo','Reconstrução e Autonomia','Apoio na reconstrução da vida social e conquista da independência econômica, fornecendo base sólida para a segurança pessoal de longo prazo.','Impacto Vital','Emancipação']
];
$('#s8list').innerHTML = s8.map(([b,t,d,l,v])=>`<div class="bg-cardBg rounded-[18px] border border-divider flex items-center justify-between gap-5" style="padding:22px 28px">
  <div class="w-[250px] shrink-0"><span class="inline-block text-[11px] font-bold text-accent bg-accentPale px-2 py-0.5 rounded mb-1.5 uppercase">${b}</span><h3 class="text-lg font-semibold leading-snug">${t}</h3></div>
  <p class="flex-1 text-[13px] text-secondaryText leading-snug">${d}</p>
  <div class="min-w-[140px] shrink-0 flex flex-col items-end text-right gap-1"><p class="text-xs text-secondaryText">${l}</p><h2 class="text-[26px] leading-none font-bold text-accent">${v}</h2></div>
  </div>`).join('');

const s10 = [
  ['building-shield','DEAM','Delegacias Especializadas de Atendimento à Mulher, com investigação focada e proteção imediata.','Segurança'],
  ['house-user','Casa da Mulher','Centro integrado com assistência psicológica, jurídica e social em um só local.','Integração'],
  ['handshake-angle','CRAS / CREAS','Rede de assistência social voltada ao fortalecimento familiar e à redução de vulnerabilidades.','Apoio Social'],
  ['mobile-screen-button','Aplicativos de Proteção','Botões do pânico digitais (ex.: SOS Mulher) ligados direto às centrais de monitoramento.','Tecnologia']
];
$('#s10cards').innerHTML = s10.map(([ic,t,d,tag])=>`<div class="bg-cardBg p-5 rounded-2xl border border-divider flex flex-col transition-transform hover:-translate-y-0.5">
  <div class="flex items-center gap-2 mb-2"><i class="fa-solid fa-${ic} text-accent"></i><h3 class="font-bold">${t}</h3></div>
  <p class="text-xs text-secondaryText leading-tight mb-3">${d}</p>
  <div class="mt-auto pt-2 border-t border-divider flex justify-between items-center"><span class="text-[10px] font-bold text-accent uppercase">${tag}</span><i class="fa-solid fa-chevron-right text-[10px] text-divider"></i></div></div>`).join('');

/* ---------- gráficos (ECharts) ---------- */
const C = {p:'#5D3B95', s:'#8B6BC5', t:'#D5CCEB', txt:'#666666'};
const charts = [];
function mk(id, opt){ const el=document.getElementById(id); if(!el||!window.echarts) return; const c=echarts.init(el); c.setOption(opt); charts.push(c); }
function bar(data, cats){ return {
  tooltip:{trigger:'axis',axisPointer:{type:'none'}},
  grid:{top:'5%',left:'2%',right:'6%',bottom:'5%',containLabel:true},
  xAxis:{type:'value',splitLine:{show:false},axisLabel:{show:false},axisLine:{show:false}},
  yAxis:{type:'category',data:cats,axisLine:{show:false},axisTick:{show:false},axisLabel:{color:C.txt,fontSize:10,fontWeight:500}},
  series:[{type:'bar',barWidth:16,data:data.map((v,i)=>({value:v,itemStyle:{color:[C.t,C.s,C.p][i]}})),itemStyle:{borderRadius:[0,4,4,0]}}] }; }
function donut(data, colors, r){ return { color:colors, tooltip:{trigger:'item',formatter:'{b}: {d}%'},
  series:[{type:'pie',radius:r||['60%','88%'],avoidLabelOverlap:false,label:{show:false},labelLine:{show:false},data}] }; }
function line(years, vals, showY){ return { tooltip:{trigger:'axis'},
  grid: showY ? {top:10,bottom:20,left:30,right:10} : {top:'10%',left:'5%',right:'5%',bottom:'0%',containLabel:true},
  xAxis:{type:'category',data:years,axisLabel:{fontSize:showY?9:10,color:C.txt},axisLine:{lineStyle:{color:'#E0E0E0'}}},
  yAxis:{type:'value',splitLine:{lineStyle:{type:'dashed'}},axisLabel:{show:showY,fontSize:9,color:C.txt}},
  series:[{data:vals,type:'line',smooth:true,symbol:'circle',symbolSize:showY?6:8,itemStyle:{color:C.p},
    areaStyle:{color:new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'rgba(93,59,149,.3)'},{offset:1,color:'rgba(93,59,149,0)'}])}}] }; }

function initCharts(){
  if(!window.echarts) return;
  mk('c3a', bar([85,92,98],['Emocional','Médico','Escuta']));
  mk('c3b', bar([80,90,100],['Sigilo','Vagas','Segurança']));
  mk('c3c', bar([88,94,99],['Orientação','Proteção','Medidas']));
  mk('c3d', { tooltip:{trigger:'item',formatter:'{b}: {d}%'}, series:[{name:'Rede de Apoio',type:'pie',radius:['55%','85%'],avoidLabelOverlap:false,
    itemStyle:{borderRadius:4,borderColor:'#fff',borderWidth:2},label:{show:false,position:'center'},
    emphasis:{label:{show:true,fontSize:12,fontWeight:'bold',formatter:'{b}'},scale:true,scaleSize:4},labelLine:{show:false},
    data:[{value:35,name:'Canais 180/190',itemStyle:{color:C.p}},{value:35,name:'Medidas Lei Maria',itemStyle:{color:C.s}},{value:30,name:'Rede Socioassistencial',itemStyle:{color:C.t}}]}]});
  mk('c6a', donut([{value:40,name:'CBF'},{value:35,name:'Ministério das Mulheres'},{value:25,name:'Ministério do Esporte'}],[C.p,C.s,C.t]));
  mk('c6b', donut([{value:65,name:'Ligue 180'},{value:35,name:'Disque 190'}],[C.p,C.s]));
  mk('c6c', { color:[C.p,C.s,C.t,'#E0E0E0'], tooltip:{trigger:'item',formatter:'{b}: {d}%'},
    series:[{type:'pie',radius:['45%','70%'],avoidLabelOverlap:true,itemStyle:{borderRadius:4,borderColor:'#fff',borderWidth:2},
      label:{show:true,formatter:'{b}\n{d}%',color:'#000',fontSize:12,fontWeight:'bold',lineHeight:16},labelLine:{show:true,length:12,length2:8,smooth:true},
      data:[{value:45,name:'Estádios e Arenas'},{value:25,name:'Transmissão Oficial'},{value:20,name:'Redes Sociais'},{value:10,name:'Ações Locais'}]}]});
  mk('c9', line(['2020','2021','2022','2023'],[450,520,580,640],true));
  mk('c10', line(['2020','2021','2022','2023'],[120,150,210,280],false));
}

/* ---------- leitor: escala, contador, apresentação ---------- */
const frames = [...document.querySelectorAll('#reader > .frame')];
const N = frames.length;
frames.forEach((f,i)=>{ const n=document.createElement('span'); n.className='num'; n.textContent=(i+1)+' / '+N; f.appendChild(n); });
let cur = 0, presenting = false;

function fit(){
  if(presenting){
    const vw=innerWidth, vh=innerHeight, s=Math.min(vw/1280, vh/720);
    frames.forEach(f=>{ const sl=f.firstElementChild; sl.style.transform=`scale(${s})`;
      f.style.width=1280*s+'px'; f.style.height=720*s+'px'; f.style.left=(vw-1280*s)/2+'px'; f.style.top=(vh-720*s)/2+'px'; });
  } else {
    frames.forEach(f=>{ f.style.width=''; f.style.left=''; f.style.top='';
      const s=f.clientWidth/1280; f.firstElementChild.style.transform=`scale(${s})`; f.style.height=720*s+'px'; });
  }
}
function setCount(){ $('#count').textContent=(cur+1)+' / '+N; $('#hCount').textContent=(cur+1)+' / '+N; $('#hProg').style.width=((cur+1)/N*100)+'%'; }
function go(i){
  cur=Math.max(0,Math.min(N-1,i)); setCount();
  if(presenting){ frames.forEach((f,k)=>f.classList.toggle('current',k===cur)); }
  else frames[cur].scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth', block:'start'});
}
let hudTimer;
function pokeHud(){ document.body.classList.add('hud-on'); clearTimeout(hudTimer); hudTimer=setTimeout(()=>document.body.classList.remove('hud-on'),2200); }
function startShow(){
  presenting=true; document.body.classList.add('presenting'); hideTip();
  frames.forEach((f,k)=>f.classList.toggle('current',k===cur)); fit(); setCount(); pokeHud();
  try{ const p=document.documentElement.requestFullscreen?.(); p&&p.catch(()=>{}); }catch(e){}
}
function endShow(){
  presenting=false; document.body.classList.remove('presenting','hud-on');
  frames.forEach(f=>f.classList.remove('current')); fit();
  try{ if(document.fullscreenElement) document.exitFullscreen().catch(()=>{}); }catch(e){}
  frames[cur].scrollIntoView({block:'start'});
}
$('#playBtn').addEventListener('click', startShow);
$('#hExit').addEventListener('click', endShow);
$('#hPrev').addEventListener('click', e=>{ e.stopPropagation(); go(cur-1); pokeHud(); });
$('#hNext').addEventListener('click', e=>{ e.stopPropagation(); go(cur+1); pokeHud(); });
document.addEventListener('fullscreenchange', ()=>{ if(!document.fullscreenElement && presenting) endShow(); });
document.addEventListener('keydown', e=>{
  if(e.target.matches('input,textarea')) return;
  const nextK=['ArrowRight','ArrowDown','PageDown',' '], prevK=['ArrowLeft','ArrowUp','PageUp'];
  if(presenting){
    if(nextK.includes(e.key)){ e.preventDefault(); go(cur+1); }
    else if(prevK.includes(e.key)){ e.preventDefault(); go(cur-1); }
    else if(e.key==='Home') go(0); else if(e.key==='End') go(N-1);
    else if(e.key==='Escape') endShow();
    pokeHud();
  } else if(e.key==='f' || e.key==='F5'){ e.preventDefault(); startShow(); }
});
$('#reader').addEventListener('click', e=>{
  if(!presenting || e.target.closest('button,.src')) return;
  (e.clientX > innerWidth/2) ? go(cur+1) : go(cur-1); pokeHud();
});
document.addEventListener('mousemove', ()=>{ if(presenting) pokeHud(); });
let tx=null;
$('#reader').addEventListener('touchstart', e=>{ tx=e.touches[0].clientX; }, {passive:true});
$('#reader').addEventListener('touchend', e=>{ if(!presenting||tx===null) return; const dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>40) go(cur+(dx<0?1:-1)); tx=null; pokeHud(); });

/* sumário clicável */
$('#toc').addEventListener('click', e=>{ const b=e.target.closest('[data-go]'); if(b){ e.stopPropagation(); go(+b.dataset.go); } });

/* contador acompanha a rolagem */
const io = new IntersectionObserver(es=>{ if(presenting) return;
  es.forEach(en=>{ if(en.isIntersecting && en.intersectionRatio>.55){ cur=frames.indexOf(en.target); setCount(); } }); }, {threshold:[.55]});
frames.forEach(f=>io.observe(f));

/* copiar link */
function toast(msg){ const t=$('#toast'); t.textContent=msg; t.hidden=false; clearTimeout(toast._t); toast._t=setTimeout(()=>t.hidden=true,1800); }
$('#copyBtn').addEventListener('click', ()=>{
  const url=location.href.split('#')[0];
  try{ navigator.clipboard.writeText(url).then(()=>toast('Link copiado')).catch(()=>toast(url)); }catch(e){ toast(url); }
});

/* fontes de dados (dica) */
const tip=$('#tip');
function showTip(el){
  tip.innerHTML=`<strong>Fonte de dados</strong>${el.dataset.sum}<a href="${el.dataset.href}" target="_blank" rel="noopener">${el.dataset.href.replace(/^https?:\/\//,'').slice(0,70)}…</a>`;
  tip.hidden=false; const r=el.getBoundingClientRect(), w=tip.offsetWidth, h=tip.offsetHeight;
  let x=Math.min(Math.max(8,r.left), innerWidth-w-8), y=r.bottom+8; if(y+h>innerHeight-8) y=r.top-h-8;
  tip.style.left=x+'px'; tip.style.top=y+'px';
}
function hideTip(){ tip.hidden=true; }
let tipHold=false;
document.addEventListener('mouseover', e=>{ const s=e.target.closest('.src'); if(s) showTip(s); else if(!e.target.closest('#tip') && !tipHold) hideTip(); });
document.addEventListener('focusin', e=>{ const s=e.target.closest('.src'); if(s) showTip(s); });
tip.addEventListener('mouseenter',()=>tipHold=true); tip.addEventListener('mouseleave',()=>{tipHold=false; hideTip();});
addEventListener('scroll', ()=>{ if(!tipHold) hideTip(); }, {passive:true});

/* trocar imagem dos espaços de foto */
let slotTarget=null;
document.querySelectorAll('.img-slot').forEach(sl=>{
  const b=document.createElement('button'); b.type='button'; b.className='swap'; b.innerHTML='<i class="fa-solid fa-image"></i> Trocar imagem';
  b.addEventListener('click', e=>{ e.stopPropagation(); slotTarget=sl; $('#imgPick').click(); });
  sl.appendChild(b);
});
$('#imgPick').addEventListener('change', e=>{
  const f=e.target.files[0]; if(!f||!slotTarget) return;
  const rd=new FileReader(); rd.onload=()=>{ slotTarget.style.backgroundImage=`url("${rd.result}")`; slotTarget.classList.add('has-img'); }; rd.readAsDataURL(f);
  e.target.value='';
});

/* inicialização */
addEventListener('resize', ()=>{ fit(); charts.forEach(c=>c.resize()); });
fit(); setCount();
(document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(()=>{ initCharts(); fit(); });
