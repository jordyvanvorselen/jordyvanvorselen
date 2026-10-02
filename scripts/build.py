"""Build the profile README.

The README is markdown. Only the banner is an SVG. The Writing list refreshes
from the blog API on jordyvanvorselen.com, because Substack blocks GitHub's runners.
"""

import base64
import json
import urllib.request
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent.parent
USER = "jordyvanvorselen"
SITE = "https://jordyvanvorselen.com"
POSTS_URL = f"{SITE}/api/posts?limit=5&sort=-publicationDate&depth=0&where%5B_status%5D%5Bequals%5D=published"
MAX_POSTS = 5

SANS = "'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono',ui-monospace,Menlo,Consolas,monospace"
BG, CARD, LINE = "#030712", "#0b1220", "#1e293b"
TEXT, MUTED, DIM = "#f8fafc", "#94a3b8", "#64748b"
TEAL, BLUE, VIOLET, AMBER, ROSE = "#2dd4bf", "#60a5fa", "#a78bfa", "#fbbf24", "#fb7185"


# ---------------------------------------------------------------- badges

def data_logo(svg_body):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{svg_body}</svg>'
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


LINKEDIN = data_logo('<path fill="white" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.064 2.064 0 1 1 0-4.128 2.064 2.064 0 0 1 0 4.128zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>')
MAIL = data_logo('<path d="M3 5h18v14H3z" fill="none" stroke="white" stroke-width="2"/><path d="M3 6l9 7 9-7" fill="none" stroke="white" stroke-width="2"/>')
PI = data_logo('<path fill="white" d="M4 6h16v3h-3v10h-3V9h-4v10H7V9H4z"/>')


def badge(label, message, color, style="for-the-badge", logo=None, label_color="0b1220", alt=None):
    def part(text):
        return quote(text.replace("-", "--").replace("_", "__"), safe="")
    url = f"https://img.shields.io/badge/{part(label)}-{part(message)}-{color}?style={style}"
    if label_color:
        url += f"&labelColor={label_color}"
    if logo:
        url += "&logo=" + quote(logo, safe="") + "&logoColor=white"
    return f'<img src="{url}" alt="{escape(alt or f"{label} {message}".strip())}">'


def chip(text, color, logo=None):
    return badge("", text, color, style="flat-square", logo=logo, label_color=None, alt=text)


# ---------------------------------------------------------------- writing

def latest_posts():
    request = urllib.request.Request(POSTS_URL, headers={"User-Agent": "readme-builder"})
    with urllib.request.urlopen(request, timeout=30) as response:
        docs = json.load(response)["docs"]
    for doc in docs[:MAX_POSTS]:
        yield {
            "title": doc["title"].strip(),
            "subtitle": (doc.get("description") or "").strip(),
            "link": doc.get("canonicalUrl") or f"{SITE}/blog/{doc['slug']}",
            "date": datetime.fromisoformat(doc["publicationDate"].replace("Z", "+00:00")),
        }


def writing(posts):
    rows = ["| | Article | Published |", "|:-:|---|:-:|"]
    for i, post in enumerate(posts):
        marker = "🆕" if i == 0 else "📝"
        rows.append(f'| {marker} | **[{post["title"]}]({post["link"]})**<br><sub>{post["subtitle"]}</sub> | <sub>`{post["date"]:%d %b %Y}`</sub> |')
    return "\n".join(rows)


# ---------------------------------------------------------------- README

