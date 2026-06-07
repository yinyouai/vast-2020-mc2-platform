import sys
sys.path.insert(0, 'backend_service')
from core_engines.data_provider import DataProviderEngine
from core_engines.analysis_engine import ForensicAnalysisEngine
from config import AppConfig

master = DataProviderEngine.load_master_snapshot()
corrections = DataProviderEngine.load_corrections()
training_labels = [p.name for p in (AppConfig.IMAGE_ASSETS_DIR / 'TrainingImages').iterdir() if p.is_dir()]

engine = ForensicAnalysisEngine(master, corrections, training_labels)

# 1. candidate_rankings
rankings = engine.candidate_rankings(0.45)
print("=== candidate_rankings ===")
print("Keys in first item:", list(rankings[0].keys()))
print()
for r in rankings[:6]:
    print("  " + r["label"].ljust(18)
          + " owners=" + str(r["owner_count"])
          + "  score=" + str(round(r["score"], 3))
          + "  min_occ=" + str(r["min_occurrence"])
          + "  exact=" + str(r["exact_target_size"]))

# 2. analysis_summary - final
summary = engine.analysis_summary(0.45)
final = summary.get("final", {})
print("\n=== analysis_summary.final ===")
print("  totem:", final.get("totem"))
print("  group:", final.get("group"))
print("  score:", final.get("score"))

# 3. corrected_matrix
suspects, items, matrix = engine.corrected_matrix()
print("\n=== corrected_matrix ===")
print("  persons:", len(suspects), "  items:", len(items))

# 4. review_priorities
priorities = engine.person_review_priorities()
print("\n=== review_priorities ===")
print("  count:", len(priorities))
print("  top5:", [p["person_id"] for p in priorities[:5]])

# 5. ai_confidence 字段是否被引擎接受（不报错即可）
print("\n=== compatibility check: extra fields ignored? ===")
cl = corrections.get("corrected_labels", {})
pencil_persons = cl.get("canadaPencil", {}).get("persons", {})
has_ai_fields = all("ai_confidence" in v for v in pencil_persons.values())
print("  canadaPencil persons have ai_confidence field:", has_ai_fields)
print("  engine ran without error: OK")
