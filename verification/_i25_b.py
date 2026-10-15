# -*- coding: utf-8 -*-
"""I-25：解析求 kappa_rel(e) —— 快速版（eps 级数用 Fraction 精确算术，e 取有理数）

物理/公式推导见 _i25_a.py 的文档串。这里把 eps-级数换成 dict{幂: Fraction} 的精确实现，
并在若干个有理 e 值上求 S(e)，再对 E=e^2 作精确插值得到解析式。

  R_p = 1/(eps(1+e)) , R_a = 1/(eps(1-e))     [面积半径, M=1]
  =>  y = M/p_areal = eps ,  e 同上
  Delta_phi/(2pi) = 1 + 3 eps + S(e) eps^2 + ...
  kappa_rel(e) = (S_FW(e) - S_GR(e))/3
"""
import math
from fractions import Fraction as F

NMAX = 8          # eps 级数保留到 eps^8
NDEG = 8          # P/Q 关于 s 的截断


# ---------------- eps-级数（dict{int: Fraction}）----------------
def sadd(A, B, n=NMAX):
    C = dict(A)
    for k, v in B.items():
        if k <= n:
            C[k] = C.get(k, F(0)) + v
    return {k: v for k, v in C.items() if v != 0}


def sneg(A, n=NMAX):
    return {k: -v for k, v in A.items() if k <= n}


def smul(A, B, n=NMAX):
    C = {}
    for i, ai in A.items():
        for j, bj in B.items():
            k = i + j
            if k <= n:
                C[k] = C.get(k, F(0)) + ai * bj
    return {k: v for k, v in C.items() if v != 0}


def smulc(A, c, n=NMAX):
    return {k: v * c for k, v in A.items() if k <= n and v * c != 0}


def sinv(A, n=NMAX):
    m = min(A)
    A = {k - m: v for k, v in A.items()}
    a0 = A[0]
    B = {0: F(1) / a0}
    for k in range(1, n + 1):
        acc = F(0)
        for i in range(1, k + 1):
            if i in A:
                acc += A[i] * B.get(k - i, F(0))
        B[k] = -acc / a0
    return {k - m: v for k, v in B.items() if v != 0}


def sdiv(A, B, n=NMAX):
    return smul(A, sinv(B, n), n)


def spow(A, p, n=NMAX):
    r = {0: F(1)}
    for _ in range(p):
        r = smul(r, A, n)
    return r


