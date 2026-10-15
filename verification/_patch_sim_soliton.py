# -*- coding: utf-8 -*-
"""给 `宇宙模拟器.html` 加第 ⑤ 个面板：孤子的诞生。

第 66 轮：用户要「模拟孤子的诞生 —— 随机湮灭中出现无法湮灭的稳定点」。
本面板把 `_soliton_66.py` 的 Morse 谱算法搬到浏览器：
  · 在 **icosphere** 上生成随机平滑场 f
  · 数临界点：max / min（指数 +1，涡心）与 saddle（指数 −1，反涡心）
  · 统计 **Σ = #max − #saddle + #min** —— 无论怎么随机，**恒为 2**
  · 「⚡ 湮灭一对」按钮：让一对 (+1, −1) 消失；Σ 岿然不动
"""
import io
import os

BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(BASE, "宇宙模拟器.html")

OK = 0
BAD = 0


def sub_once(html, old, new, tag):
    global OK, BAD
    n = html.count(old)
    if n != 1:
        print("  [XX] {:<28} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD += 1
        return html
    OK += 1
    print("  [OK] {:<28} 已改".format(tag))
    return html.replace(old, new, 1)


t = io.open(P, encoding="utf-8").read()

t = sub_once(t,
             '  <button data-t="p4">④ 雪花屏对照 ★</button>',
             '  <button data-t="p4">④ 雪花屏对照 ★</button>\n'
             '  <button data-t="p5">⑤ 孤子的诞生 ★</button>',
             "nav 加按钮")

SEC = r'''
<!-- ══════════════ 面板 5：孤子的诞生 ══════════════ -->

<section id="p5">
  <div class="grid">
    <div class="card">
      <canvas id="c5" width="900" height="560"></canvas>
      <div class="legend">
        <span><i style="background:#7c8cff"></i>指数 +1：max / min（涡心）</span>
        <span><i style="background:#ff6b6b"></i>指数 −1：saddle（反涡心）</span>
        <span><i style="background:#c25a3a"></i>背景色 = 场 f 的高低</span>
      </div>
      <div class="row">
        <button class="b pri" id="b5new">⟳ 重新随机</button>
        <button class="b" id="b5ann">⚡ 湮灭一对</button>
        <button class="b" id="b5reset">↺ 全部复原</button>
        <button class="b" id="b5play">▶ 自动随机</button>
      </div>
      <div class="hint">
        <strong>怎么读</strong>：球面（方向空间 S²）上撒一个随机平滑场，
        数它的三种临界点 —— 局部最大、局部最小（各算 <code>指数 +1</code>），
        以及鞍点（<code>指数 −1</code>）。<br>
        <strong>关键</strong>：<code>Σ = #max − #saddle + #min</code> **永远是 2**，
        不管你怎么随机；而 <code>#max / #min / #saddle</code> 每次都不同。<br>
        点「⚡ 湮灭一对」让一个 +1 和一个 −1 配对消失 —— <strong>Σ 岿然不动</strong>，
        最后必然会剩下 2 个 +1，一个也去不掉。这就是「无法湮灭的稳定点」。
      </div>
    </div>
    <div class="card">
      <div class="kv"><span>场序号</span><b id="s5n">1</b></div>
      <div class="kv"><span>#max / #min</span><b id="s5mm">—</b></div>
      <div class="kv"><span>#saddle</span><b id="s5sd">—</b></div>
      <div class="kv"><span>★ Σ = #max − #saddle + #min</span><b id="s5sig">—</b></div>
      <div class="kv"><span>存活：+1 / −1</span><b id="s5alive">—</b></div>
      <div class="kv"><span>已湮灭对数</span><b id="s5ann">0</b></div>
      <div class="hint" style="margin-top:12px">
        <strong>为什么 Σ 一定是 2</strong><br>
        这是 <strong>Poincaré–Hopf / 毛球定理</strong>：球面上**任何**连续切向量场
        的零点指数和 = <code>χ(S²) = 2</code>。换个曲面就变：<br>
        · 环面 <code>χ = 0</code> ⟹ 可以有**处处非零**的场，一个涡心都不剩；<br>
        · <code>S³: χ = 0</code> 且可平行化 ⟹ 毛球定理不适用（框架 §8.2 已澄清）。<br>
        <strong>所以「无法湮灭」不是概率问题，是几何恒等式。</strong>
      </div>
    </div>
  </div>
</section>
'''

t = sub_once(t, "</section>\n\n</main>", "</section>\n" + SEC + "\n</main>",
             "插入 panel 5 的 section")

JS = r'''
/* ════════════════════════════════════════════════════════════════
   面板 ⑤  孤子的诞生 —— 随机湮灭中的拓扑残余
   球面（方向空间）上撒随机平滑场 ⟹ 数临界点 ⟹ Σ = #max − #saddle + #min ≡ χ = 2
   核验来源：`_soliton_66.py`（SO-1 … SO-9，9 项 0 失败）
   ⚠️ 算法要点（脚本里踩过的坑）：
     · 网格必须用 **icosphere**，经纬网格的极点会把 1-ring 弄退化
     · 计数必须用 **Morse 谱**（数 max/min/saddle），
       **不能**用「单位化 ∇f 沿 1-ring 的绕数」—— 那会在 |∇f| 小的非零点造假涡心
     · 场必须**平滑** —— 逐点独立的随机场处处都是极值，判据不适用
       （这正是框架 §2.3「孤子化」那一步：先粗粒化，才谈得上拓扑缺陷）
   ════════════════════════════════════════════════════════════════ */
const S5 = { verts:null, faces:null, rings:null, f:null, crit:null, alive:null,
             n:1, playing:false, ann:0 };

function norm3(v){ const n = Math.hypot(v[0],v[1],v[2]); return [v[0]/n, v[1]/n, v[2]/n]; }

function icosphere(subdiv){
  const ph = (1 + Math.sqrt(5)) / 2;
  let V = [[-1,ph,0],[1,ph,0],[-1,-ph,0],[1,-ph,0],[0,-1,ph],[0,1,ph],
           [0,-1,-ph],[0,1,-ph],[ph,0,-1],[ph,0,1],[-ph,0,-1],[-ph,0,1]].map(norm3);
  let F = [[0,11,5],[0,5,1],[0,1,7],[0,7,10],[0,10,11],[1,5,9],[5,11,4],[11,10,2],
           [10,7,6],[7,1,8],[3,9,4],[3,4,2],[3,2,6],[3,6,8],[3,8,9],[4,9,5],
           [2,4,11],[6,2,10],[8,6,7],[9,8,1]];
  for(let s=0; s<subdiv; s++){
    const cache = new Map(), NF = [];
    const mid = (i,j)=>{
      const k = i<j ? i+'_'+j : j+'_'+i;
      if(cache.has(k)) return cache.get(k);
      const m = norm3([(V[i][0]+V[j][0])/2, (V[i][1]+V[j][1])/2, (V[i][2]+V[j][2])/2]);
      V.push(m); cache.set(k, V.length-1); return V.length-1;
    };
    for(const [a,b,c] of F){
      const ab=mid(a,b), bc=mid(b,c), ca=mid(c,a);
      NF.push([a,ab,ca],[b,bc,ab],[c,ca,bc],[ab,bc,ca]);
    }
    F = NF;
  }
  return {V, F};
}

function buildRings(nv, F){
  const nxt = new Map();
  for(const [a,b,c] of F){ nxt.set(a+','+b, c); nxt.set(b+','+c, a); nxt.set(c+','+a, b); }
  const out = [];
  for(let v=0; v<nv; v++){
    let start = null;
    for(const k of nxt.keys()){ const p = k.split(','); if(+p[0]===v){ start = +p[1]; break; } }
    const ring = []; let cur = start;
    while(cur !== null && cur !== undefined){
      ring.push(cur);
      const nx = nxt.get(v+','+cur);
      if(nx === undefined || nx === start) break;
      cur = nx;
    }
    out.push(ring);
  }
  return out;
}

function morseSpectrum(f, rings){
  let mx=0, mn=0, sd=0;
  const tol = 1e-12;
  for(let i=0;i<rings.length;i++){
    const ring = rings[i];
    let hi=0, lo=0;
    const seq = [];
    for(const j of ring){
      const d = f[i] - f[j];
      if(d > tol){ lo++; seq.push(1); }
      else if(d < -tol){ hi++; seq.push(-1); }
    }
    if(lo === ring.length){ mx++; }
    else if(hi === ring.length){ mn++; }
    else if(seq.length >= 2){
      let chg = 0;
      for(let k=0;k<seq.length;k++) if(seq[k] !== seq[(k+1)%seq.length]) chg++;
      if(chg >= 4) sd++;
    }
  }
  return {mx, mn, sd};
}

function randField(){
  const V = S5.verts, nv = V.length, nk = 12, sg = 0.55;
  const cs = [], as = [];
  for(let k=0;k<nk;k++){
    cs.push(norm3([gauss(), gauss(), gauss()]));
    as.push(gauss());
  }
  const f = new Float64Array(nv);
  for(let i=0;i<nv;i++){
    let s = 0;
    for(let k=0;k<nk;k++){
      const dx=V[i][0]-cs[k][0], dy=V[i][1]-cs[k][1], dz=V[i][2]-cs[k][2];
      s += as[k] * Math.exp(-(dx*dx+dy*dy+dz*dz) / (2*sg*sg));
    }
    f[i] = s;
  }
  return f;
}
let _g2 = null;
function gauss(){
  if(_g2 !== null){ const v = _g2; _g2 = null; return v; }
  let u = 0, v = 0;
  while(u === 0) u = Math.random();
  while(v === 0) v = Math.random();
  const r = Math.sqrt(-2*Math.log(u));
  _g2 = r*Math.sin(2*Math.PI*v);
  return r*Math.cos(2*Math.PI*v);
}

function init5(){
  if(!S5.verts){
    const {V, F} = icosphere(3);
    S5.verts = V; S5.faces = F; S5.rings = buildRings(V.length, F);
  }
  S5.n = 1; S5.ann = 0;
  newField5();
}

function newField5(){
  S5.f = randField();
  const sp = morseSpectrum(S5.f, S5.rings);
  const crit = [];
  const tol = 1e-12;
  for(let i=0;i<S5.rings.length;i++){
    const ring = S5.rings[i];
    let hi=0, lo=0;
    const seq = [];
    for(const j of ring){
      const d = S5.f[i] - S5.f[j];
      if(d > tol){ lo++; seq.push(1); }
      else if(d < -tol){ hi++; seq.push(-1); }
    }
    if(lo === ring.length) crit.push({vi:i, s:+1});
    else if(hi === ring.length) crit.push({vi:i, s:+1});
    else if(seq.length >= 2){
      let chg = 0;
      for(let k=0;k<seq.length;k++) if(seq[k] !== seq[(k+1)%seq.length]) chg++;
      if(chg >= 4) crit.push({vi:i, s:-1});
    }
  }
  S5.crit = crit;
  S5.alive = crit.map(()=>true);
  S5.ann = 0;
  S5.sp = sp;
  draw5(); stats5();
}

function annihilate5(){
  const c = S5.crit, a = S5.alive;
  const pos = [], neg = [];
  for(let i=0;i<c.length;i++) if(a[i]){ if(c[i].s > 0) pos.push(i); else neg.push(i); }
  if(pos.length <= 2 || neg.length === 0) return;
  a[pos[(Math.random()*pos.length)|0]] = false;
  a[neg[(Math.random()*neg.length)|0]] = false;
  S5.ann++;
  draw5(); stats5();
}

function fcol(v, lo, hi){
  const u = (v - lo) / Math.max(hi - lo, 1e-9);
  const r = Math.round(37 + u * (194 - 37));
  const g = Math.round(64 + u * (90 - 64));
  const b = Math.round(107 + u * (58 - 107));
  return 'rgb('+r+','+g+','+b+')';
}

function draw5(){
  const cv = document.getElementById('c5'), g = cv.getContext('2d');
  const W = cv.width, H = cv.height;
  g.fillStyle = '#080b11'; g.fillRect(0,0,W,H);
  const cx = W/2, cy = H/2 + 8, R = Math.min(W,H)/2 - 60;
  const V = S5.verts, f = S5.f;
  let lo = Infinity, hi = -Infinity;
  for(let i=0;i<f.length;i++){ if(f[i]<lo) lo=f[i]; if(f[i]>hi) hi=f[i]; }
  const faces = S5.faces.map(fc => ({fc, z: (V[fc[0]][2]+V[fc[1]][2]+V[fc[2]][2])/3}));
  faces.sort((p,q)=> p.z - q.z);
  for(const {fc, z} of faces){
    const fv = (f[fc[0]]+f[fc[1]]+f[fc[2]])/3;
    const col = fcol(fv, lo, hi);
    const sh = z > 0 ? 1.0 : 0.45;
    g.fillStyle = col;
    g.globalAlpha = sh;
    g.beginPath();
    g.moveTo(cx + R*V[fc[0]][0], cy - R*V[fc[0]][1]);
    g.lineTo(cx + R*V[fc[1]][0], cy - R*V[fc[1]][1]);
    g.lineTo(cx + R*V[fc[2]][0], cy - R*V[fc[2]][1]);
    g.closePath(); g.fill();
  }
  g.globalAlpha = 1;
  g.strokeStyle = 'rgba(139,152,169,0.35)'; g.lineWidth = 1;
  g.beginPath(); g.arc(cx, cy, R, 0, 6.2832); g.stroke();
  const c = S5.crit, a = S5.alive;
  let npos=0, nneg=0;
  for(let i=0;i<c.length;i++){
    if(!a[i]) continue;
    const v = V[c[i].vi];
    const X = cx + R*v[0], Y = cy - R*v[1];
    const front = v[2] > 0;
    g.globalAlpha = front ? 1 : 0.55;
    g.beginPath();
    g.arc(X, Y, front ? 6 : 4.5, 0, 6.2832);
    g.fillStyle = c[i].s > 0 ? '#7c8cff' : '#ff6b6b';
    g.fill();
    g.strokeStyle = '#0b0e14'; g.lineWidth = 1.5; g.stroke();
    if(c[i].s > 0) npos++; else nneg++;
  }
  g.globalAlpha = 1;
  g.fillStyle = '#8b98a9'; g.font = '12px monospace';
  g.fillText('S² 方向空间（icosphere，'+V.length+' 顶点）｜前面亮、背面暗', 24, 26);
  g.fillText('存活涡心 +1 × '+npos+'　反涡心 −1 × '+nneg, 24, H-16);
}

function stats5(){
  const sp = S5.sp || {mx:0, mn:0, sd:0};
  let npos=0, nneg=0;
  for(let i=0;i<S5.crit.length;i++){
    if(!S5.alive[i]) continue;
    if(S5.crit[i].s > 0) npos++; else nneg++;
  }
  document.getElementById('s5n').textContent = S5.n;
  document.getElementById('s5mm').textContent = sp.mx + ' / ' + sp.mn;
  document.getElementById('s5sd').textContent = sp.sd;
  const sig = sp.mx - sp.sd + sp.mn;
  document.getElementById('s5sig').innerHTML =
    '<span style="color:#5ee08a;font-size:15px">' + sig + '</span>';
  document.getElementById('s5alive').innerHTML =
    '<span style="color:#7c8cff">' + npos + '</span> / <span style="color:#ff6b6b">' + nneg + '</span>';
  document.getElementById('s5ann').textContent = S5.ann;
}

document.getElementById('b5new').onclick = ()=>{ S5.n++; newField5(); };
document.getElementById('b5ann').onclick = ()=>{ annihilate5(); };
document.getElementById('b5reset').onclick = ()=>{ newField5(); };
document.getElementById('b5play').onclick = (e)=>{
  S5.playing = !S5.playing;
  e.target.textContent = S5.playing ? '⏸ 暂停' : '▶ 自动随机';
  if(S5.playing) loop5();
};
function loop5(){
  if(!S5.playing) return;
  S5.n++; newField5();
  setTimeout(loop5, 900);
}

'''
t = sub_once(t, "// 启动\ninit1(); init2(); init4();",
             JS + "// 启动\ninit1(); init2(); init4(); init5();", "插入 panel 5 的 JS")

io.open(P, "w", encoding="utf-8").write(t)
print()
print("通过 {} 项，失败 {} 项".format(OK, BAD))
