from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from config import AppConfig
from core_engines.analysis_engine import ForensicAnalysisEngine
from core_engines.data_provider import DataProviderEngine


app = Flask(__name__)
CORS(app)


def build_analysis_engine():
    training_dir = AppConfig.IMAGE_ASSETS_DIR / "TrainingImages"
    training_labels = [
        path.name for path in training_dir.iterdir()
        if path.is_dir()
    ]
    return ForensicAnalysisEngine(
        DataProviderEngine.load_master_snapshot(),
        DataProviderEngine.load_corrections(),
        training_labels,
    )


@app.route("/static/MC2-Image-Data/<path:filename>")
def serve_images(filename):
    return send_from_directory(str(AppConfig.IMAGE_ASSETS_DIR), filename)


@app.route("/api/model_evaluation", methods=["GET"])
def get_model_evaluation():
    try:
        audit = build_analysis_engine().model_audit()
        return jsonify({
            "status": "success",
            "data": audit["confidence_statistics"],
            "audit": audit,
        })
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/distribution_matrix", methods=["POST"])
def get_distribution_matrix():
    try:
        payload = request.get_json() or {}
        threshold = float(payload.get("score_threshold", 0.25))
        excluded_items = list(payload.get("excluded_items", []))
        data_source = payload.get("data_source", "corrected")
        engine = build_analysis_engine()

        if data_source == "raw":
            suspects, items, matrix = engine.raw_matrix(threshold, excluded_items)
        else:
            suspects, items, matrix = engine.corrected_matrix(excluded_items)

        return jsonify({
            "status": "success",
            "data_source": data_source,
            "ordered_suspects": suspects,
            "ordered_items": items,
            "matrix_data": matrix,
        })
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/analysis_summary", methods=["GET"])
def get_analysis_summary():
    try:
        return jsonify({
            "status": "success",
            "data": build_analysis_engine().analysis_summary(),
        })
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/review_queue", methods=["GET"])
def get_review_queue():
    try:
        return jsonify({
            "status": "success",
            "data": build_analysis_engine().review_queue(),
        })
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/update_label", methods=["POST"])
def update_label():
    try:
        payload = request.get_json() or {}
        success = DataProviderEngine.apply_human_correction(
            person_id=payload.get("person_id"),
            image_id=payload.get("image_id"),
            box_id=int(payload.get("box_id", -1)),
            action=payload.get("action", ""),
            new_label=payload.get("new_label", ""),
            difficult=bool(payload.get("difficult", False)),
            note=payload.get("note", ""),
        )
        if not success:
            return jsonify({"status": "error", "message": "未找到对应图片或检测框"}), 404
        return jsonify({
            "status": "success",
            "message": "人工纠正已写入独立标注层",
            "analysis": build_analysis_engine().analysis_summary(),
        })
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.route("/api/export_analysis", methods=["GET"])
def export_analysis():
    try:
        result = build_analysis_engine().analysis_summary()
        DataProviderEngine.save_corrections(DataProviderEngine.load_corrections())
        with open(AppConfig.ANALYSIS_JSON_PATH, "w", encoding="utf-8") as stream:
            import json
            json.dump(result, stream, indent=2, ensure_ascii=False)
        return jsonify({
            "status": "success",
            "path": str(AppConfig.ANALYSIS_JSON_PATH),
            "data": result,
        })
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


if __name__ == "__main__":
    app.run(host=AppConfig.HOST, port=AppConfig.PORT, debug=AppConfig.DEBUG)
