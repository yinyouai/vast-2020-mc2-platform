# -*- coding: utf-8 -*-
"""
ai_corrector.py  v2
====================
从原始 i3_new_data.json 重新生成 human_corrections.json。
所有数据均来自原始 CSV / txt，不使用任何旧的 corrections 文件。

操作分级
--------
confirm   : 严格文本别名命中 → 高置信，直接写入 corrected_labels
tentative : 宽松文本 / 模型重复检测 → 需人工复核才计入最终结论
            (写入 corrected_labels 但 human_reviewed=false + source 标记)
skip      : 无充分证据，不写入

运行
----
python challenge_analysis/ai_corrector.py
"""

import json
import os
from collections import defaultdict
from datetime import datetime, timezone

# ── 路径 ─────────────────────────────────────────────────────────────────────
_HERE      = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(_HERE)
MASTER_JSON  = os.path.join(BASE_DIR, "raw_data", "i3_new_data.json")
OUTPUT_JSON  = os.path.join(BASE_DIR, "raw_data", "human_corrections.json")

# ── 阈值（调整这里即可，无需改其他代码） ──────────────────────────────────────
CFG = {
    # 重复检测：同一 Person ≥ REPEAT_MIN_FRAMES 张图，每张 score ≥ REPEAT_SCORE
    "REPEAT_SCORE":      0.35,
    "REPEAT_MIN_FRAMES": 2,
    # 单帧检测：score ≥ 此值才写为 tentative
    "SINGLE_SCORE":      0.45,
    # 拥有者 > 此数视为公共物品，剪枝
    "UBIQUITOUS_LIMIT":  15,
    # 目标团体规模
    "TARGET_GROUP_SIZE": 8,
}

# ── 已知噪声类别（模型乱检，完全不可信，不写入任何候选） ──────────────────────
NOISE_LABELS = {
    "sign", "eyeball", "pumpkinNotes", "cloudSign",
    "hairClip", "birdCall", "redWhistle",
}

# ── 受控别名 ──────────────────────────────────────────────────────────────────
# 严格别名 → confirm
STRICT_ALIASES: dict[str, tuple] = {
    "canadaPencil":   ("maple leaf pencil", "canada pencil",
                       "canadian pencil", "souvenir from canada"),
    "rainbowPens":    ("rainbow pen", "rainbow pens",
                       "color pens", "colour pens", "colored pens"),
    "rubiksCube":     ("rubik", "rubik's cube", "rubiks cube"),
    "noisemaker":     ("noisemaker", "noise maker", "cheering stick"),
    "blueSunglasses": ("blue sunglasses",),
    "pinkEraser":     ("pink eraser",),
    "lavenderDie":    ("lavender die", "purple die", "purple dice"),
    "metalKey":       ("metal key",),
    "miniCards":      ("mini cards", "tiny cards", "minicard"),
    "yellowBag":      ("yellow bag",),
    "pinkCandle":     ("pink candle",),
    "silverStraw":    ("silver straw",),
    "trophy":         ("swimming trophy", "my trophy"),
    "spinner":        ("led spinner", "fidget spinner"),
}

# 宽松别名 → tentative（仅在严格别名没命中时才触发）
BROAD_ALIASES: dict[str, tuple] = {
    "canadaPencil":   ("pencil",),
    "noisemaker":     ("whistle",),
    "lavenderDie":    ("dice", " die "),
    "miniCards":      (" card", "cards"),
    "trophy":         ("trophy",),
    "spinner":        ("spinner",),
}

# ── caption 矛盾词（这些词出现在 caption 里说明检测框大概率是误报） ────────────
CONTRADICTION_WORDS = [
    "balloon", "calabash", "gourd", "lego", "rocket",
    "tortoise", "turtle", "globe", "emoji",
]


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def person_sort_key(pid: str) -> int:
    try:
        return int(pid.replace("Person", ""))
    except ValueError:
        return 999


def collect_texts(person: dict) -> list[str]:
    """收集 Person 全部文本（独立文本 + 所有图片 caption）。"""
    pool: list[str] = []
    pool.extend(person.get("independent_texts", []))
    for img in person.get("images", {}).values():
        cap = img.get("caption", "").strip()
        if cap:
            pool.append(cap)
    return pool


def match_aliases(text_pool: list[str], aliases: tuple) -> list[str]:
    """返回命中别名的原始句子列表。"""
    if not aliases:
        return []
    hits = []
    for txt in text_pool:
        low = txt.lower()
        if any(a in low for a in aliases):
            hits.append(txt.strip())
    return hits


def caption_contradicts(person: dict, img_id: str, label: str) -> bool:
    """
    如果某图片的 caption 里有明显矛盾词，且 label 的严格别名不在 caption 里
    → 视为矛盾，检测框可能是误报。
    """
    img = person.get("images", {}).get(img_id, {})
    cap = img.get("caption", "").lower()
    if not cap:
        return False
    strict = STRICT_ALIASES.get(label, ())
    label_in_cap = any(a in cap for a in strict)
    if label_in_cap:
        return False
    return any(w in cap for w in CONTRADICTION_WORDS)


