import pandas as pd
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "backend_service"))

from core_engines.analysis_engine import ForensicAnalysisEngine
from core_engines.data_provider import DataProviderEngine


def run_community_clustering(json_path=None, score_threshold=0.55, data_source="corrected"):
    print(f"[Step 4] 生成人物-物品矩阵（数据层={data_source}）...")
    engine = ForensicAnalysisEngine(
        DataProviderEngine.load_master_snapshot(),
        DataProviderEngine.load_corrections(),
    )
    if data_source == "raw":
        suspects, items, cells = engine.raw_matrix(score_threshold)
    else:
        suspects, items, cells = engine.corrected_matrix()

    pivot_df = pd.DataFrame(0, index=suspects, columns=items, dtype=int)
    for cell in cells:
        pivot_df.loc[cell["suspect"], cell["item"]] = cell["count"]

    print("\n[任务三结果] 校正层矩阵已按 Ward 层次聚类重排：")
    print(pivot_df)
    return pivot_df


if __name__ == "__main__":
    run_community_clustering()