def ssqrt(A, n=NMAX):
    m = min(A)
    assert m % 2 == 0, ('最低幂非偶', m)
    c0 = A[m]
    rn, rd = math.isqrt(c0.numerator), math.isqrt(c0.denominator)
    assert rn * rn == c0.numerator and rd * rd == c0.denominator, ('非完全平方', c0)
    s0 = F(rn, rd)
    n2 = n - m // 2
    w = {k - m: v / c0 for k, v in A.items()}
    w[0] = w.get(0, F(0)) - 1
    w = {k: v for k, v in w.items() if v != 0}
    r = {0: F(1)}
    for k in range(1, n2 + 1):
        acc = F(0)
        for i in range(1, k):
            acc += r.get(i, F(0)) * r.get(k - i, F(0))
        r[k] = (w.get(k, F(0)) - acc) / 2
    return {k + m // 2: s0 * v for k, v in r.items() if v != 0}


def peval(coeffs, U, n=NMAX):
    r = {}
    for c in reversed(coeffs):
        r = sadd(smul(r, U, n), {0: F(c)}, n)
    return r


def wcoef(coeffs, k, SB, n=NMAX):
    r = {}
    for j in range(k, len(coeffs)):
        cj = F(coeffs[j])
        if cj:
            r = sadd(r, smulc(spow(SB, j - k, n), cj * math.comb(j, k), n), n)
    return r


def ser(*pairs):
    """{幂: 系数}"""
    d = {}
    for k, v in pairs:
        d[k] = d.get(k, F(0)) + F(v)
    return {k: v for k, v in d.items() if v != 0}


def sshift(A, k, n=NMAX):
    """乘以 eps^k"""
    return {i + k: v for i, v in A.items() if i + k <= n}


# ---------------- 两个度规（各向同性型，s = M/r）----------------
def _ser_mul(a, b, n):
    """多项式（系数表，关于 s）相乘"""
    r = [F(0)] * (min(len(a) + len(b) - 1, n + 1))
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            if i + j <= n:
                r[i + j] += ai * bj
    return r


def metric(tag):
    """tag = 'GR'/'FW' 或 (f-tag, h-tag) 二元组。
       返回 (P=h/f 的 s-系数表, Q=h 的 s-系数表, sqrt(h) 的 s-系数表)"""
    ft, ht = (tag, tag) if isinstance(tag, str) else tag
    N = NDEG

    def h_and_sq(t):
        if t == 'GR':
            return ([F(math.comb(4, j), 2 ** j) if j <= 4 else F(0) for j in range(N + 1)],
                    [F(1), F(1), F(1, 4)] + [F(0)] * (N - 2))
        return ([F(2 ** j, math.factorial(j)) for j in range(N + 1)],
                [F(1, math.factorial(j)) for j in range(N + 1)])

    def invf(t):
        if t == 'GR':      # (1+s/2)^2 (1-s/2)^-2
            return _ser_mul([F(1), F(1), F(1, 4)] + [F(0)] * (N - 2),
                            [F(j + 1, 2 ** j) for j in range(N + 1)], N)
        return [F(2 ** j, math.factorial(j)) for j in range(N + 1)]   # e^{2s}

    Q, S = h_and_sq(ht)
    P = _ser_mul(Q, invf(ft), N)
    return (P + [F(0)] * (N + 1))[:N + 1], Q, (S + [F(0)] * (N + 1))[:N + 1]


def run(tag, e, n=NMAX, neps=7):
    P, Q, Sh = metric(tag)
    # --- 转折点： u = eps(1±e) sqrt(h)(u) 的不动点迭代 ---
    us = []
    for sg in (1, -1):
        u = ser((1, F(1 + sg * e)))
        for _ in range(neps):
            u = sshift(smulc(peval(Sh, u, n), F(1 + sg * e), n), 1, n)
        us.append(u)
    up, ua = us
    SB = smulc(sadd(up, ua, n), F(1, 2), n)
    AA = smulc(sadd(up, sneg(ua, n), n), F(1, 2), n)
    # --- 两端条件 ---
    Pp = peval(P, sadd(SB, AA, n), n)
    Pm = peval(P, sadd(SB, sneg(AA, n), n), n)
    Qp = peval(Q, sadd(SB, AA, n), n)
    Qm = peval(Q, sadd(SB, sneg(AA, n), n), n)
    beta = sdiv(sadd(spow(SB, 2, n), spow(AA, 2, n), n),
                smulc(smul(SB, AA, n), F(2), n), n)
    E2 = sdiv(sadd(sadd(Qp, Qm, n), sneg(smul(beta, sadd(Qp, sneg(Qm, n), n), n), n), n),
              sadd(sadd(Pp, Pm, n), sneg(smul(beta, sadd(Pp, sneg(Pm, n), n), n), n), n), n)
    MU2 = sdiv(sadd(smul(E2, sadd(Pp, sneg(Pm, n), n), n), sneg(sadd(Qp, sneg(Qm, n), n), n), n),
               smulc(smul(SB, AA, n), F(4), n), n)
    # --- G 的 w-系数 ---
    P0, P1, P2 = (wcoef(P, k, SB, n) for k in range(3))
    Q0, Q1, Q2 = (wcoef(Q, k, SB, n) for k in range(3))
    G0 = sadd(sadd(smul(E2, P0, n), sneg(Q0, n), n), sneg(smul(MU2, spow(SB, 2, n), n), n), n)
    G1 = sadd(sadd(smul(E2, P1, n), sneg(Q1, n), n),
              sneg(smulc(smul(MU2, SB, n), F(2), n), n), n)
    G2 = sadd(sadd(smul(E2, P2, n), sneg(Q2, n), n), sneg(MU2, n), n)
    R0 = sdiv(G0, spow(AA, 2, n), n)
    u1 = sdiv(smul(G1, AA, n), G0, n)
    u2 = sdiv(smul(sadd(G2, R0, n), spow(AA, 2, n), n), G0, n)
    ratio = ssqrt(sdiv(MU2, R0, n), n)
    J = sadd({0: F(1)}, sadd(smulc(u2, F(-1, 4), n), smulc(spow(u1, 2, n), F(3, 16), n), n), n)
    tot = smul(ratio, J, n)
    return tot


def S_of(tag, e, **kw):
    tot = run(tag, e, **kw)
    return tot.get(1), tot.get(2), tot.get(3)


if __name__ == '__main__':
    print('先看几个 e 值上的前几阶（eps^1 应恒为 3）：')
    for tag in ('GR', 'FW'):
        for e in (F(1, 3), F(1, 2), F(3, 4)):
            a1, a2, a3 = S_of(tag, e)
            print('  [%s] e=%-5s  eps^1=%-4s  S=%-22s  eps^3=%.6f'
                  % (tag, e, a1, a2, float(a3)))
