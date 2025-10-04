# dcf_shareprice_v5_table.py
# -------------------------------------------------------------
# Share-price DCF with ONLY a 3x3 table output:
#   rows:  value (price), period (PV explicit), term (PV terminal)
#   cols:  Low / Base / High
# Fixed discount rate across scenarios.
# Toggle terminal method: Exit Multiple OR Gordon Growth.
# We discount **per-share** NI or FCF (your choice).
# -------------------------------------------------------------

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Share-Price DCF — 3×3 Table", layout="centered")

# ---------- helpers ----------
def discount_factors(n, r):
    t = np.arange(1, n + 1, dtype=float)     # year-end
    return 1.0 / ((1.0 + r) ** t)

def gordon_tv_per_share(next_ps, r, g):
    if g >= r:
        raise ValueError("Terminal growth must be < discount rate.")
    return next_ps / (r - g)

def exit_multiple_tv_per_share(last_ps, m):
    return last_ps * m

def build_series(base_total, growth_list, start_shares, buybacks):
    """Return per-share series, totals, and shares path for N years."""
    n = len(growth_list)
    totals = np.zeros(n)
    shares = np.zeros(n)
    totals[0] = base_total * (1 + growth_list[0])
    shares[0] = max(0.0, start_shares - buybacks[0])
    for i in range(1, n):
        totals[i] = totals[i-1] * (1 + growth_list[i])
        shares[i] = max(0.0, shares[i-1] - buybacks[i])
    per_share = np.divide(totals, np.maximum(shares, 1e-9))
    return per_share, totals, shares

def price_from_per_share(per_share, disc, term_method, term_params):
    """Return tuple (pv_explicit_ps, pv_term_ps, price_ps)."""
    n = len(per_share)
    dfs = discount_factors(n, disc)
    pv_explicit_ps = float(np.sum(per_share * dfs))
    last_ps = per_share[-1]
    if term_method == "Gordon Growth":
        g = term_params["g"]
        tv_at_n = gordon_tv_per_share(last_ps * (1 + g), disc, g)
    else:
        m = term_params["multiple"]
        tv_at_n = exit_multiple_tv_per_share(last_ps, m)
    pv_term_ps = tv_at_n / ((1 + disc) ** n)
    return pv_explicit_ps, pv_term_ps, pv_explicit_ps + pv_term_ps

# ---------- sidebar inputs ----------
st.sidebar.title("Assumptions")

metric_mode = st.sidebar.selectbox(
    "Discount which metric?",
    ["Net Income (per share)", "Free Cash Flow (per share)"]
)

years = st.sidebar.number_input("Projection years (N)", 3, 20, 7, 1)
disc_rate = st.sidebar.number_input("Discount rate (Cost of equity, %)", 0.0, 40.0, 9.0, 0.1) / 100.0  # FIXED for all scenarios

st.sidebar.subheader("Totals, shares, buybacks")
base_total = st.sidebar.number_input(
    f"Base total ({'NI' if metric_mode.startswith('Net') else 'FCF'}, $m)",
    min_value=0.0, value=500.0, step=10.0, format="%.2f"
)
start_shares = st.sidebar.number_input("Starting shares (millions)", 0.0, 1e7, 250.0, 1.0, format="%.0f")
buybacks_str = st.sidebar.text_input("Buybacks per year (millions)", value="0,0,2,2,3,3,3")

# Common buybacks for all scenarios
try:
    bb = [float(x.strip()) for x in buybacks_str.split(",") if x.strip()]
    if len(bb) < years: bb += [0.0] * (years - len(bb))
    else: bb = bb[:years]
except Exception:
    st.error("Buybacks must be comma-separated numbers (millions).")
    st.stop()

st.sidebar.subheader("Growth by scenario (% per year)")
g_low_str  = st.sidebar.text_input("Low growth path",  value="6,5,4,3,3,3,3")
g_base_str = st.sidebar.text_input("Base growth path", value="8,7,6,5,4,3,2")
g_high_str = st.sidebar.text_input("High growth path", value="10,9,8,7,6,5,4")

def parse_growth(s):
    gl = [float(x.strip())/100.0 for x in s.split(",") if x.strip()]
    if len(gl) < years: gl += [gl[-1]] * (years - len(gl))
    else: gl = gl[:years]
    return gl

try:
    g_low, g_base, g_high = parse_growth(g_low_str), parse_growth(g_base_str), parse_growth(g_high_str)
except Exception:
    st.error("Growth paths must be comma-separated percentages.")
    st.stop()

term_method = st.sidebar.selectbox("Terminal method", ["Exit Multiple", "Gordon Growth"])
if term_method == "Exit Multiple":
    m_low  = st.sidebar.number_input("Low multiple (× last per-share)",  1.0, 60.0, 12.0, 0.5)
    m_base = st.sidebar.number_input("Base multiple (× last per-share)", 1.0, 60.0, 15.0, 0.5)
    m_high = st.sidebar.number_input("High multiple (× last per-share)", 1.0, 60.0, 18.0, 0.5)
    term_params = [ {"multiple": m_low}, {"multiple": m_base}, {"multiple": m_high} ]
    col_labels = ["using multiple (low)", "using multiple (base)", "using multiple (high)"]
else:
    gl_low  = st.sidebar.number_input("Low terminal g (%)",  -5.0, 12.0, 1.5, 0.1) / 100.0
    gl_base = st.sidebar.number_input("Base terminal g (%)", -5.0, 12.0, 2.5, 0.1) / 100.0
    gl_high = st.sidebar.number_input("High terminal g (%)", -5.0, 12.0, 3.0, 0.1) / 100.0
    term_params = [ {"g": gl_low}, {"g": gl_base}, {"g": gl_high} ]
    col_labels = ["using growth (low)", "using growth (base)", "using growth (high)"]

# ---------- compute scenarios ----------
scenarios = [
    ("Low",  g_low,  term_params[0]),
    ("Base", g_base, term_params[1]),
    ("High", g_high, term_params[2]),
]

period_vals, term_vals, total_vals = [], [], []

for name, growth, tp in scenarios:
    ps, _, _ = build_series(base_total, growth, start_shares, bb)
    pv_exp_ps, pv_term_ps, price_ps = price_from_per_share(ps, disc_rate, term_method, tp)
    period_vals.append(pv_exp_ps)
    term_vals.append(pv_term_ps)
    total_vals.append(price_ps)

# ---------- single output table ----------
table = pd.DataFrame(
    {
        col_labels[0]: [total_vals[0], period_vals[0], term_vals[0]],
        col_labels[1]: [total_vals[1], period_vals[1], term_vals[1]],
        col_labels[2]: [total_vals[2], period_vals[2], term_vals[2]],
    },
    index=["value", "period", "term"],
)

st.dataframe(table.style.format("{:,.4f}"), use_container_width=True)
