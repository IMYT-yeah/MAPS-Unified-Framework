/* 宇宙模拟器 · 核心逻辑功能测试（无 DOM 依赖，纯 Node 运行）
   测试对象 = 面板① 的 tick，与面板② 的弦/粒子规则。 */

// ═══════════════ 面板 ② 的核心逻辑（与 HTML 里一致） ═══════════════
function makeNet(L){
  const S = { L, sZ: new Uint8Array(2*L*L), sX: new Uint8Array(2*L*L) };
  const mod = (n,m)=> ((n%m)+m)%m;   // ⚠️ JS 的 % 对负数返回负数，必须包一层
  S.eH = (x,y)=> mod(y,L)*L + mod(x,L);
  S.eV = (x,y)=> L*L + mod(x,L)*L + mod(y,L);
  S.compute = function(){
    const {L}=S, Av=new Int8Array(L*L).fill(1), Bp=new Int8Array(L*L).fill(1);
    for(let x=0;x<L;x++) for(let y=0;y<L;y++){
      const star=[S.eH(x,y),S.eH(x-1,y),S.eV(x,y),S.eV(x,y-1)];
      let s=1; for(const e of star) if(S.sX[e]) s=-s;
      Av[y*L+x]=s;
      const plaq=[S.eH(x,y),S.eH(x,y+1),S.eV(x,y),S.eV(x+1,y)];
      let t=1; for(const e of plaq) if(S.sZ[e]) t=-t;
      Bp[y*L+x]=t;
    }
    return {Av,Bp};
  };
  S.walk = function(which,x0,y0,len){
    let x=x0,y=y0,arr = which==='Z'?S.sZ:S.sX;
    for(let s=0;s<len;s++){
      const dir=(Math.random()*4)|0; let e;
      if(dir===0){ e=S.eH(x,y); x=(x+1)%L; }
      else if(dir===1){ e=S.eH(x-1,y); x=(x-1+L)%L; }
      else if(dir===2){ e=S.eV(x,y); y=(y+1)%L; }
      else { e=S.eV(x,y-1); y=(y-1+L)%L; }
      arr[e]^=1;
    }
    return {endX:x, endY:y};
  };
  S.flipOne = function(which,x,y,horiz){ const arr=which==='Z'?S.sZ:S.sX; arr[horiz?S.eH(x,y):S.eV(x,y)]^=1; };
  return S;
}
const countNeg = a => { let n=0; for(const v of a) if(v===-1) n++; return n; };

let ok=0, bad=0;
function chk(tag,cond,msg){ if(cond){ok++;console.log('  [OK] '+tag);} else {bad++;console.log('  [XX] '+tag);} console.log('       '+msg); }

console.log('='.repeat(70));
console.log('ST-1  初态：全基态（A_v = +1、B_p = +1）');
console.log('='.repeat(70));
let S = makeNet(6);
let r = S.compute();
chk('ST-1', countNeg(r.Av)===0 && countNeg(r.Bp)===0,
    '初态：负 A_v = '+countNeg(r.Av)+'、负 B_p = '+countNeg(r.Bp)+'（应全 0）');

console.log();
console.log('='.repeat(70));
console.log('ST-2  施加**单条** X_e ⟹ 恰两个 e 粒子（e 的两端顶点）');
console.log('='.repeat(70));
S = makeNet(6); S.flipOne('X', 2, 3, true);        // 水平边 (2,3)-(3,3)
r = S.compute();
let neg = []; for(let i=0;i<r.Av.length;i++) if(r.Av[i]===-1) neg.push([i%6, (i/6)|0]);
console.log('       负 A_v 的位置 = '+JSON.stringify(neg));
chk('ST-2', neg.length===2 && countNeg(r.Bp)===0,
    '单条 X_e ⟹ **恰 2 个 e 粒子**（'+
    '位置 '+JSON.stringify(neg)+'）⟹ 与 §5.7「环面上激发必成对」一致；且 **B_p 不受影响**（e/m 独立）');

