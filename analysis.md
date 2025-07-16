The following chart shows how wallet credit scores are distributed from 0 to 1000 in gap of 100.
<img width="1000" height="600" alt="score_distribution" src="https://github.com/user-attachments/assets/ee15e875-31ef-44be-b412-392d3df4a1dc" />
 
Wallet Counts by Score Range:
1. 0-100         25 wallets
2. 100-200     2331 wallets
3. 200-300      839 wallets
4. 300-400      276 wallets
5. 400-500       26 wallets
6. 500-600        0 wallets
7. 600-700        0 wallets
8. 700-800        0 wallets
9. 800-900        0 wallets
10. 900-1000       0 wallets

Wallet Behaviour in Low Score Ranges (0-300)
- Low repay-to-borrow ratio or no repayment at all.
- Usually experienced at least one liquidationcall event.
- Little activity (few total txs, or very short history).
- Only executed one action type (i.e., just borrows - no deposits/repayments).
These wallet types exhibited risky/robotic/exploitative behaviour.

Wallet Behaviour in High Score Ranges (700-1000)
- High repay-to-borrow ratio (many repayments for each borrow).
- No liquidation events.
- High transaction diversity — performed multiple types of DeFi actions.
- Many active days — actively participated in the protocol on an ongoing basis.
These wallets appear to be responsible, long-term users, which allows for trust and integrity.
