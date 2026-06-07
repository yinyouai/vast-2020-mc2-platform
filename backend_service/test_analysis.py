import unittest

from app import app, build_analysis_engine
from core_engines.analysis_engine import ForensicAnalysisEngine


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
            all(
                item["occurrence_count"] == len(item["image_ids"]) >= 1
                for item in summary["final"]["evidence"]
            )
        )
        winner = summary["candidate_rankings"][0]
        component_total = sum(
            winner["score_components"][key]
            for key in ("specificity", "stability", "visual", "text")
        )
        self.assertAlmostEqual(component_total, winner["score"], delta=0.0002)
        self.assertGreater(winner["evidence_image_count"], 0)
        self.assertEqual(
            set(winner["score_factors"]),
            {"specificity", "stability", "visual", "text"},
        )
        comparison = next(
            item
            for item in summary["candidate_rankings"]
            if item["label"] == "blueSunglasses"
        )
        self.assertEqual(comparison["verified_image_count"], 0)
        self.assertEqual(comparison["score_components"]["visual"], 0)
        self.assertGreater(comparison["raw_detection_image_count"], 0)
        self.assertEqual(comparison["text_support_count"], 2)

    def test_audit_threshold_curve_covers_all_raw_predictions(self):
        engine = build_analysis_engine()
        audit = engine.model_audit()
        self.assertEqual(audit["audit_scope"], "all_detected_classes")
        self.assertNotIn("reviewed_class", audit)
        self.assertNotIn("comparison_class", audit)
        self.assertTrue(
            all(
                {
                    "retention_rate",
                    "class_coverage",
                    "person_coverage",
                    "retained_predictions",
                    "discarded_predictions",
                    "active_class_count",
                    "active_person_count",
                }
                <= set(row)
                for row in audit["threshold_curve"]
            )
        )
        first = audit["threshold_curve"][0]
        self.assertEqual(first["retained_predictions"], audit["total_predictions"])
        self.assertEqual(first["active_class_count"], audit["detected_class_count"])
        self.assertEqual(first["active_person_count"], audit["total_people"])

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

    def test_review_queue_is_candidate_driven(self):
        client = app.test_client()
        canada = client.get(
            "/api/review_queue?label=canadaPencil&score_threshold=0.45"
        ).get_json()
        glasses = client.get(
            "/api/review_queue?label=blueSunglasses&score_threshold=0.45"
        ).get_json()
        self.assertEqual(canada["candidate_label"], "canadaPencil")
        self.assertEqual(glasses["candidate_label"], "blueSunglasses")
        self.assertNotEqual(
            {item["id"] for item in canada["data"]},
            {item["id"] for item in glasses["data"]},
        )
        self.assertTrue(
            any(
                item["review_kind"] in {"evidence_search", "weak_model_hit"}
                for item in glasses["data"]
            )
        )
        self.assertTrue(
            any(item["review_kind"] == "model_hit" for item in glasses["data"])
        )
        glasses_all = client.get(
            "/api/review_queue?label=blueSunglasses"
            "&score_threshold=0.45&review_mode=all"
        ).get_json()
        glasses_next = client.get(
            "/api/review_queue?label=blueSunglasses"
            "&score_threshold=0.45&review_mode=focused&batch=2"
        ).get_json()
        self.assertLess(len(glasses["data"]), len(glasses_all["data"]))
        self.assertGreater(glasses["meta"]["max_batch"], 1)
        self.assertNotEqual(
            {
                item["id"] for item in glasses["data"]
                if item["review_kind"] in {"evidence_search", "weak_model_hit"}
            },
            {
                item["id"] for item in glasses_next["data"]
                if item["review_kind"] in {"evidence_search", "weak_model_hit"}
            },
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

    def test_threshold_changes_model_hits_not_verified_evidence(self):
        client = app.test_client()
        low = client.get("/api/analysis_summary?score_threshold=0.25").get_json()["data"]
        high = client.get("/api/analysis_summary?score_threshold=0.75").get_json()["data"]
        low_rows = {item["label"]: item for item in low["candidate_rankings"]}
        high_rows = {item["label"]: item for item in high["candidate_rankings"]}
        self.assertEqual(low["candidate_scoring"]["score_threshold"], 0.25)
        self.assertEqual(high["candidate_scoring"]["score_threshold"], 0.75)
        self.assertGreaterEqual(
            low_rows["blueSunglasses"]["raw_detection_image_count"],
            high_rows["blueSunglasses"]["raw_detection_image_count"],
        )
        self.assertEqual(
            low_rows["blueSunglasses"]["verified_image_count"],
            high_rows["blueSunglasses"]["verified_image_count"],
        )
        self.assertEqual(
            low_rows["blueSunglasses"]["score"],
            high_rows["blueSunglasses"]["score"],
        )

    def test_candidate_evidence_sources_are_separated(self):
        engine = build_analysis_engine()
        summary = engine.analysis_summary(0.45)
        rows = {item["label"]: item for item in summary["candidate_rankings"]}
        for label, label_node in engine.corrected_labels.items():
            expected_verified = sum(
                len(set(person_node.get("image_ids", [])))
                for person_node in label_node.get("persons", {}).values()
            )
            self.assertEqual(rows[label]["verified_image_count"], expected_verified)
            self.assertEqual(rows[label]["evidence_image_count"], expected_verified)
            self.assertLessEqual(
                rows[label]["text_support_count"],
                rows[label]["owner_count"],
            )

        expected_images = sum(
            len(person.get("images", {}))
            for person in engine.master_data.values()
        )
        self.assertEqual(
            summary["candidate_scoring"]["data_scope"]["image_count"],
            expected_images,
        )

    def test_review_priorities_are_ranked_and_explainable(self):
        response = app.test_client().get("/api/review_priorities")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()["data"]
        people = payload["people"]
        self.assertTrue(people)
        self.assertEqual(
            [item["score"] for item in people],
            sorted((item["score"] for item in people), reverse=True),
        )
        self.assertTrue(
            all(
                item["reasons"]
                and item["recommended_case_id"]
                and set(item["contributions"]) == {
                    "uncertainty",
                    "overlap",
                    "coverage_gap",
                    "label_instability",
                    "data_quality",
                }
                for item in people
            )
        )

    def test_review_priorities_do_not_use_human_corrections(self):
        engine = build_analysis_engine()
        raw_only_engine = ForensicAnalysisEngine(
            engine.master_data,
            {"target_group_size": 8, "corrected_labels": {}, "rejected_predictions": []},
            engine.training_labels,
        )
        self.assertEqual(
            engine.person_review_priorities(),
            raw_only_engine.person_review_priorities(),
        )


if __name__ == "__main__":
    unittest.main()
