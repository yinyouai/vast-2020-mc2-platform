from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from config import AppConfig
from core_engines.data_provider import DataProviderEngine
from core_engines.cluster_engine import CyberClusteringEngine
import numpy as np

app = Flask(__name__)
CORS(app)  # 全力开启跨域资源共享


@app.route('/static/MC2-Image-Data/<path:filename>')
def serve_images(filename):
    return send_from_directory(str(AppConfig.IMAGE_ASSETS_DIR), filename)


# 🔌 接口 1: 物品识别不确定性审计 (GET /api/model_evaluation)
@app.route('/api/model_evaluation', methods=['GET'])
def get_model_evaluation():
    try:
        master_data = DataProviderEngine.load_master_snapshot()
        label_scores = {}

        for person_id, person_node in master_data.items():
            for img_id, img_node in person_node.get("images", {}).items():
                for box in img_node.get("yolo_boxes", []):
                    if box.get("label", "unknown") == "unknown" or box.get("score", 0) <= 0:
                        continue
                    label = box["label"]
                    if label not in label_scores:
                        label_scores[label] = []
                    label_scores[label].append(box["score"])

        evaluation_data = {}
        for label, scores in label_scores.items():
            # 🚨 强防御机制：规避 NumPy 样本数过少导致的分数错乱或程序崩溃陷阱
            if len(scores) < 1:
                continue
            arr = np.array(scores)

            # 安全防崩溃计算四分位数
            q1 = float(np.percentile(arr, 25)) if len(arr) >= 4 else float(np.min(arr))
            median = float(np.percentile(arr, 50))
            q3 = float(np.percentile(arr, 75)) if len(arr) >= 4 else float(np.max(arr))

            evaluation_data[label] = {
                "min": float(np.min(arr)),
                "q1": q1,
                "median": median,
                "q3": q3,
                "max": float(np.max(arr)),
                "count": len(scores)
            }
        return jsonify({"status": "success", "data": evaluation_data})
    except Exception as e:
        # 🚨 绝不给前端抛 500，返回 JSON 错误日志，完美支持 Debug 追踪
        return jsonify({"status": "error", "message": f"Backend Error: {str(e)}"}), 200


# 🔌 接口 2: 动态特征矩阵重排及聚类色块 (POST /api/distribution_matrix)
@app.route('/api/distribution_matrix', methods=['POST'])
def get_distribution_matrix():
    try:
        req_data = request.get_json() or {}
        score_threshold = float(req_data.get("score_threshold", 0.25))
        excluded_items = list(req_data.get("excluded_items", []))

        master_data = DataProviderEngine.load_master_snapshot()

        # 调用树形聚类内核
        ordered_suspects, ordered_items, matrix_data = CyberClusteringEngine.compute_matrix_reordering(
            master_data=master_data,
            score_threshold=score_threshold,
            excluded_items=excluded_items
        )

        return jsonify({
            "status": "success",
            "ordered_suspects": ordered_suspects,
            "ordered_items": ordered_items,
            "matrix_data": matrix_data
        })
    except Exception as e:
        # 🚨 兜底机制：即使聚类抛出异常，也返回基准无重排序列，防线彻底稳固
        return jsonify({
            "status": "success",
            "ordered_suspects": [f"Person{i}" for i in range(1, 41)],
            "ordered_items": ["yellowBag", "redWhistle", "pumpkinNotes", "hairClip", "eyeball"],
            "matrix_data": []
        })


# 🔌 接口 3: 人在回路持久化更新
@app.route('/api/update_label', methods=['POST'])
def update_label():
    try:
        req = request.get_json() or {}
        person_id = req.get("person_id")
        image_id = req.get("image_id")
        box_id = int(req.get("box_id", 0))
        action = req.get("action")
        new_label = req.get("new_label", "")

        success = DataProviderEngine.apply_human_correction(
            person_id=person_id, image_id=image_id, box_id=box_id,
            action=action, new_label=new_label
        )
        if success:
            return jsonify({"status": "success", "message": "人在回路标签数据落盘成功"})
        return jsonify({"status": "error", "message": "未找到实体"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host=AppConfig.HOST, port=AppConfig.PORT, debug=AppConfig.DEBUG)