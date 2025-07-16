# aave-credit-score
DeFi credit scoring using Aave V2 transaction data

Method Chosen: Rule-based, feature-engineered scoring system
Type: Heuristic model

Architecture and Processing flow
1. Load JSON File:
 - Read raw transaction data from 'user-wallet-transactions.json'.
2. Preprocess:
 - Convert timestamps and keep relevant fields.
3. Feature Engineering:
 - For each wallet, compute features like:
 - Number of deposits, borrows, repays, redeems, and liquidations.
 - USD value of borrows and repays.
 - Repay-to-borrow ratio.
 - Number of active days.
 - Transaction diversity.
4. Scoring Logic:
 - Initialize base score = 100
 - Add:
 - +min(repay_borrow_ratio * 100, 200)
 - +min(active_days, 100)
 - +min(transaction_diversity * 20, 100)
 - Subtract:
 - -min(num_liquidations * 50, 200)
 - give score between 0 and 1000.
5. Output:
 - Scores are saved in 'wallet_scores.csv'.
 - Bin scores are in range (0-100, 100-200, ..., 900-1000).
 - Bar chart is saved as 'score_distribution.png'.

Generated Files
- wallet_scores.csv: Credit scores per wallet.
- score_distribution.png: Histogram of score distribution.
- wallets_credit_score.py: Main Python script.
- analysis.md: Score distribution + wallet behavior insights.
