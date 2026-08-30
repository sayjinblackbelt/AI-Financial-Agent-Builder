const S={i:0,a:{},currency:"BRL",steps:[
{key:"name",q:"Como você gostaria de ser chamado?",help:"Ex.: Filipe"},{key:"currency",q:"Qual moeda você utiliza?",options:["BRL","USD","EUR"]},{key:"frequency",q:"Com que frequência deseja acompanhar suas finanças?",options:["Diariamente","Semanalmente","Mensalmente"]},{key:"income",q:"Qual é sua renda mensal média?",type:"number"},{key:"incomeType",q:"Qual é seu tipo principal de renda?",options:["Fixa","Variável","Mista"]},{key:"extra",q:"Possui renda adicional mensal média?",type:"number"},{key:"fixed",q:"Qual é sua média de despesas fixas mensais?",type:"number"},{key:"variable",q:"Qual é sua média de despesas variáveis mensais?",type:"number"},{key:"debt",q:"Qual é seu comprometimento mensal com dívidas?",type:"number"},{key:"goals",q:"Qual objetivo é mais importante agora?",options:["Reserva de emergência","Reduzir dívidas","Economizar","Compra planejada","Outro"]},{key:"style",q:"Como o agente deve se comunicar?",options:["Simples","Objetivo","Detalhado"]},{key:"alerts",q:"Deseja receber alertas de orçamento?",options:["Sim","Não"]}]};
const $=s=>document.querySelector(s);const num=v=>Number(String(v||0).replace(",","."))||0;function money(n){return new Intl.NumberFormat("pt-BR",{style:"currency",currency:S.currency}).format(n)}
function start(){S.i=0;S.a={};$("#welcome").classList.add("hidden");$("#wizard").classList.remove("hidden");render()}$("#start").onclick=start;
function render(){const s=S.steps[S.i],o=$("#options"),inp=$("#answer"),next=$("#next");$("#progress").textContent=`${S.i+1} de ${S.steps.length}`;$("#question").textContent=s.q;$("#help").textContent=s.help||"";o.innerHTML="";if(s.options){inp.classList.add("hidden");next.classList.add("hidden");s.options.forEach(v=>{const b=document.createElement("button");b.className="option";b.textContent=v;b.onclick=()=>save(v);o.appendChild(b)})}else{inp.value="";inp.type=s.type||"text";inp.classList.remove("hidden");next.classList.remove("hidden");next.onclick=()=>save(inp.value.trim())}}
function save(v){if(v==="")return;S.a[S.steps[S.i].key]=v;if(++S.i<S.steps.length)render();else finish()}
async function finish(){S.currency=S.a.currency||"BRL";const payload={...S.a,alerts:S.a.alerts==="Sim"};let data;try{const r=await fetch("/api/build-profile",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});if(!r.ok)throw Error();data=await r.json()}catch(e){alert("Backend não disponível. Execute o Flask para salvar os dados.");return}const s=data.snapshot;$("#wizard").classList.add("hidden");$("#result").classList.remove("hidden");$("#nameTitle").textContent=`Perfil de ${S.a.name}`;$("#income").textContent=money(s.monthly_income_estimate);$("#expenses").textContent=money(s.monthly_expense_estimate);$("#balance").textContent=money(s.estimated_balance);$("#commitment").textContent=(s.expense_commitment_percent??0).toFixed(1)+"%";$("#config").textContent=JSON.stringify(data.agent_config,null,2);S.cfg=data.agent_config;await refreshSummary();await refreshAnalysis();await refreshInsights()}
async function refreshSummary(){try{const r=await fetch("/api/summary");const s=await r.json();$("#realIncome").textContent=money(s.income);$("#realExpenses").textContent=money(s.expenses);$("#realBalance").textContent=money(s.balance)}catch(e){}}
$("#saveTransaction").onclick=async()=>{const payload={description:$("#transactionDescription").value,amount:$("#transactionAmount").value,transaction_type:$("#transactionType").value,category:$("#transactionCategory").value};const msg=$("#transactionMessage");try{const r=await fetch("/api/transactions",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});const data=await r.json();if(!r.ok)throw Error(data.error);msg.textContent="✓ Movimentação salva.";$("#transactionDescription").value="";$("#transactionAmount").value="";$("#transactionCategory").value="";await refreshSummary();await refreshAnalysis();await refreshInsights()}catch(e){msg.textContent=e.message||"Não foi possível salvar."}};
$("#refreshSummary").onclick=async()=>{await refreshSummary();await refreshAnalysis();await refreshInsights();};$("#back").onclick=()=>{if(S.i>0){S.i--;render()}else{$("#wizard").classList.add("hidden");$("#welcome").classList.remove("hidden")}};$("#restart").onclick=()=>location.reload();$("#copy").onclick=()=>navigator.clipboard.writeText(JSON.stringify(S.cfg,null,2));

