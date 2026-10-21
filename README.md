# Triune Quantum Crypto Brain

A production-minded Python prototype for a live multi-brain cryptocurrency intelligence system with neuro-symbolic messaging, layered research logic, and a real-time visual dashboard.

## Features

- Three primary AI brains: Perception, Research, Decision
- Optional fourth Meta brain for orchestration and memory
- Strict, versioned Pydantic message schema for inter-brain messaging
- Hybrid neural + symbolic + quantitative payloads
- Quantum subroutine interface for narrow hybrid workloads
- Real-time dashboard showing brain clusters, animated message traffic, disagreement states, and quantum links
- Replay-ready message bus and structured state summaries

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

Then open:

- http://localhost:8000

## Project structure

- app/models.py — Pydantic v2 message protocol
- app/quantum.py — quantum wrapper for hybrid subroutines
- app/message_bus.py — live inter-brain event stream
- app/brains.py — brain implementations and message generation logic
- app/simulator.py — orchestration loop and demo engine
- app/visualization.py — FastAPI dashboard + WebSocket
- app/main.py — entry point
- docs/architecture.md — system design and research notes

## Architecture summary

The system behaves like a connected cluster of specialist agents:

- Market Reality Engine fuses market microstructure and social data into a probabilistic world model.
- Research Engine generates causal hypotheses and symbolic claims.
- Decision Engine produces risk-aware allocation decisions.
- Meta Brain oversees disagreement and surfaces the most important content.

All communication uses structured, versioned neuro-symbolic messages.

## Quantum note

This implementation includes a valid hybrid quantum-classical interface, but it is intentionally restricted to narrow, well-scoped tasks such as expectation estimation and kernel-style heuristic scoring. It does not claim generalized quantum advantage or full quantum neural networks.

## License

MIT