def get_detections(person: dict, label: str) -> list[dict]:
    """
    返回该 Person 中某 label 的所有检测记录（未排除噪声图片），按 score 降序。
    """
    result = []
    for img_id, img in person.get("images", {}).items():
        if img.get("is_corrupted"):
            continue
        for box in img.get("yolo_boxes", []):
            if box.get("label") == label and float(box.get("score", 0)) > 0:
                result.append({
                    "image_id": img_id,
                    "score":    float(box["score"]),
                    "box_id":   int(box.get("box_id", -1)),
                })
    result.sort(key=lambda d: -d["score"])
    return result


def caption_images_for_label(person: dict, label: str) -> list[str]:
    """返回 caption 中严格命中 label 别名的图片 id 列表。"""
    aliases = STRICT_ALIASES.get(label, ())
    if not aliases:
        return []
    found = []
    for img_id, img in person.get("images", {}).items():
        cap = img.get("caption", "").lower()
        if any(a in cap for a in aliases):
            found.append(img_id)
    return found


# ── 核心裁决 ─────────────────────────────────────────────────────────────────

def decide(person_id: str, person: dict, label: str) -> dict | None:
    """
    对单个 (Person, label) 做裁决。
    返回 None 表示无充分证据；否则返回记录 dict。
    """
    text_pool = collect_texts(person)
    dets = get_detections(person, label)

    # ── 层1：严格文本命中 → confirm ──
    strict_hits = match_aliases(text_pool, STRICT_ALIASES.get(label, ()))
    cap_imgs = caption_images_for_label(person, label)

    if strict_hits or cap_imgs:
        # 证据图片 = caption 命中图片 + 高分检测图片（score ≥ REPEAT_SCORE）
        evidence = list(set(cap_imgs))
        for d in dets:
            if (d["score"] >= CFG["REPEAT_SCORE"]
                    and not caption_contradicts(person, d["image_id"], label)
                    and d["image_id"] not in evidence):
                evidence.append(d["image_id"])
        note = (strict_hits[0] if strict_hits else cap_imgs[0])[:100]
        return {
            "image_ids":      evidence,
            "occurrence_count": max(len(evidence), 1),
            "source":         "text-confirmed",
            "ai_confidence":  0.92 if len(strict_hits) > 1 else 0.83,
            "ai_reasoning":   f"Strict text: {note}",
            "human_reviewed": False,
            "difficult":      False,
        }

    # ── 层2：宽松文本命中 → tentative ──
    broad_hits = match_aliases(text_pool, BROAD_ALIASES.get(label, ()))
    if broad_hits:
        # 额外要求：至少有一条模型检测（分数不限）才算
        if dets:
            best = dets[0]
            note = broad_hits[0][:100]
            return {
                "image_ids":      [best["image_id"]],
                "occurrence_count": 1,
                "source":         "broad-text-tentative",
                "ai_confidence":  0.55,
                "ai_reasoning":   f"Broad text ('{note}') + model det {best['score']:.3f}",
                "human_reviewed": False,
                "difficult":      True,
            }

    # ── 层3：模型重复检测 → tentative ──
    high_dets = [d for d in dets if d["score"] >= CFG["REPEAT_SCORE"]]
    valid = [d for d in high_dets
             if not caption_contradicts(person, d["image_id"], label)]
    if len(valid) >= CFG["REPEAT_MIN_FRAMES"]:
        evidence = list({d["image_id"] for d in valid})
        best_score = valid[0]["score"]
        return {
            "image_ids":      evidence,
            "occurrence_count": len(evidence),
            "source":         "repeat-detection-tentative",
            "ai_confidence":  round(min(0.70, best_score + 0.05), 2),
            "ai_reasoning":   (f"Repeat det {len(evidence)} imgs, "
                               f"best={best_score:.3f}"),
            "human_reviewed": False,
            "difficult":      True,
        }

    # ── 层4：单帧高分 → tentative（最低优先级） ──
    if dets and dets[0]["score"] >= CFG["SINGLE_SCORE"]:
        best = dets[0]
        if not caption_contradicts(person, best["image_id"], label):
            return {
                "image_ids":      [best["image_id"]],
                "occurrence_count": 1,
                "source":         "single-detection-tentative",
                "ai_confidence":  round(best["score"] * 0.60, 2),
                "ai_reasoning":   f"Single det score={best['score']:.3f}",
                "human_reviewed": False,
                "difficult":      True,
            }

    return None


# ── 主流程 ────────────────────────────────────────────────────────────────────

