#!/usr/bin/env python3
"""
YOLO Logo Downloader
持续运行4小时，尽可能多地下载logo
"""

import os
import time
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

# 配置
LOGO_DIR = Path("logo")
RECORD_FILE = LOGO_DIR / "logo_records.md"
STATE_FILE = LOGO_DIR / "download_state.json"
DURATION_HOURS = 4
START_TIME = datetime.now()
END_TIME = START_TIME + timedelta(hours=DURATION_HOURS)

# 确保目录存在
LOGO_DIR.mkdir(exist_ok=True)

# 数据源列表 - 按优先级排序
SOURCES = [
    {
        "name": "simple-icons",
        "type": "github",
        "url": "https://api.github.com/repos/simple-icons/simple-icons/contents/icons",
        "enabled": True
    },
    {
        "name": "worldvectorlogo-search",
        "type": "search",
        "base_url": "https://worldvectorlogo.com/search/",
        "enabled": False  # 需要特殊处理
    }
]

# 知名公司列表（作为备选）
COMPANY_LIST = [
    "google", "microsoft", "apple", "amazon", "meta", "tesla", "nvidia", "intel",
    "amd", "qualcomm", "samsung", "sony", "panasonic", "lg", "siemens", "bosch",
    "toyota", "honda", "bmw", "mercedes", "audi", "volkswagen", "porsche", "ferrari",
    "lamborghini", "mclaren", "bugatti", "rollsroyce", "bentley", "astonmartin",
    "jpmorgan", "bankofamerica", "wellsfargo", "citigroup", "goldmansachs", "morganstanley",
    "hsbc", "barclays", "deutschebank", "ubs", "credit-suisse", "nomura",
    "exxonmobil", "chevron", "bp", "shell", "total", "schlumberger", "halliburton",
    "johnsonandjohnson", "pfizer", "novartis", "roche", "merck", "abbvie", "eli-lilly",
    "unitedhealth", "anthem", "cigna", "humana", "aetna",
    "walmart", "costco", "target", "home-depot", "lowes", "best-buy",
    "coca-cola", "pepsi", "nestle", "unilever", "procter-gamble", "colgate",
    "mcdonalds", "starbucks", "yum-brands", "chipotle", "dominos", "darden",
    "disney", "netflix", "comcast", "charter", "verizon", "at-t", "t-mobile",
    "nike", "adidas", "lululemon", "under-armour", "gap", "h-m", "zara",
    "salesforce", "oracle", "sap", "intuit", "adobe", "autodesk", "workday",
    "booking", "expedia", "airbnb", "uber", "lyft", "doordash", "instacart",
    "zoom", "slack", "teams", "webex", "skype", "telegram", "signal",
    "spotify", "apple-music", "youtube-music", "amazon-music", "tidal",
    "twitter", "facebook", "instagram", "linkedin", "snapchat", "pinterest", "tiktok",
    "reddit", "tumblr", "flickr", "vimeo", "twitch",
    "bitcoin", "ethereum", "binance", "coinbase", "kraken", "robinhood",
    "visa", "mastercard", "amex", "discover", "paypal", "square", "stripe",
    "fedex", "ups", "dhl", "amazon-logistics",
    "boeing", "airbus", "lockheed", "northrop", "raytheon", "general-dynamics",
    "caterpillar", "deere", "komatsu", "hitachi-construction",
    "3m", "honeywell", "ge", "siemens-energy", "schneider", "abb", "rockwell",
    "dupont", "dow", "basf", "lyondell", "eastman", "celanese",
    "delta", "united", "american-airlines", "southwest", "lufthansa", "emirates", "singapore-airlines"
]


def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOGO_DIR / "download.log", "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")


def load_state():
    """加载下载状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"downloaded": [], "failed": [], "last_company_index": 0}


def save_state(state):
    """保存下载状态"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def init_markdown():
    """初始化 markdown 记录文件"""
    if not RECORD_FILE.exists():
        with open(RECORD_FILE, "w", encoding="utf-8") as f:
            f.write("# Logo 下载记录\n\n")
            f.write(f"开始时间: {START_TIME.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"计划结束: {END_TIME.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("| 序号 | 公司名 | 文件名 | 来源 | 下载时间 | 状态 |\n")
            f.write("|------|--------|--------|------|----------|------|\n")


def update_markdown(index, company, filename, source, status):
    """更新 markdown 记录"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(RECORD_FILE, "a", encoding="utf-8") as f:
        f.write(f"| {index} | {company} | {filename} | {source} | {timestamp} | {status} |\n")


def download_from_simple_icons(company, state):
    """从 simple-icons 下载单个 logo"""
    try:
        # 转换公司名格式
        icon_name = company.lower().replace(" ", "").replace("-", "").replace("&", "and")
        
        # 尝试直接下载
        url = f"https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/{icon_name}.svg"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            filename = f"{company}.svg"
            filepath = LOGO_DIR / filename
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)
            return True, filename
        
        # 尝试其他常见变体
        variants = [
            company.lower().replace(" ", "").replace("&", "and"),
            company.lower().replace(" ", "-").replace("&", "and"),
            company.lower().replace("-", "").replace("&", "and"),
        ]
        
        for variant in variants:
            if variant == icon_name:
                continue
            url = f"https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/{variant}.svg"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                filename = f"{company}.svg"
                filepath = LOGO_DIR / filename
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(response.text)
                return True, filename
        
        return False, None
    except Exception as e:
        log(f"下载 {company} 失败: {e}")
        return False, None


def download_all_logos():
    """主下载循环"""
    state = load_state()
    init_markdown()
    
    log(f"=== YOLO Logo Downloader 启动 ===")
    log(f"开始时间: {START_TIME.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"计划结束: {END_TIME.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"目标: 下载尽可能多的 logo\n")
    
    index = len(state["downloaded"]) + 1
    start_idx = state.get("last_company_index", 0)
    
    for i, company in enumerate(COMPANY_LIST[start_idx:], start=start_idx):
        # 检查是否超时
        now = datetime.now()
        if now >= END_TIME:
            log(f"\n=== 时间到！已达到4小时限制 ===")
            log(f"结束时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            break
        
        # 已下载则跳过
        if company in state["downloaded"]:
            continue
        
        # 更新进度
        remaining = END_TIME - now
        log(f"[{i+1}/{len(COMPANY_LIST)}] 下载 {company}... (剩余时间: {remaining})")
        
        # 下载
        success, filename = download_from_simple_icons(company, state)
        
        if success:
            state["downloaded"].append(company)
            update_markdown(index, company, filename, "simple-icons", "✅ 成功")
            log(f"  ✓ 成功: {filename}")
            index += 1
        else:
            state["failed"].append(company)
            update_markdown(index, company, "-", "simple-icons", "❌ 失败")
            log(f"  ✗ 失败")
        
        state["last_company_index"] = i + 1
        save_state(state)
        
        # 短暂延迟避免请求过快
        time.sleep(0.5)
    
    # 总结
    log(f"\n=== 下载完成 ===")
    log(f"成功: {len(state['downloaded'])}")
    log(f"失败: {len(state['failed'])}")
    log(f"记录文件: {RECORD_FILE}")


if __name__ == "__main__":
    try:
        download_all_logos()
    except KeyboardInterrupt:
        log("\n用户中断")
        save_state(load_state())
    except Exception as e:
        log(f"\n发生错误: {e}")
        save_state(load_state())
