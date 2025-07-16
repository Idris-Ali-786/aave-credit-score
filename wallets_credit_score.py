import json
import pandas as pd
from collections import defaultdict
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

with open("/home/idrisali/Downloads/user-wallet-transactions.json", "r") as f:
    raw_data = json.load(f)

df = pd.DataFrame(raw_data)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
df = df[['userWallet', 'timestamp', 'action', 'actionData']]

wallet_features = defaultdict(lambda: {
    'num_deposits': 0,
    'num_borrows': 0,
    'num_repays': 0,
    'num_redeems': 0,
    'num_liquidations': 0,
    'borrowed_usd': 0.0,
    'repaid_usd': 0.0,
    'active_days': set(),
    'actions_set': set()
})

for _, row in df.iterrows():
    wallet = row['userWallet']
    action = row['action'].lower()
    data = row['actionData']
    timestamp = row['timestamp']

    wallet_features[wallet]['actions_set'].add(action)
    wallet_features[wallet]['active_days'].add(timestamp.date())

    if action == 'deposit':
        wallet_features[wallet]['num_deposits'] += 1
    elif action == 'borrow':
        wallet_features[wallet]['num_borrows'] += 1
        try:
            amount = float(data.get('amount', '0'))
            price = float(data.get('assetPriceUSD', '1'))
            wallet_features[wallet]['borrowed_usd'] += (amount / 1e18) * price
        except:
            pass
    elif action == 'repay':
        wallet_features[wallet]['num_repays'] += 1
        try:
            amount = float(data.get('amount', '0'))
            price = float(data.get('assetPriceUSD', '1'))
            wallet_features[wallet]['repaid_usd'] += (amount / 1e18) * price
        except:
            pass
    elif action == 'redeemunderlying':
        wallet_features[wallet]['num_redeems'] += 1
    elif action == 'liquidationcall':
        wallet_features[wallet]['num_liquidations'] += 1

processed = []
for wallet, feats in wallet_features.items():
    borrows = feats['num_borrows']
    repays = feats['num_repays']
    ratio = repays / borrows if borrows > 0 else 0

    processed.append({
        'wallet': wallet,
        'num_deposits': feats['num_deposits'],
        'num_borrows': borrows,
        'num_repays': repays,
        'num_redeems': feats['num_redeems'],
        'num_liquidations': feats['num_liquidations'],
        'borrowed_usd': feats['borrowed_usd'],
        'repaid_usd': feats['repaid_usd'],
        'repay_borrow_ratio': ratio,
        'active_days': len(feats['active_days']),
        'transaction_diversity': len(feats['actions_set']),
    })

features_df = pd.DataFrame(processed)

def calculate_score(row):
    score = 100 

    score += min(row['repay_borrow_ratio'] * 100, 200)
    score += min(row['active_days'], 100)
    score += min(row['transaction_diversity'] * 20, 100)
    score -= min(row['num_liquidations'] * 50, 200)

    return max(0, min(1000, score)) 

features_df['credit_score'] = features_df.apply(calculate_score, axis=1)
features_df.to_csv("wallet_scores.csv", index=False)
print("Credit scores saved to wallet_scores.csv")

features_df['score_range'] = pd.cut(
    features_df['credit_score'],
    bins=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
    right=False,
    labels=[
        '0-100', '100-200', '200-300', '300-400', '400-500',
        '500-600', '600-700', '700-800', '800-900', '900-1000'
    ]
)
wallet_range_counts = features_df['score_range'].value_counts().sort_index()
print("\n Wallet Counts by Score Range:")
print(wallet_range_counts)

plt.figure(figsize=(10,6))
wallet_range_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Credit Score Distribution")
plt.xlabel("Score Range")
plt.ylabel("Number of Wallets")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("score_distribution.png")

print("Score distribution plot saved to score_distribution.png")
