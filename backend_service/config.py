import os
from pathlib import Path


class AppConfig:
    # 绝对对齐：定位到项目根目录下的共享原始数据集集中大仓
    BASE_DIR = Path(__file__).resolve().parent.parent
    RAW_DATA_DIR = BASE_DIR / "raw_data"

    # 核心多模态 Master JSON 主包物理落盘路径
    MASTER_JSON_PATH = RAW_DATA_DIR / "i3_new_data.json"
    CORRECTIONS_JSON_PATH = RAW_DATA_DIR / "human_corrections.json"
    ANALYSIS_JSON_PATH = RAW_DATA_DIR / "analysis_results.json"

    # 嫌疑人图片碎片物理存放地址
    IMAGE_ASSETS_DIR = RAW_DATA_DIR / "MC2-Image-Data"

    # Flask 运行配置
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = True
