"""
Nepal Social Security Fund (SSF) Calculator
============================================
Based on Contribution-Based Social Security Act, 2074 (2017)
and Social Security Scheme Operation Procedure, 2075.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FULL CONTRIBUTION STRUCTURE (31% of basic salary)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  EMPLOYEE pays 11%:
    • 10.00% → Pension Fund (provident fund portion)     [LOCKED until 60]
    •  1.00% → Medical/Health/Maternity insurance        [consumed, NOT withdrawable]
    ──────────
    NOTE: The employee's 1% insurance share is included within the 2.67% total
    insurance pool. The remaining 1.67% comes from employer.

  EMPLOYER pays 20%:
    • 10.00% → Pension Fund (provident fund portion)     [LOCKED until 60]
    •  8.33% → Gratuity / Retirement Fund                [withdrawable on termination]
    •  1.40% → Accident & Disability insurance           [consumed, NOT withdrawable]
    •  0.27% → Dependent Family Protection insurance     [consumed, NOT withdrawable]
    ──────────
    TOTAL EMPLOYER OLD AGE = 18.33% (10% PF + 8.33% gratuity)

  COMBINED OLD AGE = 28.33%:
    • Pension Fund  = 20.00%  (employee 10% + employer 10%)  → monthly pension ÷ 160
    • Gratuity Fund =  8.33%  (employer only)                → lump sum on termination

  INSURANCE PREMIUMS = 2.67%  (1% medical + 1.4% accident + 0.27% dependent)
    → Consumed as coverage. NOT accumulated. NOT withdrawable.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LUMP SUM (GRATUITY) WITHDRAWAL RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅  The GRATUITY portion (8.33%) CAN be withdrawn as a lump sum
      when you resign or leave your job — at any time.
  ❌  The PENSION portion (20%) CANNOT be withdrawn until age 60.
      It is locked and paid out only as monthly pension (corpus ÷ 160).
  ⚠   Exception: Contributors enrolled BEFORE July 15, 2021 who did NOT
      opt into the Pension Scheme may withdraw the full 28.33% as lump sum.

SALARY CAP: NPR 1,00,000/month (per this calculator's spec).
"""


def format_npr(amount: float) -> str:
    """Format amount in NPR with Indian numbering (e.g. 12,34,567)."""
    amount = round(amount)
    sign = "-" if amount < 0 else ""
    s = str(abs(amount))
    if len(s) <= 3:
        return f"NPR {sign}{s}"
    last3 = s[-3:]
    rest = s[:-3]
    parts = []
    while len(rest) > 2:
        parts.append(rest[-2:])
        rest = rest[:-2]
    if rest:
        parts.append(rest)
    parts.reverse()
    return f"NPR {sign}{','.join(parts)},{last3}"


