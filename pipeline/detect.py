#!/usr/bin/env python3
"""Muestra 1 frame cada 2 s con ffmpeg y lo clasifica con Muse Spark Open.

Uso: python pipeline/detect.py clip.MOV
Env: MUSE_SPARK_API_KEY (o OPENAI_API_KEY), MUSE_SPARK_BASE_URL (o OPENAI_BASE_URL),
     MUSE_SPARK_MODEL (defecto: muse-spark-open).
Sale: runs/run-AAAAMMDD-HHMMSS.jsonl, una linea por frame.
Solo stdlib: no requiere pip install.
"""
import base64
import datetime
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

PROMPT = (
    'Responde SOLO con un JSON compacto {"event": true/false, "type": "...",'
    ' "confidence": 0-1, "facts": "..."}. Si no hay nada relevante usa'
    ' {"event": false, "type": "none", "confidence": 0, "facts": ""}.'
)


def call_model(b64_jpg, api_key, base_url, model):
    body = {
        "model": model,
        "reasoning_effort": "low",
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_jpg}",
                            "detail": "low",
                        },
                    },
                ],
            }
        ],
    }
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            raw = json.load(res)["choices"][0]["message"]["content"]
    finally:
        latency = time.perf_counter() - t0
    try:
        parsed = json.loads(raw)
    except (TypeError, ValueError):
        parsed = {"_raw": raw}
    return parsed, latency


def main():
    if len(sys.argv) != 2:
        print("Uso: python pipeline/detect.py clip.MOV", file=sys.stderr)
        sys.exit(2)
    clip = sys.argv[1]
    if not os.path.isfile(clip):
        print(f"No existe: {clip}", file=sys.stderr)
        sys.exit(2)
    api_key = os.environ.get("MUSE_SPARK_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("Falta MUSE_SPARK_API_KEY (o OPENAI_API_KEY).", file=sys.stderr)
        sys.exit(2)
    base_url = (
        os.environ.get("MUSE_SPARK_BASE_URL")
        or os.environ.get("OPENAI_BASE_URL")
        or "https://api.openai.com/v1"
    ).rstrip("/")
    model = (
        os.environ.get("MUSE_SPARK_MODEL")
        or os.environ.get("OPENAI_MODEL")
        or "muse-spark-open"
    )
    with tempfile.TemporaryDirectory() as tmp:
        try:
            subprocess.run(
                ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", clip,
                 "-vf", "fps=1/2", "-q:v", "3", f"{tmp}/frame-%06d.jpg"],
                check=True,
            )
        except FileNotFoundError:
            print("ffmpeg no encontrado en PATH.", file=sys.stderr)
            sys.exit(2)
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg fallo: {e}", file=sys.stderr)
            sys.exit(2)
        frames = sorted(f for f in os.listdir(tmp) if f.endswith(".jpg"))
        os.makedirs("runs", exist_ok=True)
        out = datetime.datetime.now().strftime("runs/run-%Y%m%d-%H%M%S.jsonl")
        with open(out, "w", encoding="utf-8") as fh:
            for i, name in enumerate(frames):
                with open(os.path.join(tmp, name), "rb") as img:
                    b64 = base64.b64encode(img.read()).decode()
                try:
                    resp, lat = call_model(b64, api_key, base_url, model)
                    row = {"t": i * 2.0, "frame": name, "latency_s": round(lat, 3),
                           "response": resp}
                except Exception as e:
                    row = {"t": i * 2.0, "frame": name, "latency_s": None,
                           "error": f"{type(e).__name__}: {e}"}
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                fh.flush()
                print(f"{row['t']:7.1f}s {name} -> {row.get('response', row.get('error'))}")
        print(f"OK: {len(frames)} frames -> {out}")


if __name__ == "__main__":
    main()
