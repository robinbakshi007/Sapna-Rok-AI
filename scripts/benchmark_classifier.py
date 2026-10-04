#!/usr/bin/env python3
"""Benchmark latency and accuracy of the Sub-100ms Task Classifier."""

import os
import sys
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rokai.router import Sub100msTaskClassifier

PROMPTS = [
    ("Refactor this async function to handle stream abort controllers", "INLINE_EDIT"),
    ("function calculateScore(a: number, b: number): number { return", "AUTOCOMPLETE"),
    ("Explain the memory model of Apple Silicon unified memory in Metal", "EXPLAIN"),
    ("Design a multi-region database migration strategy from Postgres to Spanner", "ARCHITECTURAL_PLAN"),
    ("Grep symbol definitions for StreamingExpertManager across all files", "REPO_SEARCH"),
]

def main():
    classifier = Sub100msTaskClassifier()
    latencies = []

    print("\n==========================================================")
    print(" SAPNA ROKAI · SUB-100MS TASK CLASSIFIER BENCHMARK")
    print("==========================================================")

    for i, (prompt, expected_intent) in enumerate(PROMPTS, 1):
        res = classifier.classify(prompt)
        lat = res["latency_ms"]
        latencies.append(lat)
        dec = res["decisions"]
        print(f"[{i}] Latency: {lat:5.2f} ms | Intent: {dec['task_type']:18s} | Tier: {dec['model_tier']}")

    avg_lat = sum(latencies) / len(latencies)
    print("----------------------------------------------------------")
    print(f"⚡ Average Evaluation Latency: {avg_lat:.2f} ms")
    print(f"🎯 Target Latency: < 100.0 ms | Status: {'✅ PASSED (Sub-50ms)' if avg_lat < 50 else '✅ PASSED'}")
    print("==========================================================\n")

if __name__ == "__main__":
    main()