def build_corrections(master_data: dict) -> dict:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # label → {person_id → record}
    raw: dict[str, dict[str, dict]] = defaultdict(dict)
    rejected: list[dict] = []
    audit_log: list[dict] = []

    # 获取所有出现过的 label（排除噪声）
    all_labels: set[str] = set(STRICT_ALIASES.keys())
    for person in master_data.values():
        for img in person.get("images", {}).values():
            for box in img.get("yolo_boxes", []):
                lbl = box.get("label", "")
                if lbl and lbl not in NOISE_LABELS:
                    all_labels.add(lbl)

    for person_id in sorted(master_data.keys(), key=person_sort_key):
        person = master_data[person_id]
        dets_all = {
            lbl: get_detections(person, lbl)
            for lbl in all_labels
        }

        for label in sorted(all_labels):
            if label in NOISE_LABELS:
                continue

            rec = decide(person_id, person, label)
            if rec is None:
                # 记录被驳回的高分但矛盾检测
                dets = dets_all.get(label, [])
                for d in dets:
                    if (d["score"] >= CFG["SINGLE_SCORE"]
                            and caption_contradicts(person, d["image_id"], label)):
                        rejected.append({
                            "person_id":       person_id,
                            "image_id":        d["image_id"],
                            "box_id":          d["box_id"],
                            "predicted_label": label,
                            "score":           d["score"],
                            "reason":          "Caption contradicts detection (AI auto-reject)",
                        })
                continue

            raw[label][person_id] = rec
            audit_log.append({
                "timestamp":  ts,
                "person_id":  person_id,
                "image_id":   rec["image_ids"][0] if rec["image_ids"] else "",
                "box_id":     -1,
                "action":     "confirm" if rec["source"] == "text-confirmed" else "tentative",
                "new_label":  label,
                "difficult":  rec["difficult"],
                "note":       rec["ai_reasoning"],
                "source":     "ai-corrector-v2",
            })

    # ── 剪枝：公共物品 ─────────────────────────────────────────────────────────
    corrected_labels: dict[str, dict] = {}
    pruned: list[str] = []

    for label, persons in raw.items():
        # 只用 confirm 计入拥有者数做剪枝判断
        confirmed_count = sum(
            1 for v in persons.values()
            if v["source"] == "text-confirmed"
        )
        repeat_count = sum(
            1 for v in persons.values()
            if "repeat" in v["source"] or "broad" in v["source"]
        )
        total = len(persons)

        if total > CFG["UBIQUITOUS_LIMIT"]:
            pruned.append(f"{label}({total})")
            continue

        corrected_labels[label] = {
            "source":           "ai-corrector-v2",
            "confirm_count":    confirmed_count,
            "tentative_count":  repeat_count,
            "persons":          persons,
        }

    return {
        "version":          2,
        "generated_by":     "ai-corrector-v2",
        "generated_at":     ts,
        "method": (
            "AI裁决(v2): 严格文本→confirm | 宽松文本+模型→tentative | "
            "模型重复≥2帧→tentative | 单帧高分→tentative。"
            "human_reviewed=false 表示待人工确认。"
        ),
        "target_group_size": CFG["TARGET_GROUP_SIZE"],
        "candidate_scoring": {
            "specificity_weight":      0.4,
            "stability_weight":        0.35,
            "visual_weight":           0.15,
            "text_weight":             0.1,
            "non_target_penalty":      0.72,
            "visual_images_per_owner": 2,
        },
        "corrected_labels":     corrected_labels,
        "rejected_predictions": rejected,
        "audit_log":            audit_log,
    }


def print_report(corrections: dict) -> None:
    cl = corrections["corrected_labels"]

    print("\n" + "=" * 70)
    print("AI 裁决报告")
    print("=" * 70)
    print(f"{'Label':<18} {'Total':>5}  {'Confirm':>7}  {'Tentative':>9}")
    print("-" * 45)

    rows = []
    for label, node in cl.items():
        total     = len(node["persons"])
        confirmed = node["confirm_count"]
        tentative = node["tentative_count"]
        rows.append((label, total, confirmed, tentative))
    rows.sort(key=lambda r: -r[1])

    for label, total, confirmed, tentative in rows:
        print(f"{label:<18} {total:>5}  {confirmed:>7}  {tentative:>9}")

    # canadaPencil 详情
    pencil = cl.get("canadaPencil", {})
    persons = pencil.get("persons", {})
    print(f"\n--- canadaPencil ({len(persons)} persons) ---")
    for pid, v in sorted(persons.items(), key=lambda kv: person_sort_key(kv[0])):
        flag = "[CONFIRM]" if v["source"] == "text-confirmed" else "[TENTATIVE]"
        imgs = v["image_ids"]
        print(f"  {pid:<10} {flag:<12} conf={v['ai_confidence']:.2f}"
              f"  imgs={len(imgs)}  {v['ai_reasoning'][:65]}")

    print(f"\nrejected_predictions: {len(corrections['rejected_predictions'])}")
    print(f"audit_log entries:    {len(corrections['audit_log'])}")


def main() -> None:
    print(f"Loading {MASTER_JSON} ...")
    with open(MASTER_JSON, encoding="utf-8") as f:
        master_data = json.load(f)
    print(f"Persons: {len(master_data)}")

    corrections = build_corrections(master_data)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(corrections, f, indent=2, ensure_ascii=False)

    print_report(corrections)
    print(f"\n[OK] Written -> {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
