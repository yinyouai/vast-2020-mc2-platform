import numpy as np
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, leaves_list


class CyberClusteringEngine:
    @staticmethod
    def compute_matrix_reordering(master_data, score_threshold=0.25, excluded_items=None):
        """
        核心高内聚算法：动态响应门限与黑客组织排除，重排列矩阵
        """
        excluded_items = excluded_items if excluded_items else []

        # 1. 动态剥离当前状态下的嫌疑人轴和去噪物资全景列轴
        suspects = sorted(list(master_data.keys()))
        all_items = set()

        for p_id, p_node in master_data.items():
            for img_id, img_node in p_node["images"].items():
                for box in img_node["yolo_boxes"]:
                    if box["label"] != "unknown" and box["label"] not in excluded_items:
                        all_items.add(box["label"])
        items = sorted(list(all_items))

        if not items:
            return suspects, [], []

        # 2. 建立 NumPy 二维网格计数拓扑矩阵
        matrix = np.zeros((len(suspects), len(items)))
        suspect_idx = {s: i for i, s in enumerate(suspects)}
        item_idx = {it: i for i, it in enumerate(items)}

        for p_id, p_node in master_data.items():
            for img_id, img_node in p_node["images"].items():
                for box in img_node["yolo_boxes"]:
                    label = box["label"]
                    # 弹性判定：人工纠错通过项、或者高于当前滑块控制门限的机器边界框
                    if (box["is_human_edited"] or box["score"] >= score_threshold) and label in item_idx:
                        matrix[suspect_idx[p_id], item_idx[label]] += 1

        ordered_suspects = list(suspects)
        ordered_items = list(items)

        # 3. 实时并发调度 Ward 离散树形聚类重排 (Matrix Reordering)
        if len(suspects) > 1 and len(items) > 1 and np.sum(matrix) > 0:
            try:
                # 纵轴（40人候选人轴）聚类洗牌
                row_linkage = linkage(pdist(matrix, metric='euclidean'), method='ward')
                ordered_suspects = [suspects[i] for i in leaves_list(row_linkage)]

                # 横轴（安全暗号物资轴）聚类洗牌
                col_linkage = linkage(pdist(matrix.T, metric='euclidean'), method='ward')
                ordered_items = [items[i] for i in leaves_list(col_linkage)]
            except Exception:
                pass  # 规避极端边缘过滤下的行列全零计算异常

        # 4. 组装网格数据单元供现代热力图组件无缝渲染
        matrix_data = []
        for i, s in enumerate(suspects):
            for j, it in enumerate(items):
                if matrix[i, j] > 0:
                    matrix_data.append({
                        "suspect": s,
                        "item": it,
                        "count": int(matrix[i, j])
                    })

        return ordered_suspects, ordered_items, matrix_data