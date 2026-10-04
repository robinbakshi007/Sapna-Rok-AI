"""Task routing and classification schemas for Sapna ROKAI."""

from typing import Any, Dict

# Core schema for classifying developer requests into execution pathways
ROKAI_TASK_ROUTING_SCHEMA: Dict[str, Any] = {
    "task_type": {
        "type": "enum",
        "choices": ["AUTOCOMPLETE", "INLINE_EDIT", "EXPLAIN", "ARCHITECTURAL_PLAN", "REPO_SEARCH"],
        "description": "The exact developer intent of the incoming coding request.",
        "choice_descriptions": {
            "AUTOCOMPLETE": "Fast next-line completion, cursor token prediction, or bracket closing in <50ms.",
            "INLINE_EDIT": "Refactoring a function, fixing a bug, or applying diffs inside a single open file.",
            "EXPLAIN": "Explaining algorithmic logic, reviewing code comments, or architectural documentation.",
            "ARCHITECTURAL_PLAN": "Multi-file structural refactoring, system designs, scaffolding, or migrations.",
            "REPO_SEARCH": "Locating symbols, grep queries, finding references across the workspace.",
        },
    },
    "model_tier": {
        "type": "enum",
        "choices": ["FAST_LOCAL_1_5B", "PRIMARY_LOCAL_9B", "CLOUD_ESCALATION"],
        "description": "The optimal compute tier required based on complexity, reasoning depth, and context size.",
        "choice_descriptions": {
            "FAST_LOCAL_1_5B": "Qwen Coder 1.5B for instant autocomplete, syntax edits, and fast routing.",
            "PRIMARY_LOCAL_9B": "Qwen 3.5 9B for complex logic, multi-step refactoring, and unit test generation.",
            "CLOUD_ESCALATION": "Cloudflare Workers AI or OpenRouter when context exceeds local limits or cloud consent is given.",
        },
    },
    "completion_budget": {
        "type": "enum",
        "choices": ["TINY_32", "BALANCED_256", "DEEP_2048"],
        "description": "The upper bound token budget for the expected completion.",
        "choice_descriptions": {
            "TINY_32": "Short inline token snippets or completions.",
            "BALANCED_256": "Standard function implementation or patch.",
            "DEEP_2048": "Comprehensive module architecture or multi-file diff.",
        },
    },
    "contains_sensitive_data": {
        "type": "boolean",
        "description": "True if code payload contains private API keys, passwords, database credentials, or private PII.",
    },
}
