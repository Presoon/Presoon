import base64, io, pathlib, random
from PIL import Image

LOGOS = pathlib.Path(r"D:/Projekty/AI/inFlowsLogo/LOGOS")
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)
FONT = "'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
MONO = "'Cascadia Code',Consolas,'SFMono-Regular',Menlo,monospace"
RM = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def logo(name, size=256):
    # Crop transparent padding (inFlows has ~6% per side) so all logos render at the same visual size.
    im = Image.open(LOGOS / f"{name}-{size}.png").convert("RGBA")
    im = im.crop(im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox())
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def chips(items, x, y, color):
    out = []
    for t in items:
        w = len(t) * 6.9 + 22
        out.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-opacity=".45"/>'
                   f'<text x="{x + w / 2:.0f}" y="{y + 16.5}" text-anchor="middle" class="chip">{t}</text>')
        x += w + 8
    return "".join(out)


def card(key, name, accent, accent2, lines, chip_items, status, visual, extra_css=""):
    desc = "".join(f'<tspan x="200" dy="{0 if i == 0 else 22}">{l}</tspan>' for i, l in enumerate(lines))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="230" viewBox="0 0 840 230" role="img" aria-label="{name}: {' '.join(lines)}">
<style>
text{{font-family:{FONT};fill:#e6edf3}}
.t{{font-size:34px;font-weight:700;letter-spacing:-.5px}}
.d{{font-size:15.5px;fill:#b3bdc8}}
.chip{{font-size:12px;font-weight:600;fill:#e6edf3}}
.st{{font-size:12px;font-weight:700;letter-spacing:1.5px;fill:{accent2}}}
.glow{{animation:glow 4s ease-in-out infinite;transform-origin:105px 115px}}
@keyframes glow{{0%,100%{{opacity:.45;transform:scale(.95)}}50%{{opacity:.9;transform:scale(1.07)}}}}
.logo{{animation:bob 6s ease-in-out infinite}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
.dot{{animation:blink 1.6s ease-in-out infinite}}
@keyframes blink{{50%{{opacity:.25}}}}
{extra_css}
{RM}
</style>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="{accent}" stop-opacity=".9"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="{accent2}" stop-opacity=".7"/><stop offset="1" stop-color="{accent2}" stop-opacity="0"/></radialGradient>
<linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".18"/><stop offset=".5" stop-color="{accent2}" stop-opacity=".6"/><stop offset="1" stop-color="#ffffff" stop-opacity=".08"/></linearGradient>
<clipPath id="c"><rect width="840" height="230" rx="22"/></clipPath>
</defs>
<g clip-path="url(#c)">
<rect width="840" height="230" fill="#0d1117"/>
<rect width="840" height="230" fill="url(#bg)" opacity=".55"/>
<circle class="glow" cx="105" cy="115" r="105" fill="url(#halo)"/>
</g>
<rect x=".75" y=".75" width="838.5" height="228.5" rx="21.5" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
<g class="logo"><image href="{logo(key)}" x="35" y="45" width="140" height="140"/></g>
<circle class="dot" cx="206" cy="44" r="4" fill="{accent2}"/>
<text x="216" y="48.5" class="st">{status}</text>
<text x="200" y="88" class="t">{name}</text>
<text x="200" y="118" class="d">{desc}</text>
{chips(chip_items, 200, 178, accent2)}
<g transform="translate(600 0)">{visual}</g>
</svg>'''
    (OUT / f"card-{key.lower()}.svg").write_text(svg, encoding="utf-8")


# --- inSpeak: live waveform -------------------------------------------------
random.seed(7)
bars = []
for i in range(26):
    h = 18 + 70 * abs(__import__("math").sin(i * 0.55)) * (0.5 + random.random() / 2)
    bars.append(f'<rect class="b" x="{12 + i * 8.4:.1f}" y="{100 - h / 2:.1f}" width="4.6" height="{h:.1f}" rx="2.3" fill="url(#wv)" style="animation-delay:-{random.random() * 1.2:.2f}s;animation-duration:{0.8 + random.random() * 0.7:.2f}s"/>')
inspeak_vis = f'''<defs><linearGradient id="wv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7a6e6"/><stop offset="1" stop-color="#b13c9b"/></linearGradient></defs>
{''.join(bars)}
<text x="120" y="178" text-anchor="middle" style="font-family:{MONO};font-size:12px;fill:#f0c4e8">voice → text · on-device</text>'''
card("inSpeak", "inSpeak", "#5c1a55", "#e46ccc",
     ["Local voice dictation for Windows. Hold a key, speak,", "text lands in any app. 100% offline: no cloud, no account."],
     ["Parakeet TDT · ONNX", ".NET NativeAOT", "WinUI 3", "v1.5.5"], "FREE DOWNLOAD", inspeak_vis,
     ".b{transform-box:fill-box;transform-origin:center;animation:wave 1s ease-in-out infinite alternate}@keyframes wave{from{transform:scaleY(.25)}to{transform:scaleY(1)}}")

# --- inFlows: messages flowing between Azure nodes -------------------------
paths = ["M40 100 C 100 40, 140 40, 160 52", "M40 100 C 100 100, 140 100, 160 100", "M40 100 C 100 160, 140 160, 160 148"]
flows = []
for i, p in enumerate(paths):
    flows.append(f'<path d="{p}" fill="none" stroke="#5fe0c0" stroke-opacity=".35" stroke-width="2" stroke-dasharray="4 6"/>')
    for k in range(3):
        flows.append(f'<circle r="4" fill="#7cf2d4"><animateMotion dur="{2.4 + i * 0.4}s" begin="-{k * 0.85 + i * 0.3:.2f}s" repeatCount="indefinite" path="{p}"/></circle>')
node = lambda x, y, t: f'<rect x="{x - 34}" y="{y - 15}" width="68" height="30" rx="8" fill="#0d1117" fill-opacity=".75" stroke="#5fe0c0" stroke-opacity=".7"/><text x="{x}" y="{y + 4.5}" text-anchor="middle" style="font-family:{MONO};font-size:11.5px;fill:#bff7ea">{t}</text>'
inflows_vis = f'''{''.join(flows)}{node(40, 100, "queue")}{node(192, 52, "topic")}{node(192, 100, "resubmit")}{node(192, 148, "DLQ")}
<text x="120" y="190" text-anchor="middle" style="font-family:{MONO};font-size:12px;fill:#bff7ea">Service Bus · Event Grid</text>'''
card("inFlows", "inFlows", "#0f4a5c", "#5fe0c0",
     ["Desktop explorer for Azure Service Bus &amp; Event Grid.", "Peek, triage DLQs, resubmit, watch messages flow live."],
     ["Electron", "React + TypeScript", "Azure SDK", "Fastify"], "EARLY ACCESS", inflows_vis)

# --- UsageWatch: quota bars --------------------------------------------------
rows = [("Claude", "72%;38%;55%;72%", 7), ("Codex", "40%;81%;63%;40%", 9), ("Gemini", "88%;64%;30%;88%", 11), ("z.ai", "25%;47%;70%;25%", 8)]
uw = []
for i, (n, vals, dur) in enumerate(rows):
    y = 38 + i * 34
    uw.append(f'<text x="10" y="{y + 11}" style="font-family:{MONO};font-size:12px;fill:#d3ccff">{n}</text>'
              f'<rect x="70" y="{y}" width="160" height="14" rx="7" fill="#ffffff" fill-opacity=".08"/>'
              f'<rect x="70" y="{y}" height="14" rx="7" fill="url(#q)"><animate attributeName="width" dur="{dur}s" repeatCount="indefinite" values="{";".join(str(int(v[:-1]) * 1.6) for v in vals.split(";"))}" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/></rect>')
usage_vis = f'''<defs><linearGradient id="q" x1="0" x2="1"><stop offset="0" stop-color="#7d6bff"/><stop offset="1" stop-color="#c3b8ff"/></linearGradient></defs>
{''.join(uw)}<text x="120" y="190" text-anchor="middle" style="font-family:{MONO};font-size:12px;fill:#d3ccff">quota left, live from the API</text>'''
card("usageWatch", "UsageWatch", "#2c2275", "#9d8cff",
     ["Tray app + desktop widget that shows how much of your", "AI subscription is left: Claude, Codex, Gemini, Kimi, z.ai."],
     ["Tauri 2 · Rust", "React", "Open source · MIT", "v0.3.1"], "OPEN SOURCE", usage_vis)

# --- Header ------------------------------------------------------------------
phrases = ["local-first Windows apps", "Azure messaging &amp; integrations", "a homelab that ships it all"]
rot = "".join(f'<text x="170" y="196" class="r r{i}" style="animation-delay:{i * 3}s">{p}</text>' for i, p in enumerate(phrases))
header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="300" viewBox="0 0 840 300" role="img" aria-label="Kamil Szpak: I build local-first Windows apps, Azure integrations and a homelab that ships it all.">
<style>
text{{font-family:{FONT};fill:#e6edf3}}
.h{{font-size:54px;font-weight:800;letter-spacing:-1.5px}}
.s{{font-size:22px;fill:#9aa7b4}}
.r{{font-size:22px;font-weight:700;fill:url(#tg);opacity:0;animation:rot 9s infinite}}
@keyframes rot{{0%{{opacity:0;transform:translateY(10px)}}4%,30%{{opacity:1;transform:translateY(0)}}34%,100%{{opacity:0;transform:translateY(-10px)}}}}
.m{{font-family:{MONO};font-size:14px;fill:#7d8590}}
.p{{font-family:{MONO};font-size:14px}}
.cur{{animation:cur 1s steps(1) infinite}}
@keyframes cur{{50%{{opacity:0}}}}
.o1{{animation:d1 14s ease-in-out infinite}}.o2{{animation:d2 17s ease-in-out infinite}}.o3{{animation:d3 12s ease-in-out infinite}}
.f1{{animation:fl 6s ease-in-out infinite}}.f2{{animation:fl 7s ease-in-out -2s infinite}}.f3{{animation:fl 5s ease-in-out -4s infinite}}
@keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-12px)}}}}
@keyframes d1{{50%{{transform:translate(120px,40px)}}}}@keyframes d2{{50%{{transform:translate(-140px,-30px)}}}}@keyframes d3{{50%{{transform:translate(60px,-50px)}}}}
.wave{{animation:hand 2.4s ease-in-out infinite;transform-box:fill-box;transform-origin:70% 80%}}
@keyframes hand{{0%,60%,100%{{transform:rotate(0)}}10%,30%{{transform:rotate(14deg)}}20%,40%{{transform:rotate(-8deg)}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}.r0{{opacity:1}}}}
</style>
<defs>
<radialGradient id="g1"><stop offset="0" stop-color="#5fe0c0" stop-opacity=".55"/><stop offset="1" stop-color="#5fe0c0" stop-opacity="0"/></radialGradient>
<radialGradient id="g2"><stop offset="0" stop-color="#e46ccc" stop-opacity=".5"/><stop offset="1" stop-color="#e46ccc" stop-opacity="0"/></radialGradient>
<radialGradient id="g3"><stop offset="0" stop-color="#7d6bff" stop-opacity=".6"/><stop offset="1" stop-color="#7d6bff" stop-opacity="0"/></radialGradient>
<linearGradient id="tg" x1="0" x2="1"><stop offset="0" stop-color="#5fe0c0"/><stop offset=".5" stop-color="#9d8cff"/><stop offset="1" stop-color="#e46ccc"/></linearGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#ffffff" stroke-opacity=".045"/></pattern>
<clipPath id="c"><rect width="840" height="300" rx="24"/></clipPath>
</defs>
<g clip-path="url(#c)">
<rect width="840" height="300" fill="#0b0f17"/>
<circle class="o1" cx="120" cy="60" r="240" fill="url(#g1)"/>
<circle class="o2" cx="760" cy="80" r="260" fill="url(#g2)"/>
<circle class="o3" cx="520" cy="300" r="260" fill="url(#g3)"/>
<rect width="840" height="300" fill="url(#grid)"/>
</g>
<g class="f1"><image href="{logo('inSpeak',128)}" x="600" y="34" width="112" height="112"/></g>
<g class="f2"><image href="{logo('inFlows',128)}" x="700" y="120" width="96" height="96"/></g>
<g class="f3"><image href="{logo('usageWatch',128)}" x="572" y="160" width="88" height="88"/></g>
<rect x=".75" y=".75" width="838.5" height="298.5" rx="23.5" fill="none" stroke="#ffffff" stroke-opacity=".12" stroke-width="1.5"/>
<text x="48" y="84" class="s">Cześć <tspan class="wave">👋</tspan>  I&#8217;m</text>
<text x="44" y="146" class="h">Kamil Szpak</text>
<text x="48" y="196" class="s">and I build</text>{rot}
<text x="48" y="256" class="m">~/presoon $ <tspan class="p" fill="#e6edf3">ls ./shipping</tspan>  →  <tspan fill="#e46ccc">inSpeak</tspan>  <tspan fill="#5fe0c0">inFlows</tspan>  <tspan fill="#9d8cff">UsageWatch</tspan><tspan class="cur" fill="#e6edf3"> ▍</tspan></text>
</svg>'''
(OUT / "header.svg").write_text(header, encoding="utf-8")
print("ok", [p.name for p in OUT.iterdir()])
