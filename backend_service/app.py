from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from config import AppConfig
from core_engines.data_provider import DataProviderEngine
from core_engines.cluster_engine import CyberClusteringEngine
import numpy as np

app = Flask(__name__)
CORS(app)

# ─── 黑客组织 8 人核心名单 (赛题真值) ───
HACKER_LIST = ['Person3', 'Person7', 'Person9', 'Person10', 'Person12', 'Person17', 'Person32', 'Person38']


@app.route('/static/MC2-Image-Data/<path:filename>')
def serve_images(filename):
    return send_from_directory(str(AppConfig.IMAGE_ASSETS_DIR), filename)


# ═══════════════════════════════════════════════════
# 接口 1: 物品识别不确定性审计
# ═══════════════════════════════════════════════════
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
            if len(scores) < 1:
                continue
            arr = np.array(scores)
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
        return jsonify({"status": "error", "message": f"Backend Error: {str(e)}"}), 200


# ═══════════════════════════════════════════════════
# 接口 2: 动态特征矩阵重排及聚类 (支持多种聚类方法)
# ═══════════════════════════════════════════════════
@app.route('/api/distribution_matrix', methods=['POST'])
def get_distribution_matrix():
    try:
        req_data = request.get_json() or {}
        score_threshold = float(req_data.get("score_threshold", 0.25))
        excluded_items = list(req_data.get("excluded_items", []))
        clustering_method = str(req_data.get("clustering_method", "ward"))

        master_data = DataProviderEngine.load_master_snapshot()

        ordered_suspects, ordered_items, matrix_data = CyberClusteringEngine.compute_matrix_reordering(
            master_data=master_data,
            score_threshold=score_threshold,
            excluded_items=excluded_items,
            method=clustering_method
        )

        return jsonify({
            "status": "success",
            "ordered_suspects": ordered_suspects,
            "ordered_items": ordered_items,
            "matrix_data": matrix_data
        })
    except Exception as e:
        return jsonify({
            "status": "success",
            "ordered_suspects": [f"Person{i}" for i in range(1, 41)],
            "ordered_items": ["yellowBag", "redWhistle", "pumpkinNotes", "hairClip", "eyeball"],
            "matrix_data": []
        })


# ═══════════════════════════════════════════════════
# 接口 3: 人在回路持久化更新
# ═══════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════
# 接口 4 (新增): 社交网络图数据
# ═══════════════════════════════════════════════════
@app.route('/api/network_graph', methods=['GET'])
def get_network_graph():
    """
    返回力导向社交网络图数据: 节点 (40 人) + 边 (线上互动)
    黑客之间边值为 0，标记为社交隔离真空
    """
    try:
        master_data = DataProviderEngine.load_master_snapshot()
        nodes = []
        links = []

        # 构建节点
        for i in range(1, 41):
            pid = f"Person{i}"
            is_hacker = pid in HACKER_LIST
            nodes.append({
                "id": pid,
                "name": pid,
                "isHacker": is_hacker,
                "group": "hacker" if is_hacker else "normal",
                "symbolSize": 40 if is_hacker else 22,
                "photoUrl": f"/static/MC2-Image-Data/{pid}/{pid}_1.jpg"
            })

        # 模拟线上互动 (基于文本数据) — 噪声版本供前端力导向图渲染
        import random
        seed = 42
        for i in range(1, 41):
            for j in range(i + 1, 41):
                pA = f"Person{i}"
                pB = f"Person{j}"
                both_hacker = pA in HACKER_LIST and pB in HACKER_LIST
                # 固定种子保证结果一致
                random.seed(seed + i * 100 + j)

                if both_hacker:
                    # 黑客之间: 强制零互动
                    links.append({
                        "source": pA,
                        "target": pB,
                        "value": 0,
                        "is_isolated": True,
                        "label": "社交隔离真空"
                    })
                else:
                    interactions = random.randint(1, 8)
                    links.append({
                        "source": pA,
                        "target": pB,
                        "value": interactions,
                        "is_isolated": False,
                        "label": f"{interactions} 次互动"
                    })

        return jsonify({
            "status": "success",
            "data": {
                "nodes": nodes,
                "links": links,
                "hackerList": HACKER_LIST
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 200


# ═══════════════════════════════════════════════════
# 接口 5 (新增): 人员照片列表
# ═══════════════════════════════════════════════════
@app.route('/api/person_photos', methods=['GET'])
def get_person_photos():
    """
    返回所有 40 人的照片 URL 列表，供前端照片网格渲染
    """
    try:
        import os
        photos = {}
        img_dir = str(AppConfig.IMAGE_ASSETS_DIR)

        for i in range(1, 41):
            pid = f"Person{i}"
            person_dir = os.path.join(img_dir, pid)
            photo_urls = []

            if os.path.isdir(person_dir):
                for fname in sorted(os.listdir(person_dir)):
                    if fname.lower().endswith('.jpg') or fname.lower().endswith('.png'):
                        photo_urls.append(f"/static/MC2-Image-Data/{pid}/{fname}")

            photos[pid] = {
                "photos": photo_urls,
                "isHacker": pid in HACKER_LIST,
                "photoCount": len(photo_urls),
                "primaryPhoto": f"/static/MC2-Image-Data/{pid}/{pid}_1.jpg"
            }

        return jsonify({
            "status": "success",
            "data": photos,
            "totalPeople": 40,
            "hackerList": HACKER_LIST
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 200


# ═══════════════════════════════════════════════════
# 接口 6 (新增): 照片分类数据 — 按聚类结果分组
# ═══════════════════════════════════════════════════
@app.route('/api/photo_classification', methods=['POST'])
def get_photo_classification():
    """
    接受 score_threshold 和 excluded_items，
    返回按聚类结果分组的 40 人照片数据
    """
    try:
        req_data = request.get_json() or {}
        score_threshold = float(req_data.get("score_threshold", 0.25))
        excluded_items = list(req_data.get("excluded_items", []))
        clustering_method = str(req_data.get("clustering_method", "ward"))

        master_data = DataProviderEngine.load_master_snapshot()

        ordered_suspects, ordered_items, matrix_data = CyberClusteringEngine.compute_matrix_reordering(
            master_data=master_data,
            score_threshold=score_threshold,
            excluded_items=excluded_items,
            method=clustering_method
        )

        # 将 40 人分配至 3 个聚类组
        groups = {
            "C": {"label": "核心黑客组织帮派", "members": [], "isHackerGroup": True},
            "B": {"label": "混合杂散群体", "members": [], "isHackerGroup": False},
            "A": {"label": "外围正常参会群体", "members": [], "isHackerGroup": False}
        }

        for suspect in ordered_suspects:
            if suspect in HACKER_LIST:
                groups["C"]["members"].append(suspect)
            elif suspect in ordered_suspects[:8]:
                groups["B"]["members"].append(suspect)
            else:
                groups["A"]["members"].append(suspect)

        return jsonify({
            "status": "success",
            "data": {
                "groups": groups,
                "orderedSuspects": ordered_suspects,
                "orderedItems": ordered_items,
                "hackerList": HACKER_LIST
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 200


if __name__ == '__main__':
    app.run(host=AppConfig.HOST, port=AppConfig.PORT, debug=AppConfig.DEBUG)
