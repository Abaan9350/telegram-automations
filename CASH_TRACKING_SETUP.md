# Cash Tracking Setup Guide

## ✅ Code Changes Complete

The bot now correctly tracks Bank and Cash separately:
- Column E (Remaining) = **Bank Balance ONLY**
- Cash is tracked separately in a summary section
- `/expense` and `/income` = Bank (default)
- `/expensecash` and `/incomecash` = Cash

---

## 📋 Manual Excel Sheet Changes Required

### Current Sheet Structure:
```
A: Date
B: Item
C: Expenses
D: Income
E: Remaining (Bank Balance)
F: Description
G: Payment Method (NEW)
H: Category
```

---

## Step-by-Step Setup:

### **Step 1: Add Payment Method Column (Column G)**

1. Click on column G header
2. Insert a new column if needed
3. In cell **G1**, type: `Payment Method`
4. For **ALL existing transaction rows** (rows with data in columns C or D):
   - Fill column G with the value: `Bank`
   - You can select all cells in column G for existing rows and type "Bank", then Ctrl+D to fill down

---

### **Step 2: Fix All Existing "Remaining" Formulas (Column E)**

Your existing rows have the old formula that doesn't filter by payment method. You need to update them.

**For each row that has a transaction** (starting from row 2 or wherever your first transaction is):

**OLD formula in E3:**
```
=IF(OR(C3<>"", D3<>""), SUM($D$2:D3) - SUM($C$2:C3), "")
```

**NEW formula in E3:**
```
=IF(OR(C3<>"",D3<>""), SUMIF($G$2:$G3,"Bank",$D$2:$D3) - SUMIF($G$2:$G3,"Bank",$C$2:$C3), "")
```

**For E4:**
```
=IF(OR(C4<>"",D4<>""), SUMIF($G$2:$G4,"Bank",$D$2:$D4) - SUMIF($G$2:$G4,"Bank",$C$2:$C4), "")
```

**Pattern:** Replace row 3 with the actual row number in each formula.

**Quick way to update all at once:**
1. Go to the first transaction row (e.g., E2 or E3)
2. Delete the old formula
3. Type this formula (adjust the row number):
   ```
   =IF(OR(C2<>"",D2<>""), SUMIF($G$2:$G2,"Bank",$D$2:$D2) - SUMIF($G$2:$G2,"Bank",$C$2:$C2), "")
   ```
4. Press Enter
5. Copy this cell and paste it down to all other transaction rows
6. The row numbers will auto-increment correctly

---

### **Step 3: Create Cash Balance Tracker**

Add this in an **unused area** of your sheet (e.g., columns J, K, L):

**In cells J1:L4, create this summary table:**

```
J1: SUMMARY
K1: (empty)
L1: (empty)

J2: Starting Cash
K2: 4000
L2: (empty)

J3: Cash Balance
K3: =K2 + SUMIF($G:$G,"Cash",$D:$D) - SUMIF($G:$G,"Cash",$C:$C)
L3: (formula calculates: Starting Cash + Cash Income - Cash Expenses)

J4: Total Money
K4: =SUMIF($G:$G,"Bank",$D:$D)-SUMIF($G:$G,"Bank",$C:$C) + K3
L4: (formula: Bank Balance + Cash Balance)
```

**Exact setup:**

| J | K | L |
|---|---|---|
| **SUMMARY** | | |
| Starting Cash | 4000 | |
| Cash Balance | `=K2 + SUMIF($G:$G,"Cash",$D:$D) - SUMIF($G:$G,"Cash",$C:$C)` | |
| Total Money | `=SUMIF($G:$G,"Bank",$D:$D)-SUMIF($G:$G,"Bank",$C:$C) + K3` | |

---

### **Step 4: Optional - Add Bank Balance Summary**

If you want to also show Bank Balance in the summary:

**In J5:K5:**

```
J5: Bank Balance
K5: =SUMIF($G:$G,"Bank",$D:$D) - SUMIF($G:$G,"Bank",$C:$C)
```

---

## 🎯 Final Sheet Layout:

### Main Transaction Area (Columns A-H):
```
Date | Item | Expenses | Income | Remaining(Bank) | Description | Payment Method | Category
-----------------------------------------------------------------------------------------
31 Jul 26 | stipend | | 10,968.00 | 10968 | last kpmg stipend | Bank | 
1 Aug 26 | Turf | 165 | | 10803 | | Bank | Entertainment
2 Aug 26 | mamma | 10000 | | 803 | | Bank | 
2 Aug 26 | Turf Agnels | 220 | | 583 | | Bank | Entertainment
(future cash transaction example)
27 Aug 26 | turf | 200 | | 583 | paid in cash | Cash | Entertainment
```

### Summary Area (Columns J-K):
```
SUMMARY
Starting Cash    | 4000
Cash Balance     | 3800  (after ₹200 cash expense example)
Total Money      | 4383  (Bank: 583 + Cash: 3800)
Bank Balance     | 583
```

---

## ✅ Verification Checklist:

After setup, verify:
- [ ] Column G exists with header "Payment Method"
- [ ] All existing transactions have "Bank" in column G
- [ ] All formulas in column E use SUMIF with "Bank" filter
- [ ] Summary section shows Starting Cash = 4000
- [ ] Summary section shows calculated Cash Balance
- [ ] Summary section shows calculated Total Money
- [ ] New bank transactions via `/expense` or `/income` affect column E
- [ ] New cash transactions via `/expensecash` or `/incomecash` do NOT affect column E, but DO affect Cash Balance in summary

---

## 🧪 Test After Setup:

1. **Test bank transaction:**
   - Send: `/expense test 100`
   - Check: Column E should decrease by 100
   - Check: Cash Balance in summary should NOT change

2. **Test cash transaction:**
   - Send: `/expensecash snacks 50`
   - Check: Column E should NOT change
   - Check: Cash Balance in summary should decrease by 50
   - Check: Payment Method column should show "Cash"

---

## 📊 How It Works:

**Bank Remaining (Column E):**
- Calculates: `SUM(Bank Income) - SUM(Bank Expenses)`
- Only counts rows where column G = "Bank"
- Shows your current bank account balance

**Cash Balance (Summary K3):**
- Calculates: `Starting Cash (4000) + SUM(Cash Income) - SUM(Cash Expenses)`
- Only counts rows where column G = "Cash"
- Shows your current cash on hand

**Total Money (Summary K4):**
- Calculates: `Bank Balance + Cash Balance`
- Shows your total wealth across both sources

---

## 🔄 Future Transactions:

From now on, the bot will automatically:
- Set column G to "Bank" for `/expense` and `/income`
- Set column G to "Cash" for `/expensecash` and `/incomecash`
- Insert the correct SUMIF formula in column E that only counts Bank transactions

**No more manual formula updates needed after this initial setup!**

---

## ⚠️ Important Notes:

1. **Do NOT add the ₹4,000 starting cash as a transaction row** in columns A-H. It lives only in the summary section (K2).

2. **Column E (Remaining)** will now ONLY show your bank balance. If you want to see your total wealth, look at "Total Money" in the summary.

3. **Cash transactions will appear in your transaction list** (columns A-H) but will NOT affect the Bank Remaining column (E).

4. **Category column (H)** continues to work as before for both Bank and Cash transactions.

---

## Need Help?

If something doesn't work after setup:
1. Check that column G exists and has "Bank" for existing rows
2. Check that column E formulas include SUMIF with "Bank" filter
3. Check that summary formulas reference the correct columns
4. Restart the bot after code changes

Happy tracking! 🎉
