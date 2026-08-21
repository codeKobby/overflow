from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER_SCRIPT = ROOT / "shared" / "scripts" / "route_request.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RouterRoutingTests(unittest.TestCase):
    def make_root(self) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return Path(directory.name)

    def ready_root(self) -> Path:
        root = self.make_root()
        state = root / ".learning"
        state.mkdir()
        readiness = load_module("overflow_detect_readiness_for_routing", ROOT / "shared" / "scripts" / "detect_readiness.py")
        for filename in readiness.REQUIRED_FILES:
            (state / filename).write_text("{}\n" if filename == "progress.json" else "# State\n", encoding="utf-8")
        for dirname in readiness.REQUIRED_DIRS:
            (state / dirname).mkdir()
        return root

    def test_overflow_without_arguments_routes_to_next(self):
        module = load_module("overflow_route_request", ROUTER_SCRIPT)
        result = module.plan(self.make_root(), "/overflow")
        self.assertEqual(result["intent"], "orient")
        self.assertEqual(result["route"], "setup-learning")
        self.assertEqual(result["route_kind"], "initializer")
        self.assertEqual(result["continuation"]["resume_route"], "next")
        self.assertIn("run `/setup-learning` first", result["announcement"])

    def test_missing_state_announces_initializer_and_preserves_original_request(self):
        module = load_module("overflow_route_request_missing", ROUTER_SCRIPT)
        result = module.plan(self.make_root(), "/overflow teach the parser")
        self.assertEqual(result["route"], "setup-learning")
        self.assertTrue(result["requires_initialization"])
        self.assertTrue(result["continuation"]["resume_after_setup"])
        self.assertEqual(result["continuation"]["resume_route"], "teach")
        self.assertEqual(result["initializer"]["original_route"], "teach")
        self.assertIn("After setup", result["announcement"])

    def test_explain_can_continue_without_initialization(self):
        module = load_module("overflow_route_request_explain", ROUTER_SCRIPT)
        result = module.plan(self.make_root(), "/explain event loops")
        self.assertEqual(result["route"], "explain")
        self.assertEqual(result["route_kind"], "direct")
        self.assertFalse(result["requires_initialization"])
        self.assertTrue(result["can_continue_statelessly"])

    def test_initialized_quiz_routes_directly(self):
        module = load_module("overflow_route_request_ready", ROUTER_SCRIPT)
        result = module.plan(self.ready_root(), "/quiz day 1")
        self.assertEqual(result["route"], "quiz")
        self.assertEqual(result["route_kind"], "overflow")
        self.assertFalse(result["requires_initialization"])
        self.assertIn("/quiz", result["announcement"])

    def test_implementation_request_announces_specialist_inspection(self):
        module = load_module("overflow_route_request_specialist", ROUTER_SCRIPT)
        result = module.plan(self.make_root(), "/overflow build a React dashboard")
        self.assertEqual(result["route"], "handoff")
        self.assertEqual(result["route_kind"], "specialist-candidate")
        self.assertFalse(result["requires_initialization"])
        self.assertIn("specialist", result["announcement"])


if __name__ == "__main__":
    unittest.main()
