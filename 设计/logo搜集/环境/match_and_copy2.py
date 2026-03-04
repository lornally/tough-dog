import os
import shutil

icons_dir = 'simple-icons/icons'
available = {f.replace('.svg', ''): f for f in os.listdir(icons_dir) if f.endswith('.svg')}

# 补充映射
more_mappings = {
    'adobe': 'adobe',
    'amazon.com': 'amazon',
    'alphabet': 'google',  # Alphabet 是 Google 母公司
    'bristol-myers-squibb': 'bristolsquibb',
    'chevron': 'chevron',
    'disney': 'disney',
    'eli-lilly-and': 'lilly',
    'ford-motor': 'ford',
    'general-electric': 'generalelectric',
    'general-motors': 'generalmotors',
    'home-depot': 'homedepot',
    'honeywell-international': 'honeywell',
    'ibm': 'ibm',
    'johnson-&-johnson': 'jnj',  # 或 johnsonandjohnson
    'jpmorgan-chase-&': 'jpmorganchase',
    'microsoft': 'microsoft',
    'oracle': 'oracle',
    'pepsico': 'pepsi',
    'pfizer': 'pfizer',
    'procter-&-gamble': 'procterandgamble',
    'salesforce': 'salesforce',
    'texas-instruments': 'texasinstruments',
    'union-pacific': 'unionpacific',
    'unitedhealth-group': 'unitedhealthgroup',
    'walmart': 'walmart',
    # 检查这些是否可用
    'berkshire-hathaway': None,
    'costco-wholesale': None,
    'danaher': None,
    'exxon-mobil': None,
}

matched = 0
for name, simple_name in more_mappings.items():
    if simple_name and simple_name in available:
        src = os.path.join(icons_dir, available[simple_name])
        dst = os.path.join('us', f'{name}.svg')
        if not os.path.exists(dst):
            shutil.copy(src, dst)
            print(f"✓ {name} -> {available[simple_name]}")
            matched += 1
    else:
        print(f"✗ {name} -> {simple_name} (not found)")

print(f"\n新增匹配: {matched}")
