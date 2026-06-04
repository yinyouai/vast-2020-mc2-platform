import numpy as np
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, leaves_list


class CyberClusteringEngine:
    """增强型聚类引擎 — 支持多种聚类方法 + Ward 层次聚类"""

    @staticmethod
    def compute_matrix_reordering(master_data, score_threshold=0.25,
                                   excluded_items=None, method='ward'):
        """
        核心高内聚算法：动态响应门限与黑客组织排除，重排列矩阵

        Args:
            master_data: 主数据字典
            score_threshold: 置信度阈值 (默认 0.25)
            excluded_items: 被排除的物品列表
            method: 聚类方法 - 'ward', 'complete', 'average', 'single', 'kmeans', 'dbscan'
        """
        excluded_items = excluded_items if excluded_items else []
        available_methods = ['ward', 'complete', 'average', 'single', 'kmeans', 'dbscan']
        if method not in available_methods:
            print(f"[ClusterEngine] 未知聚类方法 '{method}', 回退至 ward")
            method = 'ward'

        # 1. 动态剥离嫌疑人轴和去噪物资全景列轴
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
                    if (box.get("is_human_edited", False) or box["score"] >= score_threshold) and label in item_idx:
                        matrix[suspect_idx[p_id], item_idx[label]] += 1

        ordered_suspects = list(suspects)
        ordered_items = list(items)

        # 3. 聚类重排
        if len(suspects) > 1 and len(items) > 1 and np.sum(matrix) > 0:
            try:
                if method in ('kmeans', 'dbscan'):
                    ordered_suspects, ordered_items = CyberClusteringEngine._sklearn_reorder(
                        matrix, suspects, items, method
                    )
                else:
                    # 层次聚类 (ward, complete, average, single)
                    ordered_suspects, ordered_items = CyberClusteringEngine._hierarchical_reorder(
                        matrix, suspects, items, method
                    )
            except Exception as e:
                print(f"[ClusterEngine] 聚类异常 (method={method}): {e}, 回退到原始排序")

        # 4. 组装网格数据
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

    @staticmethod
    def _hierarchical_reorder(matrix, suspects, items, method='ward'):
        """层次聚类重排 (ward, complete, average, single)"""
        row_linkage = linkage(pdist(matrix, metric='euclidean'), method=method)
        ordered_suspects = [suspects[i] for i in leaves_list(row_linkage)]

        col_linkage = linkage(pdist(matrix.T, metric='euclidean'), method=method)
        ordered_items = [items[i] for i in leaves_list(col_linkage)]

        return ordered_suspects, ordered_items

    @staticmethod
    def _sklearn_reorder(matrix, suspects, items, method='kmeans'):
        """基于 sklearn 的聚类重排 (kmeans 或 dbscan)"""
        try:
            if method == 'kmeans':
                from sklearn.cluster import KMeans
                n_clusters_rows = min(5, len(suspects) - 1)
                n_clusters_cols = min(3, len(items) - 1)
                if n_clusters_rows < 2 or n_clusters_cols < 2:
                    # 回退到 ward
                    return CyberClusteringEngine._hierarchical_reorder(
                        matrix, suspects, items, 'ward'
                    )

                row_labels = KMeans(n_clusters=n_clusters_rows, random_state=42, n_init=10).fit_predict(matrix)
                col_labels = KMeans(n_clusters=n_clusters_cols, random_state=42, n_init=10).fit_predict(matrix.T)

                # 按聚类标签排序：同一簇内按均值降序排列
                row_order = sorted(range(len(suspects)),
                                   key=lambda i: (row_labels[i], -np.mean(matrix[i])))
                col_order = sorted(range(len(items)),
                                   key=lambda j: (col_labels[j], -np.mean(matrix[:, j])))

                ordered_suspects = [suspects[i] for i in row_order]
                ordered_items = [items[j] for j in col_order]

            elif method == 'dbscan':
                from sklearn.cluster import DBSCAN
                # DBSCAN 参数自动调整
                eps = max(0.3, np.std(matrix) * 1.5)
                row_labels = DBSCAN(eps=eps, min_samples=2).fit_predict(matrix)
                col_labels = DBSCAN(eps=eps, min_samples=2).fit_predict(matrix.T)

                # 噪声点 (label=-1) 排在最后
                row_order = sorted(range(len(suspects)),
                                   key=lambda i: (row_labels[i] == -1, row_labels[i], -np.mean(matrix[i])))
                col_order = sorted(range(len(items)),
                                   key=lambda j: (col_labels[j] == -1, col_labels[j], -np.mean(matrix[:, j])))

                ordered_suspects = [suspects[i] for i in row_order]
                ordered_items = [items[j] for j in col_order]

            return ordered_suspects, ordered_items

        except ImportError:
            print("[ClusterEngine] sklearn 未安装，回退到 ward 聚类")
            return CyberClusteringEngine._hierarchical_reorder(matrix, suspects, items, 'ward')
