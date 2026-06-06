import sys
from pathlib import Path

ANALYSIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = ANALYSIS_DIR.parent
sys.path.insert(0, str(ANALYSIS_DIR))

def execute_full_pipeline():
    print("=" * 72)
    print("VAST 2020 MC2 可复现取证流水线")
    print("=" * 72)

    raw_data_dir = ROOT_DIR / "raw_data" / "MC2-Image-Data"
    if not raw_data_dir.exists():
        print(f"未找到数据目录：{raw_data_dir}")
        return

    try:
        from model_auditor import run_model_auditor
        run_model_auditor()
        from community_clustering import run_community_clustering
        run_community_clustering(data_source="corrected")
        from totem_elimination import run_totem_elimination
        run_totem_elimination()
        print("=" * 72)
        print("流水线执行完成。原始预测未被覆盖，结论来自独立校正层。")
        print("=" * 72)

    except ImportError as e:
        print(f"导入分析模块失败：{e}")
    except Exception as e:
        print(f"流水线执行失败：{e}")

if __name__ == "__main__":
    execute_full_pipeline()
