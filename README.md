# Linear-chain (gamma) delay — NiceGUI demo

This reproduces your Mathematica `Manipulate` for the k‑stage linear chain (Erlang/gamma delay) in Python with NiceGUI and a Matplotlib plot.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
# open http://localhost:8080
```

## Deploy on Fly.io

```bash
fly launch --no-deploy --copy-config --name YOUR_UNIQUE_APP_NAME
# If you already have an app name, skip launch and just ensure fly.toml has it.
fly deploy
```

Scale-to-zero & auto-start are enabled in `fly.toml`.
