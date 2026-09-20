(()=>{"use strict";const M=window.InfoAcquisitionModel,$=id=>document.getElementById(id);
const vR=$("vRange"),vN=$("vNum"),cR=$("cRange"),cN=$("cNum");
function num(x){const n=Number(x);return Number.isFinite(n)?Math.max(0,Math.min(10,n)):0}
function f(x){return Number.isInteger(x)?String(x):String(Number(x.toFixed(3)))}
function sync(r,n){const x=num(n.value);r.value=x;n.value=x}
function setEqCells(eq){const s=new Set(eq.map(M.fmt));for(const k of["RR","RS","SR","SS"])$(k).classList.toggle("eq",s.has(`(${k[0]},${k[1]})`))}
function chart(V,c){if(V<=0){$("chart").innerHTML="<p class='muted'>Interior mixed-strategy curve is undefined when V=0.</p>";$("chartText").textContent="Use the pure-equilibrium analysis for this boundary.";return}
const w=520,h=280,L=50,R=20,T=20,B=42,pw=w-L-R,ph=h-T-B,x=z=>L+z/V*pw,y=p=>T+(1-p)*ph;let pts=[];for(let i=0;i<=80;i++){let z=V*i/80;pts.push(`${x(z)},${y(1-z/V)}`)}
const cx=x(Math.min(c,V)),cy=y(Math.max(0,1-Math.min(c,V)/V));const marker=c<=V?`<line x1="${cx}" y1="${T}" x2="${cx}" y2="${T+ph}" stroke="#9a6b22" stroke-dasharray="5 5"/><circle cx="${cx}" cy="${cy}" r="5" fill="#9a6b22"/>`:"";
$("chart").innerHTML=`<svg viewBox="0 0 ${w} ${h}"><rect x="${L}" y="${T}" width="${pw}" height="${ph}" fill="#fbfcfe" stroke="#d9e2ec"/><polyline points="${pts.join(" ")}" fill="none" stroke="#315b8a" stroke-width="3"/>${marker}<text x="${L+pw/2}" y="${h-6}" text-anchor="middle" font-size="13">Research cost c</text><text x="15" y="${T+ph/2}" transform="rotate(-90 15 ${T+ph/2})" text-anchor="middle" font-size="13">p(Research)</text></svg>`;
$("chartText").textContent=c>0&&c<V?`Current point: c=${f(c)}, p(Research)=${f(1-c/V)}.`:"Current parameter is outside the strict interior region or on its boundary."}
function update(){sync(vR,vN);sync(cR,cN);const V=num(vN.value),c=num(cN.value),m=M.payoffs(V,c),eq=M.pure(V,c);for(const k of["RR","RS","SR","SS"])$(k).textContent=`(${f(m[k][0])}, ${f(m[k][1])})`;setEqCells(eq);$("pure").textContent=eq.map(M.fmt).join(", ")||"No pure Nash equilibrium";
const mx=M.mixed(V,c);$("mixed").innerHTML=mx.type==="interior"?`<p><b>p(Research)=${f(mx.pR)}</b><br>p(Skip)=${f(mx.pS)}</p><p class="muted">${mx.text}</p>`:`<p><b>${mx.text}</b></p>`;
const rg=M.region(V,c);$("regionTitle").textContent=rg[0];$("regionText").textContent=rg[1];
$("br1").innerHTML=`A gets <b>${f(V-c)}</b> from Research and <b>${f(V)}</b> from Skip. ${c>0?"Skip is strictly better.":"They are tied."}`;
const alone=V-c;$("br2").innerHTML=`A gets <b>${f(alone)}</b> from Research and <b>0</b> from Skip. ${alone>0?"Research is strictly better.":Math.abs(alone)<1e-12?"They are tied.":"Skip is strictly better."}`;chart(V,c)}
vR.oninput=()=>{vN.value=vR.value;update()};cR.oninput=()=>{cN.value=cR.value;update()};vN.onchange=update;cN.onchange=update;$("reset").onclick=()=>{vR.value=vN.value=4;cR.value=cN.value=2;update()};update()})();