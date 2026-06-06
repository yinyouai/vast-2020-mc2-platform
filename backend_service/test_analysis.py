import unittest

from app import app, build_analysis_engine


EXPECTED_GROUP = [
    "Person4",
    "Person7",
    "Person14",
    "Person15",
    "Person22",
    "Person25",
    "Person35",
    "Person39",
]


class AnalysisEngineTests(unittest.TestCase):
    def test_invalidated_raw_hypothesis(self):
        hypothesis = build_analysis_engine().raw_hypothesis()
        self.assertEqual(hypothesis["status"], "invalidated")
        self.assertEqual(len(hypothesis["detections"]), 12)
        self.assertTrue(all(item["rejected"] for item in hypothesis["detections"]))

    def test_final_group_is_derived_from_candidate_rules(self):
        summary = build_analysis_engine().analysis_summary()
        self.assertEqual(summary["final"]["totem"], "canadaPencil")
        self.assertEqual(summary["final"]["group"], EXPECTED_GROUP)
        self.assertEqual(len(summary["final"]["evidence"]), 8)
        self.assertTrue(
            all(item["occurrence_count"] >= 2 for item in summary["final"]["evidence"])
        )
        winner = summary["candidate_rankings"][0]
        component_total = sum(
            winner["score_components"][key]
            for key in ("specificity", "stability", "visual", "text")
        )
        self.assertAlmostEqual(component_total, winner["score"], places=4)

    def test_audit_labels_follow_derived_candidates(self):
        engine = build_analysis_engine()
        audit = engine.model_audit()
        hypothesis = engine.raw_hypothesis()
        self.assertEqual(audit["reviewed_class"], engine.candidate_rankings()[0]["label"])
        self.assertEqual(audit["comparison_class"], hypothesis["label"])
        self.assertEqual(hypothesis["owner_count"], engine.target_size)
        self.assertTrue(
            all(
                {"precision", "recall", "f1", "predicted_owners", "comparison_owners"}
                <= set(row)
                for row in audit["threshold_curve"]
            )
        )

    def test_review_queue_exposes_real_boxes(self):
        response = app.test_client().get("/api/review_queue")
        self.assertEqual(response.status_code, 200)
        queue = response.get_json()["data"]
        boxed = [item for item in queue if item["box_id"] >= 0]
        self.assertTrue(boxed)
        self.assertTrue(
            all(
                item["bbox"]
                and {"x", "y", "width", "height"} <= set(item["bbox"])
                for item in boxed
            )
        )

    def test_api_exposes_both_matrix_layers(self):
        client = app.test_client()
        for source in ("raw", "corrected"):
            response = client.post(
                "/api/distribution_matrix",
                json={"data_source": source, "score_threshold": 0.55},
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["data_source"], source)


if __name__ == "__main__":
    unittest.main()
