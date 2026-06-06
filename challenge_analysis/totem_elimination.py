import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "backend_service"))

from config import AppConfig
from core_engines.analysis_engine import ForensicAnalysisEngine
from core_engines.data_provider import DataProviderEngine


def run_totem_elimination(json_path=None):
    print("[Step 5] 对校正后的候选物品执行覆盖率、稳定性、图文证据评分...")
    training_dir = AppConfig.IMAGE_ASSETS_DIR / "TrainingImages"
    engine = ForensicAnalysisEngine(
        DataProviderEngine.load_master_snapshot(),
        DataProviderEngine.load_corrections(),
        [path.name for path in training_dir.iterdir() if path.is_dir()],
    )
    summary = engine.analysis_summary()

    print("\n候选排名：")
    for item in summary["candidate_rankings"]:
        print(
            f"  {item['label']:<18} owners={item['owner_count']:>2} "
            f"min_occurrence={item['min_occurrence']} score={item['score']:.4f}"
        )

    final = summary["final"]
    print(f"\n最终暗号物品：{final['totem']}")
    print(f"8 位嫌疑人：{', '.join(final['group'])}")
    for reason in final["rationale"]:
        print(f"  - {reason}")

    with open(AppConfig.ANALYSIS_JSON_PATH, "w", encoding="utf-8") as stream:
        json.dump(summary, stream, indent=2, ensure_ascii=False)
    print(f"\n分析结果已写入：{AppConfig.ANALYSIS_JSON_PATH}")
    return summary

if __name__ == "__main__":
    run_totem_elimination()
