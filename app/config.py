from pydantic import BaseModel, Field
from typing import Any, Literal

MESSAGE_SCHEMA_VERSION = "1.0.0"

class NeuralComponent(BaseModel):
    embedding: list[float]
    attention_map: list[list[float]] = Field(default_factory=list)
    latent_trajectory: list[float] = Field(default_factory=list)
    uncertainty_tensor: list[float] = Field(default_factory=list)
    projection_dim: int = 0
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

class SymbolicClaim(BaseModel):
    claim_id: str
    kind: Literal["causal", "regime", "hypothesis", "constraint", "contradiction", "forecast"]
    statement: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    sources: list[str] = Field(default_factory=list)
    proof_trace: list[str] = Field(default_factory=list)

class QuantitativeAssertion(BaseModel):
    name: str
    metric: str
    mean: float | None = None
    std: float | None = None
    variance: float | None = None
    skew: float | None = None
    kurtosis: float | None = None
    wasserstein: float | None = None
    kl_divergence: float | None = None
    value_of_information: float | None = None
    distribution_summary: dict[str, float] = Field(default_factory=dict)

class QuantumSummary(BaseModel):
    used: bool = False
    backend: str | None = None
    circuit_type: str | None = None
    qubits: int | None = None
    objective: str | None = None
    expected_value: float | None = None
    notes: str | None = None

class NeuroSymbolicMessage(BaseModel):
    message_id: str
    schema_version: str = MESSAGE_SCHEMA_VERSION
    timestamp: str
    sender: str
    receiver: str
    priority: int = Field(default=1, ge=0)
    requires_ack: bool = False
    message_type: Literal["neural_only", "symbolic_only", "hybrid", "quantum_assisted", "disagreement", "consensus"]
    neural_component: NeuralComponent | None = None
    symbolic_component: list[SymbolicClaim] = Field(default_factory=list)
    quantitative_component: list[QuantitativeAssertion] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    quantum_summary: QuantumSummary | None = None

class BrainSnapshot(BaseModel):
    name: str
    state: str
    confidence: float
    throughput: int
    last_update: str
    active_claims: int