def calculate_ssf(
    basic_salary: float,
    current_age: int,
    annual_increment_pct: float = 2.0,
    annual_return_pct: float = 0.0,
    salary_cap: float = 100_000,
    retirement_age: int = 60,
) -> dict:
    """
    Calculate SSF pension and gratuity accumulation until retirement.

    The 28.33% old-age corpus is split into:
      - Pension Fund  : 20%   (employee 10% + employer 10%) — paid as monthly pension
      - Gratuity Fund :  8.33% (employer only)              — withdrawable as lump sum

    Parameters
    ----------
    basic_salary         : Current monthly basic salary (NPR)
    current_age          : Current age in years
    annual_increment_pct : Annual salary increment % (default 2%)
    annual_return_pct    : Annual investment return on corpus % (default 0%)
    salary_cap           : Max monthly basic for SSF contribution (default 1,00,000)
    retirement_age       : Target retirement age (default 60)
    """
    if current_age >= retirement_age:
        raise ValueError(
            f"Current age ({current_age}) must be less than retirement age ({retirement_age})."
        )

    years_to_retire = retirement_age - current_age

    # ── Contribution rate constants ──────────────────────────────────────────
    EMPLOYEE_RATE       = 0.11      # total employee deduction
    EMPLOYER_RATE       = 0.20      # total employer contribution
    TOTAL_RATE          = 0.31

    # Old Age split
    PENSION_RATE        = 0.20      # employee 10% + employer 10% → locked pension
    GRATUITY_RATE       = 0.0833    # employer 8.33% → withdrawable lump sum

    # Insurance (consumed, not accumulated)
    MEDICAL_RATE        = 0.0100    # employer 1% medical/maternity
    ACCIDENT_RATE       = 0.0140    # employer 1.4% accident/disability
    DEPENDENT_RATE      = 0.0027    # employer 0.27% dependent family
    INSURANCE_RATE      = MEDICAL_RATE + ACCIDENT_RATE + DEPENDENT_RATE  # = 0.0267

    monthly_return = (1 + annual_return_pct / 100.0) ** (1 / 12) - 1

    # Accumulators
    pension_corpus   = 0.0
    gratuity_corpus  = 0.0

    total_employee_paid      = 0.0
    total_employer_paid      = 0.0
    total_pension_contrib    = 0.0
    total_gratuity_contrib   = 0.0
    total_insurance_consumed = 0.0

    salary = basic_salary
    yearly_breakdown = []

    for year in range(1, years_to_retire + 1):
        yr_pension   = 0.0
        yr_gratuity  = 0.0
        yr_insurance = 0.0
        yr_employee  = 0.0
        yr_employer  = 0.0

        for _ in range(12):
            s = min(salary, salary_cap)

            m_pension   = s * PENSION_RATE
            m_gratuity  = s * GRATUITY_RATE
            m_insurance = s * INSURANCE_RATE
            m_employee  = s * EMPLOYEE_RATE
            m_employer  = s * EMPLOYER_RATE

            # Grow existing corpus then add this month's contribution
            pension_corpus  = pension_corpus  * (1 + monthly_return) + m_pension
            gratuity_corpus = gratuity_corpus * (1 + monthly_return) + m_gratuity

            yr_pension   += m_pension
            yr_gratuity  += m_gratuity
            yr_insurance += m_insurance
            yr_employee  += m_employee
            yr_employer  += m_employer

        total_pension_contrib    += yr_pension
        total_gratuity_contrib   += yr_gratuity
        total_insurance_consumed += yr_insurance
        total_employee_paid      += yr_employee
        total_employer_paid      += yr_employer

        yearly_breakdown.append({
            "year": year,
            "age": current_age + year,
            "monthly_basic_effective": round(min(salary, salary_cap), 2),
            "annual_pension_contrib": round(yr_pension, 2),
            "annual_gratuity_contrib": round(yr_gratuity, 2),
            "annual_insurance_consumed": round(yr_insurance, 2),
            "pension_corpus_eoy": round(pension_corpus, 2),
            "gratuity_corpus_eoy": round(gratuity_corpus, 2),
        })

        salary = salary * (1 + annual_increment_pct / 100.0)

    total_old_age_corpus = pension_corpus + gratuity_corpus
    monthly_pension = pension_corpus / 160

    return {
        "inputs": {
            "basic_salary": basic_salary,
            "effective_start_salary": min(basic_salary, salary_cap),
            "current_age": current_age,
            "retirement_age": retirement_age,
            "years_to_retire": years_to_retire,
            "annual_increment_pct": annual_increment_pct,
            "annual_return_pct": annual_return_pct,
            "salary_cap": salary_cap,
        },
        "totals": {
            "total_employee_paid": round(total_employee_paid, 2),
            "total_employer_paid": round(total_employer_paid, 2),
            "total_all_paid": round(total_employee_paid + total_employer_paid, 2),
            "total_pension_contrib": round(total_pension_contrib, 2),
            "total_gratuity_contrib": round(total_gratuity_contrib, 2),
            "total_old_age_contrib": round(total_pension_contrib + total_gratuity_contrib, 2),
            "total_insurance_consumed": round(total_insurance_consumed, 2),
        },
        "pension_corpus": round(pension_corpus, 2),
        "gratuity_corpus": round(gratuity_corpus, 2),
        "total_old_age_corpus": round(total_old_age_corpus, 2),
        "monthly_pension": round(monthly_pension, 2),
        "annual_pension": round(monthly_pension * 12, 2),
        "yearly_breakdown": yearly_breakdown,
    }


