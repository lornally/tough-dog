import os
import shutil

# 读取需要的 logo 列表
with open('logo_names.txt', 'r') as f:
    needed = [line.strip() for line in f if line.strip()]

# 可用的 simple-icons
icons_dir = 'simple-icons/icons'
available = {f.replace('.svg', ''): f for f in os.listdir(icons_dir) if f.endswith('.svg')}

# 匹配映射
mappings = {
    '3m': '3m',
    'abbott-laboratories': 'abbott',
    'abbvie': 'abbvie',
    'accenture-plc': 'accenture',
    'adobe': 'adobe',
    'advanced-micro-devices': 'amd',
    'alphabet': None,  # 需要特殊处理
    'amazon.com': 'amazon',
    'american-airlines-group': 'americanairlines',
    'american-express': 'americanexpress',
    'apple': 'apple',
    'bank-of-america': 'bankofamerica',
    'berkshire-hathaway': None,
    'boeing': 'boeing',
    'bristol-myers-squibb': 'bristolsquibb',
    'caterpillar': 'caterpillar',
    'chevron': 'chevron',
    'cisco-systems': 'cisco',
    'citigroup': 'citrix',  # 或者 citi
    'coca-cola': 'cocacola',
    'costco-wholesale': None,
    'danaher': None,
    'dell-technologies': 'dell',
    'disney': 'disney',
    'ebay': 'ebay',
    'eli-lilly-and': 'lilly',
    'exxon-mobil': None,
    'facebook': 'facebook',
    'fedex': 'fedex',
    'ford-motor': None,
    'general-electric': None,
    'general-motors': None,
    'goldman-sachs-group': 'goldmansachs',
    'home-depot': 'homedepot',
    'honeywell-international': 'honeywell',
    'hp': 'hp',
    'ibm': 'ibm',
    'intel': 'intel',
    'intuit': 'intuit',
    'johnson-&-johnson': 'johnsonandjohnson',
    'jpmorgan-chase-&': 'jpmorganchase',
    'mastercard': 'mastercard',
    "mcdonald's": 'mcdonalds',
    'merck-&': 'merck',
    'microsoft': 'microsoft',
    'netflix': 'netflix',
    'nike': 'nike',
    'nvidia': 'nvidia',
    'oracle': 'oracle',
    'paypal-holdings': 'paypal',
    'pepsico': 'pepsi',
    'pfizer': 'pfizer',
    'procter-&-gamble': 'procterandgamble',
    'qualcomm': 'qualcomm',
    'salesforce': 'salesforce',
    'starbucks': 'starbucks',
    'tesla': 'tesla',
    'texas-instruments': 'texasinstruments',
    'uber-technologies': 'uber',
    'union-pacific': 'unionpacific',
    'unitedhealth-group': 'unitedhealthgroup',
    'ups': 'ups',
    'verizon-communications': 'verizon',
    'visa': 'visa',
    'walmart': 'walmart',
    'wells-fargo-&': 'wellsfargo',
}

matched = 0
not_found = []

for name in needed:
    simple_name = mappings.get(name)
    if simple_name and simple_name in available:
        src = os.path.join(icons_dir, available[simple_name])
        dst = os.path.join('us', f'{name}.svg')
        shutil.copy(src, dst)
        print(f"✓ {name} -> {available[simple_name]}")
        matched += 1
    else:
        not_found.append(name)

print(f"\n匹配成功: {matched}/{len(needed)}")
print(f"未找到: {', '.join(not_found)}")