async function refreshInsights(){
 try{
  const r=await fetch("/api/insights");const data=await r.json();
  $("#insights").innerHTML=data.insights.map(i=>{const icon=i.priority==="high"?"🔴":i.priority==="medium"?"🟡":i.priority==="positive"?"🟢":"ℹ️";return `<div class="insight"><span>${icon} <strong>${i.title}</strong><br><small>${i.message}</small></span></div>`}).join("");
  const n=await fetch("/api/narrative");const narrative=await n.json();
  $("#narrative").textContent=narrative.narrative;
 }catch(e){console.warn("Insights unavailable",e)}
}

async function refreshAnalysis(){
 try{
  const r=await fetch("/api/analysis"); const data=await r.json();
  const alerts=$("#alerts"), categories=$("#topCategories"), budgets=$("#budgetStatus"), trends=$("#trends");
  alerts.innerHTML=data.alerts.length?data.alerts.map(a=>`<div class="alert ${a.level}">${a.level==="critical"?"🔴":"🟡"} ${a.message}</div>`).join(""):'<div class="alert ok">🟢 Nenhum alerta financeiro relevante no momento.</div>';
  categories.innerHTML=data.top_expense_categories.length?data.top_expense_categories.map((c,i)=>`<div class="insight"><span>#${i+1} ${c.category}</span><strong>${money(c.total)}</strong></div>`).join(""):'<p>Ainda não há despesas registradas.</p>';
  trends.innerHTML=data.trends&&data.trends.length?data.trends.map(t=>{
    const icon=t.direction==="improved"||t.direction==="decreased"?"📈":"📉";
    const label=t.type==="expenses"?"Despesas":"Saldo";
    const direction=t.direction==="improved"?"melhorou":t.direction==="worsened"?"piorou":t.direction==="increased"?"aumentou":"diminuiu";
    const pct=t.percent!==null?` (${Math.abs(t.percent)}%)`:"";
    return `<div class="insight"><span>${icon} ${label} ${direction}${pct} em relação ao mês anterior.</span><strong>${money(Math.abs(t.absolute))}</strong></div>`;
  }).join(""):'<p>Registre dados em mais de um mês para visualizar tendências.</p>';
  budgets.innerHTML=data.budget_status.length?data.budget_status.map(b=>`<div class="insight"><span>${b.status==="exceeded"?"🔴":b.status==="warning"?"🟡":"🟢"} ${b.category} — ${b.percent}%</span><strong>${money(b.spent)} / ${money(b.limit)}</strong></div>`).join(""):'<p>Nenhum orçamento definido.</p>';
 }catch(e){console.warn("Analysis unavailable",e)}
}
$("#saveBudget").onclick=async()=>{
 const payload={category:$("#budgetCategory").value.trim(),monthly_limit:$("#budgetLimit").value};
 try{
  const r=await fetch("/api/budgets",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
  const data=await r.json(); if(!r.ok)throw Error(data.error);
  $("#budgetCategory").value="";$("#budgetLimit").value="";await refreshAnalysis();await refreshInsights();
 }catch(e){alert(e.message||"Não foi possível salvar o orçamento.")}
};