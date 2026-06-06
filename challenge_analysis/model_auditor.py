from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "backend_service"))

from core_engines.analysis_engine import ForensicAnalysisEngine
from core_engines.data_provider import DataProviderEngine


def run_model_auditor(json_path=None):
    print("[Step 3] 审计原始 YOLO v2 输出，不把置信度直接等同于正确率...")
    training_dir = ROOT_DIR / "raw_data" / "MC2-Image-Data" / "TrainingImages"
    labels = [path.name for path in training_dir.iterdir() if path.is_dir()]
    engine = ForensicAnalysisEngine(
        DataProviderEngine.load_master_snapshot(),
        DataProviderEngine.load_corrections(),
        labels,
    )
    audit = engine.model_audit()
    hypothesis = engine.raw_hypothesis()

    print(
        f"训练类别 {audit['training_class_count']} 个，原始预测实际出现 "
        f"{audit['detected_class_count']} 个类别，缺失 {audit['missing_class_count']} 个。"
    )
    print(
        f"{audit['reviewed_class']} 人员级 "
        f"precision={audit['reviewed_person_precision']:.3f}, "
        f"recall={audit['reviewed_person_recall']:.3f}。"
    )
    print(
        f"{hypothesis['label']} 高阈值假设：{hypothesis['owner_count']} 人、"
        f"{len(hypothesis['detections'])} 个框，复核状态={hypothesis['status']}。"
    )
    return audit

if __name__ == "__main__":
    run_model_auditor()
