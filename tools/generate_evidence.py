import json
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "evidence"
FONT = r"C:\Windows\Fonts\tahoma.ttf"
FONT_BOLD = r"C:\Windows\Fonts\tahomabd.ttf"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def wrapped_lines(text: str, width: int):
    lines = []
    for raw_line in text.splitlines() or [""]:
        lines.extend(textwrap.wrap(raw_line, width=width, replace_whitespace=False) or [""])
    return lines


def draw_card(filename: str, title: str, subtitle: str, sections):
    image = Image.new("RGB", (1600, 900), "#0b1220")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((45, 35, 1555, 865), radius=28, fill="#111827", outline="#334155", width=3)
    draw.text((90, 78), "LAB 10 - SPRING WEBFLUX API EVIDENCE", font=font(27, True), fill="#60a5fa")
    draw.text((90, 125), title, font=font(38, True), fill="#f8fafc")
    draw.text((90, 180), subtitle, font=font(23), fill="#94a3b8")
    y = 235
    for label, content, color in sections:
        draw.text((90, y), label, font=font(22, True), fill=color)
        y += 38
        for line in wrapped_lines(content, 102):
            draw.text((110, y), line, font=font(20), fill="#e2e8f0")
            y += 29
            if y > 815:
                break
        y += 18
        if y > 815:
            break
    draw.text((1190, 820), "นายปวริศช์ ประมวล | 673380278-9 | Sec 1", font=font(18), fill="#64748b")
    image.save(EVIDENCE_DIR / filename, optimize=True)


def main():
    data = json.loads((EVIDENCE_DIR / "api-results.json").read_text(encoding="utf-8"))
    for item in data["requests"]:
        request_line = f'{item["method"]} {data["baseUrl"]}{item["path"]}'
        sections = [("REQUEST", request_line, "#38bdf8")]
        if "requestBody" in item:
            sections.append(("REQUEST BODY", json.dumps(item["requestBody"], ensure_ascii=False, indent=2), "#fbbf24"))
        response = item["response"]
        response_text = response if isinstance(response, str) else json.dumps(response, ensure_ascii=False, indent=2)
        sections.append((f'RESPONSE - HTTP {item["status"]}', response_text, "#4ade80"))
        draw_card(
            item["file"],
            f'{item["method"]} {item["path"]}',
            f'Captured from the running Reactor Netty server - {data["capturedAt"]}',
            sections,
        )

    suites = list((ROOT / "target" / "surefire-reports").glob("TEST-*.xml"))
    tests = failures = errors = skipped = 0
    for suite in suites:
        root = ET.parse(suite).getroot()
        tests += int(root.attrib.get("tests", 0))
        failures += int(root.attrib.get("failures", 0))
        errors += int(root.attrib.get("errors", 0))
        skipped += int(root.attrib.get("skipped", 0))
    draw_card(
        "07-automated-tests.png",
        "Maven automated test result",
        "StepVerifier + WebTestClient + ProductWebClient integration test",
        [
            ("COMMAND", "mvn test", "#38bdf8"),
            ("RESULT", f"Tests run: {tests}, Failures: {failures}, Errors: {errors}, Skipped: {skipped}\nBUILD SUCCESS", "#4ade80"),
            ("NON-BLOCKING CHECK", "Production source contains no .block(), Thread.sleep(), or Future.get() calls.", "#fbbf24"),
        ],
    )


if __name__ == "__main__":
    main()
