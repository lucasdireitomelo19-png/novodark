"""Biblioteca de efeitos sonoros e trilha sintetizados (sem licença de terceiros).

Uso: python3 sfx.py            -> gera pipeline/sfx/*.wav (48 kHz, estéreo)
Todos os sons são gerados por síntese com numpy/scipy, então podem ser usados livremente.
"""
import os
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sfx")
rng = np.random.default_rng(7)


def t_(d): return np.arange(int(SR * d)) / SR
def ruido(d): return rng.standard_normal(int(SR * d))
def env(d, a=0.01, r=None, curva=3.0):
    n = int(SR * d); e = np.ones(n); na = max(1, int(SR * a)); e[:na] = np.linspace(0, 1, na)
    r = d - a if r is None else r; nr = max(1, int(SR * r)); e[-nr:] *= np.linspace(1, 0, nr) ** curva
    return e
def passa(x, f, tipo="low", ordem=4):
    sos = signal.butter(ordem, f, tipo, fs=SR, output="sos"); return signal.sosfilt(sos, x)
def varredura(x, f0, f1, tipo="band", q=0.5):
    """Filtro passa-banda que se move de f0 a f1 ao longo do som (feito no domínio da frequência, sem cliques)."""
    f, tt, Z = signal.stft(x, SR, nperseg=2048, noverlap=1536)
    u = np.clip(tt / (len(x) / SR), 0, 1); fc = f0 * (f1 / f0) ** u
    larg = fc * q; mask = np.exp(-0.5 * ((f[:, None] - fc[None, :]) / (larg[None, :] / 2 + 1e-9)) ** 2)
    _, y = signal.istft(Z * mask, SR, nperseg=2048, noverlap=1536)
    y = y[: len(x)]; return np.pad(y, (0, len(x) - len(y)))
def reverb(x, tam=1.6, mix=0.35):
    n = int(SR * tam); ir = rng.standard_normal(n) * np.exp(-np.linspace(0, 7, n)); ir = passa(ir, 5000)
    w = signal.fftconvolve(x, ir); seco = np.concatenate([x, np.zeros(len(w) - len(x))])
    return seco * (1 - mix) + w / (np.max(np.abs(w)) + 1e-9) * np.max(np.abs(x)) * mix
def estereo(x, larg=0.0015):
    d = int(SR * larg); return np.stack([x, np.concatenate([np.zeros(d), x[:-d]]) if d else x], 1)
def salvar(nome, x, pico=0.89):
    if x.ndim == 1: x = estereo(x)
    x = x / (np.max(np.abs(x)) + 1e-9) * pico
    os.makedirs(OUT, exist_ok=True); wavfile.write(os.path.join(OUT, nome + ".wav"), SR, (x * 32767).astype(np.int16))


def whoosh(d=0.7, f0=300, f1=4500):
    x = varredura(ruido(d), f0, f1, q=0.9) * env(d, a=d * 0.55, r=d * 0.45, curva=1.5)
    return reverb(x, 0.6, 0.25)
def impacto(d=2.4):
    t = t_(d); grave = np.sin(2 * np.pi * (55 * np.exp(-t * 3) + 32) * t) * np.exp(-t * 2.2)
    estalo = passa(ruido(d), 3000) * np.exp(-t * 35); sub = np.sin(2 * np.pi * 38 * t) * np.exp(-t * 1.4)
    return reverb(grave * 1.0 + estalo * 0.5 + sub * 0.7, 2.2, 0.4)
def riser(d=3.0):
    t = t_(d); x = varredura(ruido(d), 200, 6000, q=0.6) * (t / d) ** 2
    tom = np.sin(2 * np.pi * (80 + 600 * (t / d) ** 2) * t) * (t / d) ** 2 * 0.4
    return reverb(x + tom, 1.0, 0.3)
def batida_coracao(d=1.2):
    t = t_(d); x = np.zeros_like(t)
    for t0 in (0.0, 0.28):
        k = np.clip(t - t0, 0, None); x += np.sin(2 * np.pi * 50 * k) * np.exp(-k * 18) * (t >= t0)
    return passa(x, 200)
def maquina(d=0.09):
    t = t_(d); return passa(ruido(d), 2500, "high") * np.exp(-t * 90) + np.sin(2 * np.pi * 900 * t) * np.exp(-t * 120) * 0.3
def datilografia(n=14, intervalo=0.11):
    d = n * intervalo + 0.5; x = np.zeros(int(SR * d))
    for i in range(n):
        k = maquina(); p = int(SR * (i * intervalo + rng.uniform(-0.02, 0.02))) if i else 0
        x[p:p + len(k)] += k * rng.uniform(0.6, 1.0)
    return x
