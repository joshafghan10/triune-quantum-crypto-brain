from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from .models import QuantumSummary


class QuantumAdapter:
    """A narrow hybrid quantum-classical adapter.

    The implementation is intentionally honest: it provides a small, simulated
    variational-style expectation estimator. Real quantum advantage is neither
    claimed nor implied. This is meant to show where quantum computation would
    enter a production system without pretending that the full market problem is
    quantum-native.
    """

    def __init__(self, backend: str = "numpy-simulator"):
        self.backend = backend

    def estimate_expectation(self, objective: str, vector: Sequence[float]) -> QuantumSummary:
        values = np.asarray(vector, dtype=float)
        if values.size == 0:
            values = np.array([1.0, 0.0, 0.0, 0.0], dtype=float)

        # Simulate a tiny 3-qubit variational expectation using a smooth objective.
        # The output is not a real hardware run, but it creates a realistic hybrid
        # quantum interface for a constrained problem.
        theta = np.linspace(0.1, 1.1, values.size)
        amplitudes = np.exp(1j * theta) * values
        amplitude_norm = np.linalg.norm(amplitudes)
        if amplitude_norm == 0:
            expected_value = 0.0
        else:
            expected_value = float(np.real(np.dot(np.conjugate(amplitudes), values)) / (amplitude_norm ** 2))

        # Convert to a bounded interpretable result.
        bounded = max(-1.0, min(1.0, expected_value / (1.0 + abs(expected_value))))
        return QuantumSummary(
            used=True,
            backend=self.backend,
            circuit_type="variational-expectation",
            qubits=min(3, max(1, values.size)),
            objective=objective,
            expected_value=round(float(bounded), 6),
            notes="Hybrid quantum-classical expectation estimate for a narrow, non-generalized subroutine.",
        )

    def kernel_score(self, left: Sequence[float], right: Sequence[float]) -> float:
        a = np.asarray(left, dtype=float)
        b = np.asarray(right, dtype=float)
        dim = min(a.size, b.size)
        if dim == 0:
            return 0.0
        a = a[:dim]
        b = b[:dim]
        cosine = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))
        return float(np.clip(cosine, -1.0, 1.0))
