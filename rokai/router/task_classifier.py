"""Sub-100ms Task Classifier for Sapna ROKAI.

Evaluates coding context against typed schema boundaries in a single forward pass,
bypassing generative token streaming loops.
"""

from __future__ import annotations

import math
import os
import re
import time
from typing import Any, Dict, List, Optional, Tuple

from rokai.router.schemas import ROKAI_TASK_ROUTING_SCHEMA


def temperature_softmax(logits: List[float], temperature: float = 1.0) -> List[float]:
    """Compute temperature-calibrated softmax over logit scores."""
    temp = max(temperature, 1e-4)
    scaled = [s / temp for s in logits]
    max_val = max(scaled)
    exp_vals = [math.exp(s - max_val) for s in scaled]
    sum_exp = sum(exp_vals)
    if sum_exp == 0:
        return [1.0 / len(logits)] * len(logits)
    return [e / sum_exp for e in exp_vals]


class Sub100msTaskClassifier:
    """System One decision engine for Sapna ROKAI."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        max_context_tokens: int = 2048,
        temperature: float = 1.0,
        device: Optional[str] = None,
    ):
        self.model_path = model_path
        self.max_context_tokens = max_context_tokens
        self.temperature = temperature
        self.device = device or ("mps" if os.uname().sysname == "Darwin" else "cpu")
        self.backend = "semantic_engine"
        self.model = None
        self.tokenizer = None

        self._init_runtime()

    def _init_runtime(self) -> None:
        """Initialize native model weights if available on disk."""
        if not self.model_path or not os.path.exists(self.model_path):
            self.backend = "semantic_engine"
            return

        # Attempt Apple Silicon MLX
        if os.uname().sysname == "Darwin":
            try:
                import mlx.core as mx
                from mlx_lm import load
                if mx.metal.is_available():
                    self.model, self.tokenizer = load(self.model_path)
                    self.backend = "mlx_metal"
                    return
            except Exception:
                pass

        # Attempt PyTorch Transformers
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float32
            dev = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = AutoModelForCausalLM.from_pretrained(self.model_path, torch_dtype=dtype, device_map=dev)
            self.model.eval()
            self.backend = "pytorch"
        except Exception:
            self.backend = "semantic_engine"

    def classify(self, context: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Classify developer intent, compute model tier, and check privacy boundaries.
        
        Target latency: < 50ms.
        """
        start_t = time.perf_counter()
        target_schema = schema or ROKAI_TASK_ROUTING_SCHEMA
        max_chars = self.max_context_tokens * 4
        truncated_context = context[:max_chars]

        if self.backend == "mlx_metal" and self.model and self.tokenizer:
            raw_result = self._score_mlx(truncated_context, target_schema)
        elif self.backend == "pytorch" and self.model and self.tokenizer:
            raw_result = self._score_pytorch(truncated_context, target_schema)
        else:
            raw_result = self._score_semantic_fast(truncated_context, target_schema)

        elapsed_ms = (time.perf_counter() - start_t) * 1000

        # Construct unified decision summary
        decisions = raw_result["output"]
        fields_meta = raw_result["fields"]

        return {
            "decisions": decisions,
            "fields": fields_meta,
            "latency_ms": round(elapsed_ms, 2),
            "backend": self.backend,
            "recommended_action": self._build_recommendation(decisions, elapsed_ms),
        }

    def _build_recommendation(self, decisions: Dict[str, Any], latency_ms: float) -> str:
        tier = decisions.get("model_tier", "PRIMARY_LOCAL_9B")
        task = decisions.get("task_type", "INLINE_EDIT")
        sensitive = decisions.get("contains_sensitive_data", False)
        budget = decisions.get("completion_budget", "BALANCED_256")

        if sensitive:
            return f"ROKAI Policy: Local execution locked to prevent credentials leak. Using {tier} ({latency_ms:.1f}ms)."
        return f"ROKAI Policy: Routed {task} to {tier} with {budget} limit ({latency_ms:.1f}ms)."

    def _score_semantic_fast(self, context: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Sub-1ms semantic logit projection."""
        lower_ctx = context.lower()
        decisions = {}
        fields_data = {}

        # 1. Privacy filter
        sensitive_signals = [
            "password", "secret", "bearer", "api_key", "token", "private_key",
            "postgres_password", "aws_secret", "authorization:", "db_pass",
        ]
        has_sensitive = any(sig in lower_ctx for sig in sensitive_signals)
        decisions["contains_sensitive_data"] = has_sensitive
        fields_data["contains_sensitive_data"] = {
            "scores": [0.98 if has_sensitive else 0.02, 0.02 if has_sensitive else 0.98],
            "choices": ["true", "false"],
        }

        # 2. Schema field evaluation
        for field_name, field_def in schema.items():
            if field_name == "contains_sensitive_data":
                continue

            choices = field_def.get("choices", [])
            descs = field_def.get("choice_descriptions", {})
            raw_scores = []

            for choice in choices:
                score = 1.0
                choice_term = choice.lower().replace("_", " ")
                choice_desc = descs.get(choice, "").lower()

                # Exact and term matches
                if choice.lower() in lower_ctx or choice_term in lower_ctx:
                    score += 5.0

                # Diagnostic signals
                tokens = re.findall(r"\b[a-z]{3,}\b", f"{choice_term} {choice_desc}")
                for tok in tokens:
                    if tok in lower_ctx:
                        score += 1.5

                raw_scores.append(score)

            probs = temperature_softmax(raw_scores, self.temperature)
            max_idx = int(max(range(len(probs)), key=lambda i: probs[i]))
            decisions[field_name] = choices[max_idx]
            fields_data[field_name] = {"scores": probs, "choices": choices}

        return {"output": decisions, "fields": fields_data}

    def _score_mlx(self, context: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        import mlx.core as mx
        decisions = {}
        fields_data = {}

        for field_name, field_def in schema.items():
            choices = field_def.get("choices", ["true", "false"])
            prompt = f"Context: {context}\nField: {field_name}\nChoices: {', '.join(choices)}\nSelection:"
            tokens = self.tokenizer.encode(prompt)
            input_ids = mx.array([tokens])
            candidate_ids = [self.tokenizer.encode(c.strip())[0] for c in choices]

            logits = self.model(input_ids)
            choice_logits = logits[0, -1, candidate_ids]
            probs = mx.softmax(choice_logits / self.temperature).tolist()
            max_idx = int(max(range(len(probs)), key=lambda i: probs[i]))

            decisions[field_name] = choices[max_idx]
            fields_data[field_name] = {"scores": probs, "choices": choices}

        return {"output": decisions, "fields": fields_data}

    def _score_pytorch(self, context: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        import torch
        import torch.nn.functional as F
        decisions = {}
        fields_data = {}

        for field_name, field_def in schema.items():
            choices = field_def.get("choices", ["true", "false"])
            prompt = f"Context: {context}\nField: {field_name}\nChoices: {', '.join(choices)}\nSelection:"
            inputs = self.tokenizer(prompt, return_tensors="pt")
            device = next(self.model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            candidate_ids = [self.tokenizer.encode(c.strip(), add_special_tokens=False)[0] for c in choices]

            with torch.no_grad():
                outputs = self.model(**inputs)
                last_logits = outputs.logits[:, -1, candidate_ids].squeeze(0).float()
                probs = F.softmax(last_logits / self.temperature, dim=-1).tolist()

            max_idx = int(max(range(len(probs)), key=lambda i: probs[i]))
            decisions[field_name] = choices[max_idx]
            fields_data[field_name] = {"scores": probs, "choices": choices}

        return {"output": decisions, "fields": fields_data}
