/* 第 65 轮：测试 `宇宙模拟器.html` 新增的第 ④ 面板（雪花屏对照）
 * 做法：stub 掉最小 DOM ⟹ 直接跑页面里的 JS ⟹ 验证 tick 的四条结构性质。
 */
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '宇宙模拟器.html'), 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.log('[XX] 没找到 <script>'); process.exit(1); }
const js = m[1];

/* ── 最小 DOM stub ── */
const g2d = new Proxy({}, {
  get: (t, k) => (k in t ? t[k] : () => {}),
  set: (t, k, v) => { t[k] = v; return true; },
});
const els = {};
function mkEl(id) {
  return {
    id, textContent: '', innerHTML: '', value: '12', dataset: {}, width: 920, height: 430,
    getContext: () => g2d, onclick: null, oninput: null, classList: { add(){}, remove(){} },
  };
}
global.document = {
  getElementById: (id) => (els[id] || (els[id] = mkEl(id))),
  querySelectorAll: () => [],
};
global.requestAnimationFrame = () => {};

const full = js + '\n;module.exports = { S4, S1, countK, lineKeep, maxLineKeep, diffFrac,' +
           ' init4, ordered4, step4, at4, tick1, init1 };';
const mod = { exports: {} };
new Function('module', 'require', full)(mod, require);
const { S4, countK, maxLineKeep, diffFrac, init4, ordered4, step4, at4 } = mod.exports;

let OK = 0, BAD = 0;
const chk = (tag, cond, msg) => {
  if (cond) { OK++; console.log('  [OK] ' + tag.padEnd(8) + ' ' + msg); }
  else { BAD++; console.log('  [XX] ' + tag.padEnd(8) + ' ' + msg); }
};

console.log('='.repeat(78));
console.log('ST4-1  面板 ④ 已挂载，状态对象可用');
console.log('='.repeat(78));
init4();
console.log('       S4.L = ' + S4.L + '，|A| = ' + S4.A.length + '，|W| = ' + S4.W.length);
chk('ST4-1', S4.L === 12 && S4.A.length === 1728 && S4.W.length === 1728,
    '两个 N = 1728 的构型已建立');

console.log('');
console.log('='.repeat(78));
console.log('ST4-2  ★ 左（tick）：跑 120 步，k 必须严格不变');
console.log('='.repeat(78));
init4();
const k0 = countK(S4.A);
for (let i = 0; i < 120; i++) step4();
const gA = S4.kAmax - S4.kAmin;
console.log('       k0 = ' + k0 + '　k 极差 = ' + gA + '　帧间变化量 = ' + S4.dA.toFixed(4));
chk('ST4-2', gA === 0 && Math.abs(S4.dA - 0.5) < 0.06,
    'k 极差 = **0**（置换 ⟹ 守恒 ✓）；帧间变化量 ' + S4.dA.toFixed(3) + ' ≈ 0.50');

console.log('');
console.log('='.repeat(78));
console.log('ST4-3  ★ 右（白噪声）：同样 120 帧，k 必须跳');
console.log('='.repeat(78));
const gW = S4.kWmax - S4.kWmin;
console.log('       k 极差 = ' + gW + '　帧间变化量 = ' + S4.dW.toFixed(4) +
            '　理论 √(N/4) = ' + Math.sqrt(1728 / 4).toFixed(1));
chk('ST4-3', gW > 40 && Math.abs(S4.dW - 0.5) < 0.06,
    'k 极差 = **' + gW + '**（远大于 0 ⟹ 判别成功）；帧间变化量 ' + S4.dW.toFixed(3) +
    ' —— **与 tick 相同**（这个判据分不开）');

console.log('');
console.log('='.repeat(78));
console.log('ST4-4  ★ 轴对齐的线级重排：tick 恒为 1，白噪声远小于 1');
console.log('='.repeat(78));
init4();
let rAmin = 9, rWmax = -9;
for (let i = 0; i < 60; i++) {
  step4();
  rAmin = Math.min(rAmin, S4.rA);
  rWmax = Math.max(rWmax, S4.rW);
}
console.log('       tick 的 rA 最小值 = ' + rAmin.toFixed(4) + '（应恒为 1.0000）');
console.log('       白噪声的 rW 最大值 = ' + rWmax.toFixed(4) + '（理论巧合率 C(24,12)/2²⁴ ≈ 0.1612）');
chk('ST4-4', rAmin === 1 && rWmax < 0.30,
    'tick 恒 **1.0000**、白噪声 ≤ **' + rWmax.toFixed(3) + '** ⟹ 时间维度分得开');

console.log('');
console.log('='.repeat(78));
console.log('ST4-5  有序初态：tick 的 k 仍是 864（= N/2），且立刻可跑');
console.log('='.repeat(78));
ordered4();
const kOrd = countK(S4.A);
// 左半满 ⟹ k = (L/2)*L*L = 6*144 = 864
chk('ST4-5', kOrd === 864 && countK(S4.W) === 864,
    '两侧初态的 k 都 = ' + kOrd + '（= 左半 6×12×12）⟹ 密度与随机构型一致，对比公平');

console.log('');
console.log('='.repeat(78));
console.log('ST4-6  左半密度随时间：tick 慢、白噪声瞬间');
console.log('='.repeat(78));
ordered4();
const halfDens = (arr) => {
  let s = 0, n = 0;
  for (let z = 0; z < 12; z++) for (let y = 0; y < 12; y++) for (let x = 0; x < 6; x++) {
    s += arr[at4(x, y, z)]; n++;
  }
  return s / n;
};
const devA = [], devW = [];
for (let t = 0; t < 130; t++) {
  devA.push(Math.abs(halfDens(S4.A) - 0.5));
  devW.push(Math.abs(halfDens(S4.W) - 0.5));
  step4();
}
console.log('       偏离 |左半密度 − 0.5|：');
console.log('         t = 0    tick ' + devA[0].toFixed(4) + ' ｜ 白噪声 ' + devW[0].toFixed(4));
console.log('         t = 1    tick ' + devA[1].toFixed(4) + ' ｜ 白噪声 ' + devW[1].toFixed(4));
console.log('         t = 20   tick ' + devA[20].toFixed(4) + ' ｜ 白噪声 ' + devW[20].toFixed(4));
console.log('         t = 60   tick ' + devA[60].toFixed(4) + ' ｜ 白噪声 ' + devW[60].toFixed(4));
console.log('         t = 129  tick ' + devA[129].toFixed(4) + ' ｜ 白噪声 ' + devW[129].toFixed(4));
chk('ST4-6', devW[1] < 0.06 && devA[1] > 0.3,
    '白噪声 t=1 就混合（' + devW[1].toFixed(4) + '）、tick t=1 仍有 ' + devA[1].toFixed(4) +
    ' ⟹ **有序 → 雪花的速度差 ~60 倍**');

console.log('');
console.log('='.repeat(78));
console.log('通过 ' + OK + ' 项，失败 ' + BAD + ' 项');
console.log('='.repeat(78));
process.exit(BAD === 0 ? 0 : 1);
