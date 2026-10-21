from __future__ import annotations

import random
from datetime import datetime, timezone
from typing import Any

import numpy as np

from .config import CONFIG
from .message_bus import MessageBus
from .models import NeuroSymbolicMessage, NeuralComponent, QuantitativeAssertion, SymbolicClaim
from .quantum import QuantumAdapter


class BaseBrain:
    def __init__(self, name: str, bus: MessageBus, quantum: QuantumAdapter | None = None):
        self.name = name
        self.bus = bus
        self.quantum = quantum or QuantumAdapter()
        self.state = "idle"
        self.confidence = 0.55
        self.throughput = 0
        self.last_update = datetime.now(timezone.utc).isoformat()
        self.message_counter = 0

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _neural_payload(self, embedding: list[float], uncertainty: list[float], confidence: float) -> NeuralComponent:
        return NeuralComponent(
            embedding=embedding,
            attention_map=[[0.05 * (i + 1) for i in range(6)] for _ in range(6)],
            latent_trajectory=[float(x) for x in np.linspace(0.0, 1.0, len(embedding))],
            uncertainty_tensor=uncertainty,
            projection_dim=len(embedding),
            confidence=confidence,
        )

    def _make_message(
        self,
        receiver: str,
        message_type: str,
        claims: list[SymbolicClaim],
        quant: list[QuantitativeAssertion],
        embedding: list[float],
        uncertainty: list[float],
        confidence: float,
        priority: int = CONFIG.default_priority,
        quantum_summary=None,
        metadata: dict[str, Any] | None = None,
    ) -> NeuroSymbolicMessage:
        self.message_counter += 1
        self.throughput += 1
        self.last_update = self._now()
        self.state = "active"
        return NeuroSymbolicMessage(
            message_id=f"{self.name}-{receiver}-{self.message_counter}-{self._now()}",
            timestamp=self._now(),
            sender=self.name,
            receiver=receiver,
            priority=priority,
            requires_ack=False,
            message_type=message_type,
            neural_component=self._neural_payload(embedding, uncertainty, confidence),
            symbolic_component=claims,
            quantitative_component=quant,
            metadata=metadata or {},
            quantum_summary=quantum_summary,
        )

    async def emit(self, message: NeuroSymbolicMessage) -> None:
        await self.bus.publish(message)


class PerceptionBrain(BaseBrain):
    async def tick(self, step: int) -> None:
        trend = 0.5 + 0.3 * math.sin(step / 6)
        liquidity = 0.6 + 0.2 * math.cos(step / 8)
        funding = 0.65 + 0.15 * math.sin(step / 4)
        flow = 0.55 + 0.25 * math.cos(step / 7)

        embedding = [trend, liquidity, funding, flow, 0.75, 0.5, 0.8, 0.6]
        uncertainty = [0.1, 0.12, 0.14, 0.18, 0.1]

        claims = [
            SymbolicClaim(
                claim_id=f"{self.name}-regime-{step}",
                kind="regime",
                statement="Volatility expansion regime is strengthening and liquidity is thinning.",
                confidence=0.82,
                sources=["orderbook", "funding", "liquidations"],
                proof_trace=["funding_rate_elevated", "liquidity_spread_widening"],
            ),
            SymbolicClaim(
                claim_id=f"{self.name}-causal-{step}",
                kind="causal",
                statement="Funding persistence is increasing the probability of forced liquidation cascades.",
                confidence=0.74,
                sources=["funding_rate", "open_interest"],
                proof_trace=["oi_growth", "liquidation_sentiment"],
            ),
        ]

        quant = [
            QuantitativeAssertion(
                name="liquidity_pressure",
                metric="zscore",
                mean=0.0,
                std=0.25,
                value_of_information=0.84,
                distribution_summary={"low": 0.2, "mid": 0.5, "high": 0.3},
            ),
            QuantitativeAssertion(
                name="funding_regime",
                metric="funding_rate",
                mean=funding,
                std=0.12,
                value_of_information=0.79,
                distribution_summary={"normal": 0.37, "elevated": 0.43, "extreme": 0.2},
            ),
        ]

        msg = self._make_message(
            receiver="research",
            message_type="hybrid",
            claims=claims,
            quant=quant,
            embedding=embedding,
            uncertainty=uncertainty,
            confidence=0.81,
            metadata={"market_state": "risk-on_volatility_expansion", "source": "multi_modal_fusion"},
        )
        await self.emit(msg)