def print_report(result: dict, label: str = "") -> None:
    inp = result["inputs"]
    tot = result["totals"]
    eff = inp["effective_start_salary"]
    W = 65

    header = "NEPAL SSF PENSION CALCULATOR"
    if label:
        header += f"  [{label}]"

    print("\n" + "=" * W)
    print(f"  {header}")
    print("=" * W)

    # ── INPUTS ──────────────────────────────────────────────────────────────
    print("\n📥  INPUTS")
    print(f"   Monthly basic salary         : {format_npr(inp['basic_salary'])}")
    if inp["basic_salary"] > inp["salary_cap"]:
        print(f"   ⚠  Salary capped at          : {format_npr(inp['salary_cap'])}")
    print(f"   Current age                  : {inp['current_age']} yrs")
    print(f"   Retirement age               : {inp['retirement_age']} yrs")
    print(f"   Years until retirement       : {inp['years_to_retire']} yrs")
    print(f"   Annual salary increment      : {inp['annual_increment_pct']}%")
    print(f"   Annual return on corpus      : {inp['annual_return_pct']}%")

    # ── MONTHLY CONTRIBUTION BREAKDOWN ──────────────────────────────────────
    print("\n📊  MONTHLY CONTRIBUTION BREAKDOWN  (at starting salary)")
    print(f"   {'─'*55}")
    print(f"   EMPLOYEE pays 11%            : {format_npr(eff * 0.11)}")
    print(f"     → Pension Fund (10%)       : {format_npr(eff * 0.10)}")
    print(f"     → Medical insurance (1%)   : {format_npr(eff * 0.01)}  ❌ not withdrawable")
    print(f"   {'─'*55}")
    print(f"   EMPLOYER pays 20%            : {format_npr(eff * 0.20)}")
    print(f"     → Pension Fund (10%)       : {format_npr(eff * 0.10)}")
    print(f"     → Gratuity Fund (8.33%)    : {format_npr(eff * 0.0833)}")
    print(f"     → Accident ins. (1.4%)     : {format_npr(eff * 0.014)}  ❌ not withdrawable")
    print(f"     → Dependent ins. (0.27%)   : {format_npr(eff * 0.0027)}  ❌ not withdrawable")
    print(f"   {'─'*55}")
    print(f"   TOTAL (31%)                  : {format_npr(eff * 0.31)}")
    print(f"     → Pension Fund (20%)       : {format_npr(eff * 0.20)}  🔒 locked until 60")
    print(f"     → Gratuity Fund (8.33%)    : {format_npr(eff * 0.0833)}  ✅ withdrawable anytime")
    print(f"     → Insurance total (2.67%)  : {format_npr(eff * 0.0267)}  ❌ consumed as coverage")

    # ── LIFETIME TOTALS ──────────────────────────────────────────────────────
    print("\n📈  LIFETIME CONTRIBUTION TOTALS  (over all years)")
    print(f"   Total paid by employee       : {format_npr(tot['total_employee_paid'])}")
    print(f"   Total paid by employer       : {format_npr(tot['total_employer_paid'])}")
    print(f"   {'─'*55}")
    print(f"   Total paid into SSF          : {format_npr(tot['total_all_paid'])}")
    print(f"     → Into Pension Fund (20%)  : {format_npr(tot['total_pension_contrib'])}")
    print(f"     → Into Gratuity Fund(8.33%): {format_npr(tot['total_gratuity_contrib'])}")
    print(f"     → Insurance consumed(2.67%): {format_npr(tot['total_insurance_consumed'])}  ❌ gone")

    # ── CORPUS AT RETIREMENT ─────────────────────────────────────────────────
    print("\n🏦  ACCUMULATED CORPUS AT RETIREMENT (age 60)")
    ret_note = f"+ {inp['annual_return_pct']}% p.a. returns" if inp['annual_return_pct'] > 0 else "no investment returns"
    print(f"   [{ret_note}]")
    print(f"   Pension corpus  (20%)        : {format_npr(result['pension_corpus'])}")
    print(f"   Gratuity corpus (8.33%)      : {format_npr(result['gratuity_corpus'])}")
    print(f"   Total Old Age corpus (28.33%): {format_npr(result['total_old_age_corpus'])}")

    # ── GRATUITY NOTE ────────────────────────────────────────────────────────
    print("\n💼  GRATUITY (Lump Sum — available on job termination)")
    print(f"   ┌{'─'*55}┐")
    print(f"   │  The 8.33% gratuity corpus can be withdrawn as a       │")
    print(f"   │  lump sum ANYTIME you leave your job (before or at 60).│")
    print(f"   │                                                         │")
    print(f"   │  Gratuity amount at retirement : {format_npr(result['gratuity_corpus']):<22} │")
    print(f"   │                                                         │")
    print(f"   │  ⚠  The 20% pension corpus CANNOT be withdrawn early.  │")
    print(f"   │     It is locked and paid only as monthly pension.      │")
    print(f"   └{'─'*55}┘")

    # ── PENSION ──────────────────────────────────────────────────────────────
    print("\n🏖️  MONTHLY PENSION  (from age 60, if 15+ years contributed)")
    print(f"   ┌{'─'*55}┐")
    print(f"   │  Formula: Pension Corpus (20%) ÷ 160                    │")
    print(f"   │                                                         │")
    print(f"   │  Pension corpus             : {format_npr(result['pension_corpus']):<22} │")
    print(f"   │  Monthly pension            : {format_npr(result['monthly_pension']):<22} │")
    print(f"   │  Annual pension             : {format_npr(result['annual_pension']):<22} │")
    print(f"   └{'─'*55}┘")

    if inp["years_to_retire"] < 15:
        print(f"\n   ⚠  WARNING: Only {inp['years_to_retire']} yrs of contributions.")
        print(f"      Monthly pension requires 15+ years. Gratuity still available.")

    # ── YEAR-BY-YEAR TABLE ───────────────────────────────────────────────────
    print("\n📅  YEAR-BY-YEAR GROWTH  (every 5 years + first + last)")
    print(f"   {'Yr':<5} {'Age':<5} {'Basic (eff)':<16} {'Pension Corpus':<18} {'Gratuity Corpus'}")
    print(f"   {'─'*68}")
    for row in result["yearly_breakdown"]:
        show = (
            row["year"] == 1
            or row["year"] % 5 == 0
            or row["year"] == inp["years_to_retire"]
        )
        if show:
            print(
                f"   {row['year']:<5} {row['age']:<5} "
                f"{format_npr(row['monthly_basic_effective']):<16} "
                f"{format_npr(row['pension_corpus_eoy']):<18} "
                f"{format_npr(row['gratuity_corpus_eoy'])}"
            )

    print("\n" + "=" * W)
    print("  ⓘ  Figures are projections. Actual SSF returns set by Board.")
    print("  ⓘ  Pension reviewed every 3 years for inflation.")
    print("  ⓘ  Source: SSF Act 2074 / Scheme Operation Procedure 2075")
    print("=" * W + "\n")


