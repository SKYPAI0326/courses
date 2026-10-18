#!/usr/bin/env python3
"""
L0 Truth Table 生成範本

用法：
1. 複製此檔到課程目錄 `_validation/L0-generate.py`
2. 修改下方「課程客製」段，填入你的 dataset 路徑與要算的事實
3. 跑：python3 _validation/L0-generate.py
4. 產出：_validation/L0-truth-table.json + L0-{dataset}-truth.txt

設計原則：
- 全部用 Python 算，不要用 Excel（避免人為失誤）
- 每個 dataset 算「總筆數 / 總額 / Top N / 異常列表」基本 4 件事
- 教學埋點都要被 truth table 抓到
- 同一指標多種口徑（如 ABC 含/不含零銷售）都要算
"""

import csv
import json
from collections import defaultdict
from datetime import datetime

# ─────────────────────────────────────
# 通用工具函數
# ─────────────────────────────────────

def read_csv(path):
    """讀 CSV 回傳 list of dict"""
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def topn_by_field(rows, field, n=5, agg_field='金額'):
    """按 field 分組、agg_field 加總，回傳 Top N"""
    grouped = defaultdict(lambda: {'amount': 0, 'count': 0})
    for r in rows:
        key = r[field]
        grouped[key]['amount'] += int(r[agg_field])
        grouped[key]['count'] += int(r.get('數量', 1))
    sorted_items = sorted(grouped.items(), key=lambda x: -x[1]['amount'])
    return sorted_items[:n]


def abc_classify(rows, key_field, amount_field='金額',
                 a_threshold=0.80, b_threshold=0.95,
                 include_zero_sales=False, all_keys=None):
    """ABC 分類，回傳 dict"""
    by_key = defaultdict(int)
    for r in rows:
        by_key[r[key_field]] += int(r[amount_field])

    total = sum(by_key.values())
    sorted_items = sorted(by_key.items(), key=lambda x: -x[1])

    A, B, C = [], [], []
    running = 0
    for k, v in sorted_items:
        ratio = running / total
        if ratio < a_threshold:
            A.append(k)
        elif ratio < b_threshold:
            B.append(k)
        else:
            C.append(k)
        running += v

    # 處理零銷售
    zero_sales = []
    if all_keys and include_zero_sales:
        zero_sales = [k for k in all_keys if k not in by_key]
        C.extend(zero_sales)

    return {
        'A_count': len(A), 'B_count': len(B), 'C_count': len(C),
        'A_list': A, 'B_list': B, 'C_list': C,
        'zero_sales': zero_sales,
        'total_amount': total,
    }


# ─────────────────────────────────────
# 課程客製：以下依你的 dataset 修改
# ─────────────────────────────────────

DATASETS_DIR = 'assets/datasets/'  # 相對於課程根目錄

truth = {
    'generated_at': datetime.now().strftime('%Y-%m-%d'),
    'datasets': {},
}

# ─── 範例 1：訂單 / 銷售 dataset ───
def compute_orders():
    rows = read_csv(f'{DATASETS_DIR}your-orders.csv')
    top5 = topn_by_field(rows, 'SKU', n=5)
    total = sum(int(r['金額']) for r in rows)
    return {
        'total_rows': len(rows),
        'total_amount': total,
        'unique_skus': len(set(r['SKU'] for r in rows)),
        'top_5': [(k, v) for k, v in top5],
        'top_5_share': sum(v['amount'] for k, v in top5) / total,
    }

# truth['datasets']['orders'] = compute_orders()


# ─── 範例 2：費用 dataset（含異常埋點）───
def compute_expenses():
    rows = read_csv(f'{DATASETS_DIR}your-expenses.csv')

    # 教學埋點：手動標記異常 ID
    anomaly_ids_expected = ['E0010', 'E0021', 'E0050', 'E0063', 'E0130', 'E0152', 'E0188']
    anomaly_rules = {
        'E0010': '② 極小金額',
        'E0021': '① 大額',
        'E0050': '③ 分類矛盾 + ① 大額',
        'E0063': '④ 整數異常',
        'E0130': '⑤ 重複（與 E0188）',
        'E0152': '⑥ 時間異常',
        'E0188': '⑤ 重複（與 E0130）',
    }

    # 各分類平均（給後續對齊用）
    by_category = defaultdict(list)
    for r in rows:
        by_category[r['分類']].append(int(r['金額']))
    category_avg = {k: sum(v) / len(v) for k, v in by_category.items()}

    return {
        'total_rows': len(rows),
        'anomaly_ids_expected': anomaly_ids_expected,
        'anomaly_rules': anomaly_rules,
        'category_avg': category_avg,
    }

# truth['datasets']['expenses'] = compute_expenses()


# ─── 範例 3：業績趨勢 dataset ───
def compute_sales_trend():
    rows = read_csv(f'{DATASETS_DIR}your-sales.csv')

    # 按月加總
    by_month = defaultdict(int)
    for r in rows:
        month = r['日期'][:7]  # YYYY-MM
        by_month[month] += int(r['金額(萬)']) * 10000  # 換算為元

    sorted_months = sorted(by_month.items())

    # 算月度變化率
    changes = {}
    for i, (m, v) in enumerate(sorted_months):
        if i > 0:
            prev = sorted_months[i-1][1]
            changes[m] = (v - prev) / prev

    return {
        'total_rows': len(rows),
        'by_month': dict(sorted_months),
        'mom_changes': changes,
    }

# truth['datasets']['sales'] = compute_sales_trend()


# ─────────────────────────────────────
# 輸出
# ─────────────────────────────────────

if __name__ == '__main__':
    # 跑所有 compute 函數
    truth['datasets']['orders'] = compute_orders()
    # truth['datasets']['expenses'] = compute_expenses()
    # truth['datasets']['sales'] = compute_sales_trend()

    # 寫 JSON
    with open('_validation/L0-truth-table.json', 'w', encoding='utf-8') as f:
        json.dump(truth, f, ensure_ascii=False, indent=2, default=str)

    # 人類可讀輸出
    print('═══ L0 Truth Table ═══')
    for ds_name, ds in truth['datasets'].items():
        print(f'\n--- {ds_name} ---')
        for k, v in ds.items():
            if isinstance(v, (list, dict)) and len(str(v)) > 80:
                print(f'  {k}: {str(v)[:80]}...')
            else:
                print(f'  {k}: {v}')

    print(f'\n✓ 已寫入 _validation/L0-truth-table.json')