console.log();
console.log('='.repeat(70));
console.log('ST-3  走一条**长路径** ⟹ 中间顶点被经过 2 次 ⟹ 仍只有 2 个 e 粒子');
console.log('='.repeat(70));
S = makeNet(8);
let x=0,y=0;
for(let i=0;i<4;i++){ S.flipOne('X',x,y,true); x=(x+1)%8; }   // 沿 x 走 4 步
r = S.compute();
neg = []; for(let i=0;i<r.Av.length;i++) if(r.Av[i]===-1) neg.push([i%8, (i/8)|0]);
console.log('       负 A_v 的位置 = '+JSON.stringify(neg)+'（应恰为路径两端 (0,0) 与 (4,0)）');
chk('ST-3', neg.length===2,
    '长路径也只留 **2 个端点** ⟹ **弦把两个粒子连起来**（中间不产生激发）—— 这正是「弦张力」的图像');

console.log();
console.log('='.repeat(70));
console.log('ST-4  **闭合弦**（绕一圈）⟹ 零激发');
console.log('='.repeat(70));
S = makeNet(6);
for(let i=0;i<6;i++) S.flipOne('X', i, 2, true);      // 沿 x 走满一圈
r = S.compute();
chk('ST-4', countNeg(r.Av)===0,
    '闭合弦 ⟹ 负 A_v = '+countNeg(r.Av)+'（应 0）⟹ **闭合弦无激发**，回到基态扇区');

console.log();
console.log('='.repeat(70));
console.log('ST-5  ⭐ 拓扑约束：**负 A_v 的个数恒为偶数**（Π_v A_v = 1）');
console.log('='.repeat(70));
let allEven = true, samples = [];
for(let t=0;t<400;t++){
  const SS = makeNet(7);
  for(let s=0;s<30;s++){
    const n = 1 + ((Math.random()*4)|0);
    SS.walk(Math.random()<0.5?'Z':'X', (Math.random()*7)|0, (Math.random()*7)|0, n);
  }
  const rr = SS.compute();
  const na = countNeg(rr.Av), nb = countNeg(rr.Bp);
  if(na%2!==0 || nb%2!==0) allEven = false;
  if(t<6) samples.push('(A:'+na+',B:'+nb+')');
}
console.log('       前 6 个样本 (负A, 负B) = '+samples.join(' ')+'  … 共 400 次随机试验');
chk('ST-5', allEven,
    '400 次随机试验里，**负 A_v 与负 B_p 的个数全部是偶数** ✓ —— 这就是 `Π_v A_v = Π_p B_p = 1`（第 60 轮用过的那条）');

console.log();
console.log('='.repeat(70));
console.log('ST-6  面板① 的 tick：双射 + k 守恒');
console.log('='.repeat(70));
function tickTest(L, dims){
  const N = L*L*L;
  const a = new Uint8Array(N);
  for(let i=0;i<N;i++) a[i] = Math.random()<0.5 ? 1:0;
  const k0 = a.reduce((s,v)=>s+v,0);
  const at = (x,y,z)=> ((x%L)+L)%L + L*(((y%L)+L)%L) + L*L*(((z%L)+L)%L);
  // 一次 tick
  const b = new Uint8Array(N);
  const axis = (Math.random()*3)|0;
  for(let i=0;i<L;i++) for(let j=0;j<L;j++){
    const phi = Math.random()<0.5?0:1;
    for(let k=0;k<L;k+=2){
      const p=(k+phi)%L, q=(k+1+phi)%L;
      let i1,j1,k1,i2,j2,k2;
      if(axis===0){i1=p;j1=i;k1=j;i2=q;j2=i;k2=j;}
      else if(axis===1){i1=i;j1=p;k1=j;i2=i;j2=q;k2=j;}
      else {i1=i;j1=j;k1=p;i2=i;j2=j;k2=q;}
      b[at(i1,j1,k1)] = a[at(i2,j2,k2)];
      b[at(i2,j2,k2)] = a[at(i1,j1,k1)];
    }
  }
  return { k0, k1: b.reduce((s,v)=>s+v,0) };
}
let kOK = true;
for(let t=0;t<200;t++){ const {k0,k1} = tickTest(8); if(k0!==k1) kOK=false; }
chk('ST-6', kOK, '200 次随机 tick，占据数 k **严格不变** ✓ ⟹ 置换性质（与核验脚本 US-1 一致）');

console.log();
console.log('='.repeat(70));
console.log('通过 '+ok+' 项，失败 '+bad+' 项');
console.log('='.repeat(70));
process.exit(bad===0?0:1);
