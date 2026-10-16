import asyncio, json, os, sys, subprocess, edge_tts
d = sys.argv[1]; alvo = float(sys.argv[2]) if len(sys.argv) > 2 else 60.2
TEXT = open(f"{d}/roteiro.txt", encoding="utf-8").read().strip()
async def gerar(rate):
    c = edge_tts.Communicate(TEXT, "pt-BR-AntonioNeural", rate=rate, boundary="WordBoundary",
                             proxy=os.environ.get("HTTPS_PROXY"))
    words = []
    with open(f"{d}/narracao.mp3", "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"t": ch["offset"]/1e7, "d": ch["duration"]/1e7, "w": ch["text"]})
    json.dump(words, open(f"{d}/palavras.json", "w"), ensure_ascii=False)
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{d}/narracao.mp3"]))
r = int(sys.argv[3]) if len(sys.argv) > 3 else 8
for _ in range(6):
    dur = asyncio.run(gerar(f"{r:+d}%"))
    print(d, f"rate {r:+d}% -> {dur:.2f}s")
    if alvo - 0.6 <= dur <= alvo: break
    r += max(1, round((dur/alvo - 1) * 100)) if dur > alvo else -max(1, round((1 - dur/alvo) * 100))
open(f"{d}/rate.txt","w").write(f"{r:+d}%")
