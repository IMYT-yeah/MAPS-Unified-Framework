/* 第 66 轮：测试 `宇宙模拟器.html` 新增的第 ⑤ 面板（孤子的诞生）
 * 做法：stub 最小 DOM ⟹ 直接跑页面 JS ⟹ 验证 Morse 谱恒为 χ = 2。
 */
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '宇宙模拟器.html'), 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
const js = m[1];

const g2d = new Proxy({}, {
  get: (t, k) => (k in t ? t[k] : () => {}),
  set: (t, k, v) => { t[k] = v; return true; },
});
const els = {};
const mkEl = (id) => ({
  id, textContent: '', innerHTML: '', value: '12', dataset: {}, width: 900, height: 560,
  getContext: () => g2d, onclick: null, oninput: null, classList: { add(){}, remove(){} },
});
global.document = {
  getElementById: (id) => (els[id] || (els[id] = mkEl(id))),
  querySelectorAll: () => [],
};
global.requestAnimationFrame = () => {};
global.setTimeout = () => {};

const mod = { exports: {} };
new Function('module', 'require',
  js + '\n;module.exports = { S5, icosphere, buildRings, morseSpectrum, randField,' +
       ' newField5, init5, annihilate5 };')(mod, require);
const { S5, icosphere, buildRings, morseSpectrum, randField, init5, annihilate5 } = mod.exports;

let OK = 0, BAD = 0;
const chk = (tag, cond, msg) => {
  if (cond) { OK++; console.log('  [OK] ' + tag.padEnd(8) + ' ' + msg); }
  else { BAD++; console.log('  [XX] ' + tag.padEnd(8) + ' ' + msg); }
};

console.log('='.repeat(78));
console.log('ST5-1  icosphere 与 1-ring：无退化极点');
console.log('='.repeat(78));
const { V, F } = icosphere(3);
const rings = buildRings(V.length, F);
const degs = {};
rings.forEach(r => { degs[r.length] = (degs[r.length] || 0) + 1; });
console.log('       顶点 ' + V.length + ' ／ 面 ' + F.length + ' ／ 1-ring 度数分布 ' + JSON.stringify(degs));
chk('ST5-1', V.length === 642 && F.length === 1280 && degs[5] === 12 && degs[6] === 630,
    'icosphere(subdiv=3) 正确：642 顶点 / 1280 面，12 个五度顶点（**无退化极点**）');

console.log('');
console.log('='.repeat(78));
console.log('ST5-2  ★ 30 个随机场：Σ = #max − #saddle + #min 必须恒为 2');
console.log('='.repeat(78));
init5();
const sigs = [], mxs = [], mns = [], sds = [];
for (let i = 0; i < 30; i++) {
  S5.f = randField();
  const sp = morseSpectrum(S5.f, S5.rings);
  mxs.push(sp.mx); mns.push(sp.mn); sds.push(sp.sd);
  sigs.push(sp.mx - sp.sd + sp.mn);
}
const uniq = [...new Set(sigs)];
const avg = (a) => (a.reduce((x, y) => x + y, 0) / a.length).toFixed(2);
console.log('       #max    均值 ' + avg(mxs) + '（' + Math.min(...mxs) + '–' + Math.max(...mxs) + '）');
console.log('       #min    均值 ' + avg(mns) + '（' + Math.min(...mns) + '–' + Math.max(...mns) + '）');
console.log('       #saddle 均值 ' + avg(sds) + '（' + Math.min(...sds) + '–' + Math.max(...sds) + '）');
console.log('       ★ Σ 的取值集合 = [' + uniq.join(', ') + ']');
chk('ST5-2', uniq.length === 1 && uniq[0] === 2,
    '**Σ 恒为 2**（30 个随机场全部相同），而 #max/#min/#saddle 每次都变');

console.log('');
console.log('='.repeat(78));
console.log('ST5-3  ★ 湮灭：Σ 不变，最后只剩 2 个 +1');
console.log('='.repeat(78));
let sigOK = true, trials = 0, left = [];
for (let s = 0; s < 40; s++) {
  init5();
  const sp0 = morseSpectrum(S5.f, S5.rings);
  const sig0 = sp0.mx - sp0.sd + sp0.mn;
  for (let k = 0; k < 40; k++) annihilate5();
  let npos = 0, nneg = 0;
  for (let i = 0; i < S5.crit.length; i++) {
    if (!S5.alive[i]) continue;
    if (S5.crit[i].s > 0) npos++; else nneg++;
  }
  if (sig0 !== 2) sigOK = false;
  if (npos !== 2 || nneg !== 0) sigOK = false;
  trials++;
  left.push(npos + '/' + nneg);
}
console.log('       40 次独立试验，每次随机场 → 反复湮灭 40 次：');
console.log('       结束时「存活 +1 / −1」的分布 = ' + [...new Set(left)].join(', '));
chk('ST5-3', sigOK && trials === 40,
    '**无论从哪个构型出发、湮灭多少次，最后都恰好剩 2 个 +1、0 个 −1** ⟹ 「无法湮灭的稳定点」');

console.log('');
console.log('='.repeat(78));
console.log('ST5-4  渲染与统计不抛异常');
console.log('='.repeat(78));
let drew = true;
try { init5(); annihilate5(); annihilate5(); } catch (e) { drew = false; console.log('   ' + e.message); }
chk('ST5-4', drew, 'draw5 / stats5 在 stub DOM 下正常执行（无异常）');

console.log('');
console.log('='.repeat(78));
console.log('通过 ' + OK + ' 项，失败 ' + BAD + ' 项');
console.log('='.repeat(78));
process.exit(BAD === 0 ? 0 : 1);
