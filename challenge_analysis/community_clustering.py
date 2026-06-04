import json
import pandas as pd
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, leaves_list


def run_community_clustering(json_path, score_threshold=0.55):
    print(f"🚀 [Step 4] 启动高噪声弹性过滤与双向层次聚类重排 (当前门限={score_threshold})...")
    with open(json_path, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    flat_data = []
    for person_id, person_node in master_data.items():
        for img_id, img_node in person_node["images"].items():
            for box in img_node["yolo_boxes"]:
                if box["score"] >= score_threshold and box["label"] != "unknown":
                    flat_data.append({"Suspect": person_id, "Item": box["label"]})

    df_flat = pd.DataFrame(flat_data)
    pivot_df = pd.crosstab(df_flat['Suspect'], df_flat['Item'])
    all_40_suspects = [f"Person{i}" for i in range(1, 41)]
    pivot_df = pivot_df.reindex(all_40_suspects, fill_value=0)

    # 执行矩阵双向重排算法 (Matrix Reordering)
    row_order = leaves_list(linkage(pdist(pivot_df.values, metric='euclidean'), method='ward'))
    col_order = leaves_list(linkage(pdist(pivot_df.values.T, metric='euclidean'), method='ward'))

    ordered_suspects = [pivot_df.index[i] for i in row_order]
    ordered_items = [pivot_df.columns[i] for i in col_order]

    reordered_matrix = pivot_df.loc[ordered_suspects, ordered_items]
    print("\n📊 [任务三 & 四结果] 经过数学重排收敛后的全员资产频谱矩阵:")
    print(reordered_matrix)
    return pivot_df


if __name__ == "__main__":
    run_community_clustering("../raw_data/i3_new_data.json")