class ResearchBrain(BaseBrain):
    async def tick(self, step: int) -> None:
        hypothesis = 0.7 + 0.2 * math.sin(step / 5)
        causal_strength = 0.6 + 0.25 * math.cos(step / 4)
        embedding = [hypothesis, causal_strength, 0.9, 0.7, 0.8, 0.5, 0.6, 0.75]
        uncertainty = [0.09, 0.11, 0.15, 0.08, 0.13]

        claims = [
            SymbolicClaim(
                claim_id=f"{self.name}-hypothesis-{step}",
                kind="hypothesis",
                statement="Funding expansion is likely driving a short-term distribution regime before a structural reversal.",
                confidence=0.77,
                sources=["market_reality_engine", "historical_patterns"],
                proof_trace=["phase_shift_detected", "liquidity_tail_event"],
            ),
            SymbolicClaim(
                claim_id=f"{self.name}-causal-graph-{step}",
                kind="causal",
                statement="Funding -> OI concentration -> liquidation cascade -> volatility expansion is the dominant chain.",
                confidence=0.8,
                sources=["causal_graph"],
                proof_trace=["causal_edge_funding_oi", "causal_edge_liquidation_volatility"],
            ),
        ]

        quantum = None
        if step % 4 == 0:
            q = self.quantum.estimate_expectation("regime_kernel_score", embedding)
            quantum = q

        quant = [
            QuantitativeAssertion(
                name="hypothesis_rank",
                metric="confidence_score",
                mean=0.72,
                std=0.14,
                value_of_information=0.88,
                distribution_summary={"weak": 0.18, "moderate": 0.45, "strong": 0.37},
            ),
            QuantitativeAssertion(
                name="causal_divergence",
                metric="kl",
                mean=0.26,
                std=0.08,
                kl_divergence=0.26,
                value_of_information=0.69,
                distribution_summary={"low": 0.2, "mid": 0.6, "high": 0.2},
            ),
        ]

        message_type = "quantum_assisted" if quantum else "hybrid"
        msg = self._make_message(
            receiver="decision",
            message_type=message_type,
            claims=claims,
            quant=quant,
            embedding=embedding,
            uncertainty=uncertainty,
            confidence=0.78,
            priority=7 if quantum else 5,
            quantum_summary=quantum,
            metadata={"quantum_used": quantum is not None, "objective": "regime_hypothesis_rank"},
        )
        await self.emit(msg)


class DecisionBrain(BaseBrain):
    async def tick(self, step: int) -> None:
        capital = 0.55 + 0.2 * math.sin(step / 5)
        risk = 0.7 + 0.1 * math.cos(step / 6)
        embedding = [capital, risk, 0.4, 0.75, 0.8, 0.6, 0.5, 0.9]
        uncertainty = [0.16, 0.12, 0.14, 0.18, 0.2]

        claims = [
            SymbolicClaim(
                claim_id=f"{self.name}-decision-{step}",
                kind="constraint",
                statement="Reduce beta exposure and maintain strict downside protection under elevated liquidation risk.",
                confidence=0.86,
                sources=["risk_model", "volatility_regime"],
                proof_trace=["cvart_threshold", "liquidity_buffer"],
            ),
            SymbolicClaim(
                claim_id=f"{self.name}-forecast-{step}",
                kind="forecast",
                statement="Risk-adjusted allocation should bias toward defensive assets until volatility returns to baseline.",
                confidence=0.78,
                sources=["portfolio_optimizer"],
                proof_trace=["expected_shortfall_projection"],
            ),
        ]

        quant = [
            QuantitativeAssertion(
                name="portfolio_beta",
                metric="beta",
                mean=0.62,
                std=0.13,
                value_of_information=0.91,
                distribution_summary={"low": 0.35, "mid": 0.4, "high": 0.25},
            ),
            QuantitativeAssertion(
                name="expected_shortfall",
                metric="ES",
                mean=-0.18,
                std=0.07,
                value_of_information=0.9,
                distribution_summary={"mild": 0.37, "moderate": 0.46, "severe": 0.17},
            ),
        ]

        msg = self._make_message(
            receiver="meta",
            message_type="hybrid",
            claims=claims,
            quant=quant,
            embedding=embedding,
            uncertainty=uncertainty,
            confidence=0.87,
            priority=8,
            metadata={"decision": "defensive_rebalance", "risk_budget": "strict"},
        )
        await self.emit(msg)


class MetaBrain(BaseBrain):
    async def tick(self, step: int, bus: MessageBus) -> None:
        recent = bus.latest(10)
        disagreement_score = 0.26 + 0.12 * math.sin(step / 5)
        embedding = [disagreement_score, 0.7, 0.5, 0.8, 0.9, 0.4, 0.6, 0.75]
        uncertainty = [0.08, 0.1, 0.12, 0.15, 0.18]

        claims = [
            SymbolicClaim(
                claim_id=f"{self.name}-consensus-{step}",
                kind="constraint",
                statement="The system should surface the market-risk disagreement to the human operator with defensive framing.",
                confidence=0.88,
                sources=["inter_brain_dialogue"],
                proof_trace=["disagreement_detected", "risk_alignment"],
            )
        ]

        quant = [
            QuantitativeAssertion(
                name="disagreement_score",
                metric="risk_gap",
                mean=disagreement_score,
                std=0.09,
                value_of_information=0.84,
                distribution_summary={"low": 0.28, "medium": 0.42, "high": 0.3},
            )
        ]

        if recent:
            msg = self._make_message(
                receiver="decision",
                message_type="consensus" if disagreement_score < 0.5 else "disagreement",
                claims=claims,
                quant=quant,
                embedding=embedding,
                uncertainty=uncertainty,
                confidence=0.9,
                priority=9,
                metadata={"recent_messages": len(recent), "disagreement_score": round(disagreement_score, 4)},
            )
            await self.emit(msg)