def carimbo(d=0.8):
    t = t_(d); x = np.sin(2 * np.pi * 110 * t) * np.exp(-t * 25) + passa(ruido(d), 1200) * np.exp(-t * 40) * 0.8
    return reverb(x, 0.5, 0.2)
def ping(d=1.6):
    t = t_(d); return reverb(np.sin(2 * np.pi * 1320 * t) * np.exp(-t * 6) + np.sin(2 * np.pi * 2640 * t) * np.exp(-t * 9) * 0.3, 1.2, 0.4)
def estatica(d=0.35):
    x = passa(ruido(d), 6000, "high") + passa(ruido(d), 800) * 0.5
    corte = (np.sin(2 * np.pi * 37 * t_(d)) > 0).astype(float) * 0.7 + 0.3
    return x * corte * env(d, 0.005, 0.1, 1)
def obturador(d=0.25):
    t = t_(d); x = passa(ruido(d), 3000, "high") * (np.exp(-t * 80) + 0.7 * np.exp(-np.clip(t - 0.07, 0, None) * 90) * (t > 0.07))
    return x
def chuva(d=12.0):
    x = passa(passa(ruido(d), 7000), 500, "high") * 0.6 + passa(ruido(d), 300) * 0.3
    gotas = np.zeros(int(SR * d))
    for p in rng.integers(0, len(gotas) - 400, int(d * 60)): gotas[p:p + 300] += rng.standard_normal(300) * np.exp(-np.arange(300) / 40)
    return x + passa(gotas, 2000, "high") * 0.5
def fogo(d=12.0):
    base = passa(ruido(d), 900) * 0.6; est = np.zeros(int(SR * d))
    for p in rng.integers(0, len(est) - 800, int(d * 25)): est[p:p + 600] += rng.standard_normal(600) * np.exp(-np.arange(600) / 60) * rng.uniform(0.3, 1)
    return base + passa(est, 1500, "high")
def trovao(d=6.0):
    t = t_(d); x = passa(ruido(d), 180) * (np.exp(-t * 0.9) * (1 + 0.6 * np.sin(2 * np.pi * 1.7 * t) ** 2))
    return reverb(x + passa(ruido(d), 2000) * np.exp(-t * 6) * 0.5, 2.5, 0.4)
def glitch(d=0.3):
    t = t_(d); sq = signal.square(2 * np.pi * rng.choice([180, 240, 320]) * t) * 0.3
    return (sq + passa(ruido(d), 5000, "high") * 0.6) * ((np.sin(2 * np.pi * 23 * t) > -0.2).astype(float)) * env(d, 0.002, 0.05, 1)
def drone(d=60.0, raiz=55.0, escuro=True):
    """Trilha de fundo: acorde menor grave com batimento lento e vento filtrado. Feita para tocar em loop."""
    t = t_(d); x = np.zeros_like(t)
    for f, a in ((raiz, 1.0), (raiz * 1.5, 0.45), (raiz * 2 * 1.189, 0.3), (raiz * 2, 0.35), (raiz * 0.5, 0.6)):
        lfo = 1 + 0.003 * np.sin(2 * np.pi * 0.07 * t + f)
        x += a * np.sin(2 * np.pi * f * lfo * t) * (0.7 + 0.3 * np.sin(2 * np.pi * (0.05 + f / 4000) * t))
    vento = varredura(ruido(d), 250, 900, q=0.8) * (0.5 + 0.5 * np.sin(2 * np.pi * (1 / d) * 3 * t)) * 0.6
    x = passa(x, 900) + vento
    cf = int(SR * 2); x[:cf] *= np.linspace(0, 1, cf); x[-cf:] *= np.linspace(1, 0, cf)  # emenda suave no loop
    return reverb(x, 3.0, 0.5)[: len(t)]


if __name__ == "__main__":
    salvar("whoosh", whoosh()); salvar("whoosh_curto", whoosh(0.4, 600, 6000)); salvar("whoosh_grave", whoosh(1.0, 120, 1500))
    salvar("impacto", impacto()); salvar("riser", riser()); salvar("coracao", batida_coracao())
    salvar("datilografia", datilografia()); salvar("carimbo", carimbo()); salvar("ping", ping())
    salvar("estatica", estatica()); salvar("obturador", obturador()); salvar("glitch", glitch())
    salvar("chuva", chuva(), 0.5); salvar("fogo", fogo(), 0.5); salvar("trovao", trovao())
    salvar("drone", drone(), 0.6); salvar("drone_tenso", drone(60.0, 46.25), 0.6)
    print("ok:", sorted(os.listdir(OUT)))
