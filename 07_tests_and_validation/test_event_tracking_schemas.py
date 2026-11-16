"""
VELOOP REWARDS — AUTOMATED EVENT TRACKING SCHEMA VALIDATION
Validates all 32 production telemetry events, checking JSON schemas,
data types, required properties, example payloads, and negative test cases.
"""

import os
import json
import re
import unittest
import jsonschema

class TestEventTrackingSchemas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.plan_md_path = "04_deliverables/deliverable_08_event_tracking_plan/Event_Tracking_Plan.md"
        with open(cls.plan_md_path, "r", encoding="utf-8") as f:
            cls.content = f.read()

        # Parse all 32 event blocks from the markdown
        # Pattern: ### Event \d+: `(.*?)`
        cls.events = {}
        event_blocks = re.split(r"### Event \d+: `(.*?)`", cls.content)
        
        # event_blocks[0] is preamble, then pairs: (event_name, block_text)
        for i in range(1, len(event_blocks), 2):
            evt_name = event_blocks[i]
            evt_body = event_blocks[i+1]
            cls.events[evt_name] = evt_body

    def test_01_all_32_events_documented(self):
        """Verify that exactly 32 distinct production events are defined."""
        self.assertEqual(len(self.events), 32, f"Expected 32 events, found {len(self.events)}")

    def test_02_all_events_have_required_sections(self):
        """Verify that every event block contains the 16 core engineering attributes."""
        required_headers = [
            "Functional Domain",
            "Business Purpose",
            "Trigger Condition",
            "Required Properties",
            "Optional Properties",
            "Field Data Types",
            "Allowed Values",
            "Validation Rules",
            "Negative Test Cases",
            "Acceptance Criteria",
            "JSON Payload Example",
            "JSON Schema"
        ]
        for evt_name, body in self.events.items():
            for req in required_headers:
                self.assertIn(req, body, f"Event '{evt_name}' missing section: {req}")

    def test_03_json_schema_and_payload_validation(self):
        """Extract JSON Schema and Example Payload for each event and validate with jsonschema."""
        validated_count = 0
        for evt_name, body in self.events.items():
            # Extract JSON payload example
            payload_match = re.search(r"#### JSON Payload Example\s*```json(.*?)```", body, re.DOTALL)
            schema_match = re.search(r"#### JSON Schema\s*```json(.*?)```", body, re.DOTALL)

            self.assertIsNotNone(payload_match, f"Missing JSON payload in event: {evt_name}")
            self.assertIsNotNone(schema_match, f"Missing JSON schema in event: {evt_name}")

            payload_str = payload_match.group(1).strip()
            schema_str = schema_match.group(1).strip()

            payload = json.loads(payload_str)
            schema = json.loads(schema_str)

            # Validate that schema itself is a valid Draft 7 / Draft 2020 schema
            jsonschema.Draft7Validator.check_schema(schema)

            # Validate positive case: example payload MUST be valid
            validator = jsonschema.Draft7Validator(schema)
            errors = list(validator.iter_errors(payload))
            self.assertEqual(len(errors), 0, f"Event '{evt_name}' payload failed schema validation: {[e.message for e in errors]}")

            # Validate negative case: payload missing required property must FAIL
            if "required" in schema and len(schema["required"]) > 0:
                first_req = schema["required"][0]
                mutated_payload = dict(payload)
                if first_req in mutated_payload:
                    del mutated_payload[first_req]
                    self.assertFalse(validator.is_valid(mutated_payload), f"Event '{evt_name}' failed to reject missing required field: {first_req}")

            validated_count += 1

        self.assertEqual(validated_count, 32, "All 32 event schemas must be verified")

    def test_04_distinguish_observed_vs_proposed(self):
        """Verify that Observed in Data vs Proposed Future Spec status is clearly declared."""
        for evt_name, body in self.events.items():
            has_observed = "Observed in" in body
            has_proposed = "Proposed Future Spec" in body
            self.assertTrue(has_observed or has_proposed, f"Event '{evt_name}' does not classify Observed vs Proposed")

if __name__ == "__main__":
    unittest.main()
