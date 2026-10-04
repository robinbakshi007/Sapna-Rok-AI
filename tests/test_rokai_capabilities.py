"""Comprehensive Verification Suite for All 5 Sapna ROKAI Core Capabilities."""

import os
import time
import unittest

from rokai.curation import ContrastiveCurationPipeline
from rokai.packaging import OllamaModelPackager
from rokai.router import ROKAI_TASK_ROUTING_SCHEMA, Sub100msTaskClassifier
from rokai.scoring import AppleSiliconMLXParallelScorer
from rokai.training import LoRARouterTrainer


class TestROKAICapabilities(unittest.TestCase):
    """Test suite validating all 5 capabilities at 100% completion."""

    def test_capability_1_sub_100ms_task_classification(self):
        """Capability 1: Sub-100ms Task Classification via single-pass logit projection."""
        classifier = Sub100msTaskClassifier()
        prompt = (
            "Refactor the authenticateSession function in session.ts to add structured audit logging "
            "and propagate correlation IDs to down-stream services."
        )
        result = classifier.classify(prompt)

        self.assertIn("decisions", result)
        self.assertIn("latency_ms", result)
        self.assertLess(result["latency_ms"], 100.0, "Classification latency must be under 100ms")
        self.assertEqual(result["decisions"]["task_type"], "INLINE_EDIT")
        self.assertFalse(result["decisions"]["contains_sensitive_data"])
        print(f"\n[Cap 1 Pass] Sub-100ms Classification Latency: {result['latency_ms']} ms")

    def test_capability_2_contrastive_synthetic_data(self):
        """Capability 2: 4-step contrastive synthetic data curation pipeline."""
        pipeline = ContrastiveCurationPipeline(output_dir="data")
        pair = pipeline.generate_contrastive_pair(domain="TypeScript/React", pair_id=1)

        self.assertIsNotNone(pair)
        self.assertIn("example_a", pair)
        self.assertIn("example_b", pair)
        self.assertNotEqual(pair["example_a"]["label"], pair["example_b"]["label"])

        # Test paired dataset building
        train_path, eval_path = pipeline.build_dataset(total_pairs=40, eval_split=0.2)
        self.assertTrue(train_path.exists())
        self.assertTrue(eval_path.exists())
        print(f"[Cap 2 Pass] Generated contrastive datasets: {train_path}, {eval_path}")

    def test_capability_3_single_epoch_lora_alignment(self):
        """Capability 3: Single-epoch LoRA alignment training execution."""
        trainer = LoRARouterTrainer({"output_dir": "models/test_adapter"})
        train_path = "data/train_contrastive_pairs.jsonl"
        self.assertTrue(os.path.exists(train_path))

        res = trainer.train(train_path)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["epochs_completed"], 1)
        self.assertTrue(os.path.exists(os.path.join(res["output_dir"], "adapter_config.json")))
        print(f"[Cap 3 Pass] 1-Epoch LoRA Alignment completed in {res['duration_sec']}s")

    def test_capability_4_apple_silicon_mlx_parallel_scoring(self):
        """Capability 4: Apple Silicon MLX parallel scoring with candidate projection."""
        scorer = AppleSiliconMLXParallelScorer()
        context = "Explain how the memory manager detects KV-cache memory leaks in unified memory."
        res = scorer.score_parallel_fields(context, ROKAI_TASK_ROUTING_SCHEMA)

        self.assertIn("output", res)
        self.assertIn("latency_ms", res)
        self.assertLess(res["latency_ms"], 100.0)
        self.assertEqual(res["output"]["task_type"], "EXPLAIN")
        print(f"[Cap 4 Pass] MLX Parallel Scorer Latency: {res['latency_ms']} ms (Engine: {res['engine']})")

    def test_capability_5_zero_code_ollama_packaging(self):
        """Capability 5: Zero-Code 1-token Ollama Modelfile packaging."""
        packager = OllamaModelPackager(model_name="sapna-router:latest")
        modelfile = packager.generate_modelfile(num_predict=1, temperature=1.0)

        self.assertTrue(modelfile.exists())
        content = modelfile.read_text()
        self.assertIn("PARAMETER num_predict 1", content)
        self.assertIn("PARAMETER temperature 1.0", content)
        print(f"[Cap 5 Pass] Ollama 1-Token Modelfile verified at: {modelfile}")


if __name__ == "__main__":
    unittest.main()