def get_float_input(prompt: str, default: float = None) -> float:
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            val = float(raw)
            if val < 0:
                print("  ⚠  Please enter a positive number.")
                continue
            return val
        except ValueError:
            print("  ⚠  Invalid input. Please enter a number.")


def get_int_input(prompt: str, min_val: int = 0, max_val: int = 120) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if val < min_val or val > max_val:
                print(f"  ⚠  Please enter a value between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("  ⚠  Invalid input. Please enter a whole number.")


def main():
    print("\n╔══════════════════════════════════════════════════╗")
    print("║       Nepal SSF Pension Calculator               ║")
    print("║   Based on SSF Act 2074 & Scheme Rules 2075      ║")
    print("╚══════════════════════════════════════════════════╝\n")

    basic_salary = get_float_input("  Monthly BASIC salary (NPR): ")
    current_age  = get_int_input(  "  Current age (years): ", min_val=18, max_val=59)
    increment    = get_float_input("  Annual salary increment % [Enter = 2%]: ", default=2.0)
    return_rate  = get_float_input("  Assumed annual return on corpus % [Enter = 0%]: ", default=0.0)

    try:
        result_base = calculate_ssf(
            basic_salary=basic_salary,
            current_age=current_age,
            annual_increment_pct=increment,
            annual_return_pct=return_rate,
        )

        # Always show the user's chosen scenario
        label = f"{return_rate}% return" if return_rate > 0 else "0% return — conservative"
        print_report(result_base, label=label)

        # Always also show the 5% comparison alongside
        result_5 = calculate_ssf(
            basic_salary=basic_salary,
            current_age=current_age,
            annual_increment_pct=increment,
            annual_return_pct=5.0,
        )

        print("\n" + "─" * 65)
        print("  📊  COMPARISON: 0% vs 5% annual return on corpus")
        print("─" * 65)
        base_label = f"{return_rate}% return" if return_rate != 0.0 else "0% (no returns)"
        print(f"  {'Metric':<38} {base_label:<20} {'5% annual return'}")
        print(f"  {'─'*75}")
        metrics = [
            ("Pension corpus (20%)",      "pension_corpus"),
            ("Gratuity corpus (8.33%)",   "gratuity_corpus"),
            ("Total old age corpus",      "total_old_age_corpus"),
            ("Monthly pension (÷160)",    "monthly_pension"),
            ("Annual pension",            "annual_pension"),
        ]
        for label_m, key in metrics:
            v0 = result_base[key]
            v5 = result_5[key]
            print(f"  {label_m:<38} {format_npr(v0):<20} {format_npr(v5)}")
        print()

    except ValueError as e:
        print(f"\n  ❌ Error: {e}\n")


if __name__ == "__main__":
    main()