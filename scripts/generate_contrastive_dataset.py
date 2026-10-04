#!/usr/bin/env python3
"""CLI Script to generate contrastive dataset pairs."""

import argparse
import sys
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rokai.curation import ContrastiveCurationPipeline


def main():
    parser = argparse.ArgumentParser(description="Generate contrastive dataset pairs for Sapna ROKAI")
    parser.add_argument("--pairs", type=int, default=1000, help="Total pairs to generate")
    parser.add_argument("--output", type=str, default="data", help="Output directory")
    parser.add_argument("--split", type=float, default=0.15, help="Held-out evaluation ratio")
    args = parser.parse_args()

    pipeline = ContrastiveCurationPipeline(output_dir=args.output)
    train_path, eval_path = pipeline.build_dataset(total_pairs=args.pairs, eval_split=args.split)
    print(f"\n✅ Dataset generated successfully:")
    print(f"  - Training:   {train_path}")
    print(f"  - Evaluation: {eval_path}\n")


if __name__ == "__main__":
    main()