def readme(posts):
    top_badges = " ".join([
        badge("status", "open for teams", "14b8a6"),
        badge("focus", "AI-native delivery", "3b82f6"),
        badge("practice", "ATDD · CD · DDD", "a78bfa"),
        badge("hours", "EU & US time zones", "f59e0b"),
    ])
    domains = " ".join([
        chip("🔥 Fire safety", "e11d48"), chip("🔬 Semiconductors", "2563eb"), chip("💡 Consumer IoT", "7c3aed"),
        chip("☁️ B2B SaaS", "0d9488"), chip("🛠️ Developer platforms", "0284c7"), chip("👷 HR tech", "d97706"),
        chip("⚽ Fantasy sports", "059669"), chip("⛓️ Blockchain", "db2777"),
    ])
    ai_tools = " ".join([
        badge("", "Herdr", "0f172a", style="flat-square", label_color=None, alt="Herdr"),
        badge("", "Claude Code", "D97757", style="flat-square", logo="claude", label_color=None, alt="Claude Code"),
        badge("", "Codex", "10a37f", style="flat-square", label_color=None, alt="Codex"),
        badge("", "Pi", "7c3aed", style="flat-square", logo=PI, label_color=None, alt="Pi"),
        badge("", "APM", "0f766e", style="flat-square", label_color=None, alt="Agent Package Manager"),
        badge("", "and more", "334155", style="flat-square", label_color=None, alt="and more"),
    ])
    plugins = " ".join(
        f'<a href="https://github.com/{USER}/{name}">'
        + badge("pi", name, "7c3aed", style="flat-square", logo=PI, label_color="0b1220", alt=name) + "</a>"
        for name in ["pi-claude-rules", "pi-claude-hooks", "pi-bare-worktrees"]
    )
    def icons(ids, alt):
        return f'<img src="https://skillicons.dev/icons?i={ids}&theme=dark" height="44" alt="{alt}">'

    languages = icons("java,kotlin,ts,go,elixir,ruby,python,dart", "Java, Kotlin, TypeScript, Go, Elixir, Ruby, Python, Dart")
    frameworks = icons("spring,react,nextjs,rails,flutter", "Spring Boot, React, Next.js, Rails, Flutter")
    systems = icons("aws,azure,terraform,docker,kubernetes,githubactions,postgres,redis", "AWS, Azure, Terraform, Docker, Kubernetes, GitHub Actions, PostgreSQL, Redis")
    connect = " ".join([
        f'<a href="https://jordyvanvorselen.com">{badge("", "jordyvanvorselen.com", "0d9488", logo="googlechrome", label_color=None, alt="Website")}</a>',
        f'<a href="https://www.linkedin.com/in/jordy-van-vorselen">{badge("", "LinkedIn", "0a66c2", logo=LINKEDIN, label_color=None, alt="LinkedIn")}</a>',
        f'<a href="https://{USER}.substack.com">{badge("", "Substack", "ff6719", logo="substack", label_color=None, alt="Substack")}</a>',
        f'<a href="mailto:jordy@vanvorselen.com">{badge("", "jordy@vanvorselen.com", "7c3aed", logo=MAIL, label_color=None, alt="Email")}</a>',
    ])

    def npm(name):
        package = quote(f"@{USER}/{name}", safe="@/")
        return f'<img src="https://img.shields.io/npm/v/{package}?style=flat-square&color=7c3aed&label=npm" alt="npm version">'

    return f"""<p align="center">
  <img src="assets/banner.svg" width="100%" alt="Jordy van Vorselen, Freelance Lead Engineer. I make software teams ship faster. Measured, not vibes.">
</p>

<p align="center">
  {top_badges}
</p>

### I make the whole team ship faster.

Not by typing faster. By installing the rails that let a team **trust its own speed**:

- \u2705 &nbsp;**Acceptance tests** as the definition of correct
- \U0001f6a6 &nbsp;**CI that blocks slop** before a human reviews it
- \U0001f4e6 &nbsp;**Releases so small** they are boring

AI writes the code now.<br>
These rails decide where that speed goes: **to your users**, or into review queues and rework.

> [!TIP]
> **Hiring for a team that needs to go faster?** I measure where your delivery leaks, install the fix with your engineers, and prove it in numbers. → [jordy@vanvorselen.com](mailto:jordy@vanvorselen.com)

## 📈 Results, measured

<sub>From one of the teams I led, measured from its Git history:</sub>

<table>
<tr>
<td width="33%" align="center" valign="top">
<img src="assets/spacer.svg" width="250" height="1" alt="">

<img src="https://img.shields.io/badge/%F0%9F%9A%80%20releases-14b8a6?style=for-the-badge" alt="Releases">

# 9.9×

**More releases** per year

<sub>Next: multiple a day</sub>

</td>
<td width="33%" align="center" valign="top">
<img src="assets/spacer.svg" width="250" height="1" alt="">

<img src="https://img.shields.io/badge/%F0%9F%93%88%20throughput-3b82f6?style=for-the-badge" alt="Throughput">

# 2.5×

**More shipped** in 12 months

<sub>Same team size</sub>

</td>
<td width="33%" align="center" valign="top">
<img src="assets/spacer.svg" width="250" height="1" alt="">

<img src="https://img.shields.io/badge/%F0%9F%9B%A1%EF%B8%8F%20safety%20net-f59e0b?style=for-the-badge" alt="Safety net">

# 10,000+

**Automated tests**

<sub>Full suite green in 20 min</sub>

</td>
</tr>
</table>

<br>

<p align="center">
  <a href="https://www.jordyvanvorselen.com/experience"><img src="https://img.shields.io/badge/Full%20CV-all%20clients%20and%20case%20studies%20%E2%86%92-14b8a6?style=for-the-badge&labelColor=0b1220" alt="Full CV with all clients and case studies"></a>
</p>

## 🧰 Stack

**Concepts over syntax.** I go deep on architecture and hard technical problems. Languages are the easy part, especially with AI.

Shipped to production with:

<table>
  <tr><td width="240">🔤 <b>Languages</b></td><td>{languages}</td></tr>
  <tr><td>🧱 <b>Frameworks</b></td><td>{frameworks}</td></tr>
  <tr><td>⚙️ <b>Systems</b></td><td>{systems}</td></tr>
  <tr><td>🤖 <b>AI tooling I actually use</b></td><td>{ai_tools}</td></tr>
  <tr><td>🔌 <b>Harness plugins I authored</b></td><td>{plugins}</td></tr>
</table>

## ✍️ Writing

<!-- WRITING:START -->
{writing(posts)}
<!-- WRITING:END -->

## 📬 Connect

<p>
  {connect}
</p>

<br>

<p align="center">
  <i>“A language that doesn't affect the way you think about programming is not worth knowing.”</i>
  <br>
  <sub>Alan J. Perlis, first recipient of the Turing Award</sub>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:2dd4bf,50:60a5fa,100:a78bfa&height=110&section=footer" width="100%" alt="">
</p>
"""


def main():
    (ROOT / "README.md").write_text(readme(list(latest_posts())))


if __name__ == "__main__":
    main()
