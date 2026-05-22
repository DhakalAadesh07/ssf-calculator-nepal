# 🇳🇵 Nepal SSF Pension Calculator

A free, open-source calculator for Nepal's **Social Security Fund (SSF)** that shows how much pension you will receive at retirement — based on your salary, age, and expected salary growth.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/ssf-nepal-calculator/blob/main/ssf_calculator.ipynb)

> ⚠️ **Before sharing:** Replace `YOUR_USERNAME` in the badge link above with your actual GitHub username.

---

## ▶️ Run it instantly — no installation needed

Click the **Open in Colab** badge above. It opens in your browser and runs in Google's free cloud — no Python, no setup required.

**Steps inside Colab:**
1. Click **Runtime → Run all** from the top menu, OR
2. Run Cell 2 first (loads the calculator), then Cell 4 (enter your details)
3. Edit the 4 values in Cell 4 to match your situation and press **Shift + Enter**

---

## 📊 What it calculates

| Output | Description |
|---|---|
| **Monthly pension** | What you receive every month from age 60 (corpus ÷ 160) |
| **Gratuity (lump sum)** | The 8.33% you can withdraw when you leave your job |
| **Insurance consumed** | The 2.67% spent on medical, accident & dependent coverage |
| **Year-by-year table** | How your pension and gratuity corpus grow over time |
| **0% vs 5% comparison** | Side-by-side projection with and without investment returns |

---

## 💡 How SSF contributions are split (31% of basic salary)

| Portion | Rate | What happens |
|---|---|---|
| Pension Fund | 20% | 🔒 Locked until age 60. Monthly pension = corpus ÷ 160 |
| Gratuity Fund | 8.33% | ✅ Withdrawable as lump sum when you leave your job |
| Medical / Maternity insurance | 1.00% | ❌ Consumed — covers up to NPR 1,00,000/yr at empanelled hospitals |
| Accident & Disability insurance | 1.40% | ❌ Consumed — workplace accident coverage from day 1 |
| Dependent Family insurance | 0.27% | ❌ Consumed — pension for spouse/children if you pass away |
| **Total** | **31%** | |

---

## 🖥️ Run locally (developers)

```bash
git clone https://github.com/YOUR_USERNAME/ssf-nepal-calculator.git
cd ssf-nepal-calculator
python3 ssf_calculator.py
```

No external dependencies — pure Python 3, standard library only.

---

## 📁 Files

| File | Description |
|---|---|
| `ssf_calculator.py` | Command-line Python script |
| `ssf_calculator.ipynb` | Jupyter notebook (use this with Colab) |
| `README.md` | This file |

---

## ⚖️ Legal basis

- Contribution-Based Social Security Act, 2074 (2017)
- Social Security Scheme Operation Procedure, 2075
- Official portal: [ssf.gov.np](https://ssf.gov.np)

> **Disclaimer:** This is an estimate tool. Actual SSF returns and pension amounts are determined by the SSF Board and reviewed every 3 years. Consult SSF directly for official figures.

---

## 🤝 Contributing

Pull requests welcome! If SSF rules change (rates, formula, caps), please open an issue or PR with a source link.

---

*Built for Nepal's private sector workers to understand their SSF entitlements.*
