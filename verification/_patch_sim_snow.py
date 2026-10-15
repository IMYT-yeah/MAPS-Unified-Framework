# -*- coding: utf-8 -*-
"""给 `宇宙模拟器.html` 加第 ④ 个面板：雪花屏对照。

第 65 轮：用户观察「界面和电视雪花屏一模一样」。本面板把这个观察做成**可看的实验**：
  左 = tick 置换（框架底层）　右 = 真随机白噪声（每帧重抽）
旁观统计栏里，「k 的极差」这一行会立刻分开两边：左恒为 0、右不断变大。
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
        print("  [XX] {:<26} 命中 {} 次 —— 拒绝".format(tag, n))
        BAD += 1
        return html
    OK += 1
    print("  [OK] {:<26} 已改".format(tag))
    return html.replace(old, new, 1)


t = io.open(P, encoding="utf-8").read()

# ── ① nav 加按钮
t = sub_once(
    t,
    '  <button data-t="p3">③ 规则清单与诚实边界</button>',
    '  <button data-t="p3">③ 规则清单与诚实边界</button>\n'
    '  <button data-t="p4">④ 雪花屏对照 ★</button>',
    "nav 加按钮")

# ── ② 顺手修一处 markdown 残留（`.sub` 里 ** 没被渲染）
t = sub_once(
    t,
    '按《正反物质对风暴统一框架 v2.9》的**底层规则**运行的格点模拟 ——',
    '按《正反物质对风暴统一框架 v2.9》的<strong>底层规则</strong>运行的格点模拟 ——',
    "修 .sub 的 markdown 残留")

# ── ③ 插入新 section（放在 p3 之后、</main> 之前）
SEC = r'''
<!-- ══════════════ 面板 4：雪花屏对照 ══════════════ -->

<section id="p4">
  <div class="grid">
    <div class="card">
      <canvas id="c4" width="920" height="430"></canvas>
      <div class="legend">
        <span><i style="background:#7c8cff"></i>左：tick 置换（框架 §8.6.7 的底层）</span>
        <span><i style="background:#ffd43b"></i>右：真随机白噪声（每帧重新抽）</span>
      </div>
      <div class="row">
        <button class="b pri" id="b4play">▶ 播放</button>
        <button class="b" id="b4step">单步</button>
        <button class="b" id="b4ord">⚑ 有序初态</button>
        <button class="b" id="b4reset">↺ 重置</button>
      </div>
      <label class="sl">速度（tick/帧）= <span id="v4sp">2</span></label>
      <input type="range" id="r4sp" min="1" max="20" step="1" value="2">
      <div class="hint">
        两边的<strong>单帧图像统计上无法区分</strong>（点密度、两点关联、块密度方差都相同）——
        这就是「看起来一模一样」的原因。区别全在<strong>时间与守恒量</strong>里：
        盯住右侧「k 的极差」，左边会一直是 <code>0</code>，右边会不断变大。
      </div>
    </div>
    <div class="card">
      <div class="kv"><span>帧数</span><b id="s4frame">0</b></div>
      <div class="kv"><span>亮点数 k（左 / 右）</span><b id="s4k">0 / 0</b></div>
      <div class="kv"><span>★ k 的极差（自开始）</span><b id="s4kr">0 / 0</b></div>
      <div class="kv"><span>帧间逐位变化量</span><b id="s4d">—</b></div>
      <div class="kv"><span>★ 轴对齐线级重排</span><b id="s4r">—</b></div>
      <div class="hint" style="margin-top:12px">
        <strong>怎么读这两行 ★</strong><br>
        · <code>k 的极差</code>：tick 是<strong>置换</strong> ⟹ 亮点数严格不变；真雪花屏每帧重抽
          ⟹ 按 √(N/4) 跳动（本面板 N = 1728 ⟹ ±21）。<br>
        · <code>轴对齐线级重排</code>：tick 只沿<strong>一个轴</strong>、在<strong>每条线内部</strong>
          交换 ⟹ 每条线的亮点数一定不变（恒为 1.00）；白噪声只有概率巧合（≈0.18）。<br>
        · <code>帧间逐位变化量</code>两边都是 0.50 —— <strong>这个看似显然的判据其实分不开</strong>
          （开发时我在这里预测错了，见核验脚本 SN-4）。
      </div>
    </div>
  </div>
</section>
'''
# 用 </main> 前的注释定位
ANCHOR = "</section>\n\n</main>"
n = t.count(ANCHOR)
if n != 1:
    print("  [XX] {:<26} 命中 {} 次".format("</main> 锚点", n))
    BAD += 1
else:
    t = t.replace(ANCHOR, "</section>\n" + SEC + "\n</main>", 1)
    OK += 1
    print("  [OK] {:<26} 已改".format("插入 panel 4 的 section"))

# ── ④ 插入 JS（放在「// 启动」之前）
JS = r'''
/* ════════════════════════════════════════════════════════════════
   面板 ④  雪花屏对照 —— 同一个「像」，两种机制
   左：tick 置换（框架底层）      右：i.i.d. 白噪声（每帧重抽）
   目的：让「单帧分不开、时间维度分得开」这件事**看得见**。
   判据来源：核验脚本 `_snow_65.py`（SN-1 … SN-9，11 项 0 失败）
   ════════════════════════════════════════════════════════════════ */
const S4 = { L:12, A:null, W:null, kA:0, kW:0,
             kAmin:1e9, kAmax:-1, kWmin:1e9, kWmax:-1,
             dA:0, dW:0, rA:1, rW:0, frame:0, playing:false, sp:2 };

const m4 = (n,m)=> ((n%m)+m)%m;                     // ⚠️ JS 的 % 对负数返回负数
const at4 = (x,y,z)=>{ const L=S4.L; return m4(x,L) + L*m4(y,L) + L*L*m4(z,L); };

function countK(a){ let k=0; for(let i=0;i<a.length;i++) k+=a[i]; return k; }

function init4(){
  const L = S4.L, N = L*L*L, k = N>>1;
  S4.A = new Uint8Array(N);
  const idx = new Int32Array(N);
  for(let i=0;i<N;i++) idx[i] = i;
  for(let i=N-1;i>0;i--){ const j=(Math.random()*(i+1))|0; const t0=idx[i]; idx[i]=idx[j]; idx[j]=t0; }
  for(let i=0;i<k;i++) S4.A[idx[i]] = 1;
  S4.W = new Uint8Array(N);
  for(let i=0;i<N;i++) S4.W[i] = Math.random()<0.5 ? 1 : 0;
  S4.dA = 0; S4.dW = 0; S4.rA = 1; S4.rW = 0; S4.frame = 0;
  S4.kAmin = S4.kAmax = countK(S4.A);
  S4.kWmin = S4.kWmax = countK(S4.W);
  draw4(); stats4();
}

/* 有序初态：两侧都设成「轴 0 的左半全满」—— 然后看它们各自多快变成雪花 */
function ordered4(){
  const L = S4.L, N = L*L*L;
  S4.A = new Uint8Array(N); S4.W = new Uint8Array(N);
  for(let z=0;z<L;z++) for(let y=0;y<L;y++) for(let x=0;x<L;x++){
    const v = (x < L/2) ? 1 : 0;
    S4.A[at4(x,y,z)] = v; S4.W[at4(x,y,z)] = v;
  }
  S4.dA = 0; S4.dW = 0; S4.rA = 1; S4.rW = 0; S4.frame = 0;
  S4.kAmin = S4.kAmax = countK(S4.A);
  S4.kWmin = S4.kWmax = countK(S4.W);
  draw4(); stats4();
}

/* 一 tick：选轴 + 每条线独立相位 + 沿轴完美匹配（与面板 ① 同一规则） */
function step4(){
  const L = S4.L, a = S4.A, b = new Uint8Array(a.length);
  const axis = (Math.random()*3)|0;
  for(let i=0;i<L;i++) for(let j=0;j<L;j++){
    const phi = Math.random()<0.5 ? 0 : 1;
    for(let k=0;k<L;k+=2){
      const p = (k+phi)%L, q = (k+1+phi)%L;
      let i1,j1,k1, i2,j2,k2;
      if(axis===0){ i1=p; j1=i; k1=j; i2=q; j2=i; k2=j; }
      else if(axis===1){ i1=i; j1=p; k1=j; i2=i; j2=q; k2=j; }
      else { i1=i; j1=j; k1=p; i2=i; j2=j; k2=q; }
      b[at4(i1,j1,k1)] = a[at4(i2,j2,k2)];
      b[at4(i2,j2,k2)] = a[at4(i1,j1,k1)];
    }
  }
  // 右：真随机白噪声 —— 每帧逐位重抽
  const w = S4.W, w2 = new Uint8Array(w.length);
  for(let i=0;i<w.length;i++) w2[i] = Math.random()<0.5 ? 1 : 0;

  S4.dA = diffFrac(a, b);   S4.dW = diffFrac(w, w2);
  S4.rA = maxLineKeep(a, b, L);   S4.rW = maxLineKeep(w, w2, L);

  const kA = countK(b), kW = countK(w2);
  if(kA < S4.kAmin) S4.kAmin = kA;
  if(kA > S4.kAmax) S4.kAmax = kA;
  if(kW < S4.kWmin) S4.kWmin = kW;
  if(kW > S4.kWmax) S4.kWmax = kW;

  S4.A = b; S4.W = w2; S4.frame++;
  draw4(); stats4();
}

function diffFrac(a, b){
  let d = 0; for(let i=0;i<a.length;i++) if(a[i]!==b[i]) d++;
  return d/a.length;
}

/* 沿轴 ax：每条线上的亮点数是否不变（比例） */
function lineKeep(a, b, ax, L){
  const nl = L*L, sa = new Int32Array(nl), sb = new Int32Array(nl);
  for(let z=0;z<L;z++) for(let y=0;y<L;y++) for(let x=0;x<L;x++){
    let li;
    if(ax===0) li = y*L + z;
    else if(ax===1) li = x*L + z;
    else li = x*L + y;
    const p = x + L*y + L*L*z;
    sa[li] += a[p]; sb[li] += b[p];
  }
  let same = 0;
  for(let i=0;i<nl;i++) if(sa[i]===sb[i]) same++;
  return same/nl;
}

function maxLineKeep(a, b, L){
  let best = 0;
  for(let ax=0; ax<3; ax++){ const v = lineKeep(a,b,ax,L); if(v>best) best = v; }
  return best;
}

function draw4(){
  const cv = document.getElementById('c4'), g = cv.getContext('2d');
  const W = cv.width, H = cv.height, L = S4.L;
  g.fillStyle = '#080b11'; g.fillRect(0,0,W,H);
  const cell = 30, oy = 46, z = L>>1;
  const blocks = [['左 · tick 置换', S4.A, 40, '#7c8cff', '#2b3550'],
                  ['右 · 真随机白噪声（每帧重抽）', S4.W, 520, '#ffd43b', '#3a3418']];
  for(const [label, arr, ox, cOn, cOff] of blocks){
    g.fillStyle = '#8b98a9'; g.font = '13px monospace';
    g.fillText(label, ox, oy-12);
    for(let y=0;y<L;y++) for(let x=0;x<L;x++){
      g.fillStyle = arr[at4(x,y,z)] ? cOn : cOff;
      g.fillRect(ox+x*cell, oy+y*cell, cell-1, cell-1);
    }
    g.strokeStyle = '#252c3a'; g.lineWidth = 1;
    g.strokeRect(ox-0.5, oy-0.5, cell*L+1, cell*L+1);
  }
  g.fillStyle = '#8b98a9'; g.font = '12px monospace';
  g.fillText('中心切片  z = '+z+'　（每格 = 一个格点）', 40, oy+cell*L+22);
}

function stats4(){
  const kA = countK(S4.A), kW = countK(S4.W);
  const gA = S4.kAmax - S4.kAmin, gW = S4.kWmax - S4.kWmin;
  document.getElementById('s4frame').textContent = S4.frame;
  document.getElementById('s4k').innerHTML =
    '<span style="color:#7c8cff">'+kA+'</span> / <span style="color:#ffd43b">'+kW+'</span>';
  document.getElementById('s4kr').innerHTML =
    '<span style="color:#5ee08a">'+gA+'</span> / <span style="color:#ff8080">'+gW+'</span>';
  document.getElementById('s4d').textContent = S4.dA.toFixed(3)+' / '+S4.dW.toFixed(3);
  document.getElementById('s4r').innerHTML =
    '<span style="color:#5ee08a">'+S4.rA.toFixed(2)+'</span> / '
    + '<span style="color:#ff8080">'+S4.rW.toFixed(2)+'</span>';
}

document.getElementById('b4step').onclick = ()=>{ step4(); };
document.getElementById('b4reset').onclick = ()=>{ init4(); };
document.getElementById('b4ord').onclick = ()=>{ ordered4(); };
document.getElementById('b4play').onclick = (e)=>{
  S4.playing = !S4.playing;
  e.target.textContent = S4.playing ? '⏸ 暂停' : '▶ 播放';
  if(S4.playing) loop4();
};
document.getElementById('r4sp').oninput = (e)=>{
  S4.sp = +e.target.value; document.getElementById('v4sp').textContent = S4.sp;
};
function loop4(){
  if(!S4.playing) return;
  for(let i=0;i<S4.sp;i++) step4();
  requestAnimationFrame(loop4);
}

'''
t = sub_once(t, "// 启动\ninit1(); init2();", JS + "// 启动\ninit1(); init2(); init4();", "插入 panel 4 的 JS")

io.open(P, "w", encoding="utf-8").write(t)

print()
print("通过 {} 项，失败 {} 项".format(OK, BAD))
