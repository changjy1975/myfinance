import streamlit as st
import pandas as pd
import plotly.express as px

# 設定頁面寬度與標題
st.set_page_config(layout="wide", page_title="財務健康管理系統")

st.title("📊 個人資產負債管理與財務健康檢查")

# --- 側邊欄：數據輸入 ---
with st.sidebar:
    st.header("⚙️ 數據輸入")
    report_date = st.date_input("報告日期")
    
    with st.expander("💰 資產項目", expanded=True):
        cash_tw = st.number_input("台幣現金", value=315905)
        cash_ext = st.number_input("外幣現金", value=588203)
        cash_fixed = st.number_input("台幣定存", value=1800000)
        stock_tw = st.number_input("台股總值", value=1134698)
        stock_us = st.number_input("美股總值", value=10463977)
        real_estate = st.number_input("不動產估值", value=46890000)
        other_assets = st.number_input("保險/其他資產", value=2827446)

    with st.expander("💸 負債項目", expanded=True):
        loan_short = st.number_input("短期負債 (信貸/質押)", value=3119392)
        loan_long = st.number_input("長期負債 (房貸)", value=15252853)
        monthly_repayment = st.number_input("每月貸款支出 (本息和)", value=85000)

    with st.expander("📈 收支項目", expanded=True):
        monthly_income = st.number_input("每月常態收入 (稅後)", value=200000)
        monthly_expense = st.number_input("每月常態支出", value=80000)

# --- 計算邏輯 ---
total_cash = cash_tw + cash_ext + cash_fixed
total_stock = stock_tw + stock_us
total_assets = total_cash + total_stock + real_estate + other_assets
total_liabilities = loan_short + loan_long
net_worth = total_assets - total_liabilities

# 指標計算
debt_to_asset_ratio = (total_liabilities / total_assets) * 100
loan_burden_ratio = (monthly_repayment / monthly_income) * 100
emergency_fund_ratio = total_cash / monthly_expense
expense_to_income_ratio = (monthly_expense / monthly_income) * 100
net_worth_income_multiple = net_worth / (monthly_income * 12)

# --- 第一層：核心數據看板 ---
m1, m2, m3 = st.columns(3)
m1.metric("淨資產 (Net Worth)", f"${net_worth:,.0f}")
m2.metric("總資產 (Total Assets)", f"${total_assets:,.0f}")
m3.metric("總負債 (Total Liabilities)", f"${total_liabilities:,.0f}")

st.divider()

# --- 第二層：資產分布與視覺化 (移至診斷前) ---
st.subheader("🎨 資產配置分佈")
col_chart, col_table = st.columns([6, 4])

asset_dist_df = pd.DataFrame({
    "資產類別": ["現金與定存", "股票投資", "不動產", "保險與其他"],
    "金額": [total_cash, total_stock, real_estate, other_assets]
})

with col_chart:
    fig = px.pie(asset_dist_df, values='金額', names='資產類別', hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(margin=dict(t=20, b=20, l=0, r=0), height=350)
    st.plotly_chart(fig, use_container_width=True)

with col_table:
    asset_dist_df["佔比"] = asset_dist_df["金額"].apply(lambda x: f"{(x/total_assets)*100:.1f}%")
    asset_dist_df["金額 (TWD)"] = asset_dist_df["金額"].apply(lambda x: f"${x:,.0f}")
    st.table(asset_dist_df[["資產類別", "金額 (TWD)", "佔比"]])

st.divider()

# --- 第三層：財務健康診斷 (五大指標) ---
st.subheader("🩺 財務健康診斷")
h1, h2, h3, h4, h5 = st.columns(5)

with h1:
    is_debt_ok = debt_to_asset_ratio <= 40
    st.metric("負債比", f"{debt_to_asset_ratio:.1f}%")
    st.caption("🟢 健康" if is_debt_ok else "🔴 負債偏高")

with h2:
    is_loan_ok = loan_burden_ratio <= 30
    st.metric("貸款負擔比", f"{loan_burden_ratio:.1f}%")
    st.caption("🟢 壓力適中" if is_loan_ok else "🔴 壓力較大")

with h3:
    if 3 <= emergency_fund_ratio <= 6:
        status = "🟢 理想"
        is_emergency_ok = True
    elif emergency_fund_ratio < 3:
        status = "🔴 嚴重不足"
        is_emergency_ok = False
    else:
        status = "🟡 資金閒置"
        is_emergency_ok = True
    st.metric("預備金倍數", f"{emergency_fund_ratio:.1f} 倍")
    st.caption(status)

with h4:
    is_expense_ok = expense_to_income_ratio <= 60
    st.metric("支出收入比", f"{expense_to_income_ratio:.1f}%")
    st.caption("🟢 儲蓄強健" if is_expense_ok else "🔴 支出過度")

with h5:
    st.metric("淨資產倍數", f"{net_worth_income_multiple:.1f} 倍")
    st.caption("財務獨立度指標")

# --- 第四層：自動化操作建議專區 ---
st.markdown("### 💡 根據診斷結果的財務操作建議")
suggestions = []

if not is_debt_ok:
    suggestions.append("⚠️ **降低槓桿**：負債比超過 40%，建議檢視「短期負債」的利息成本，並評估是否適度變現部分高獲利資產進行償還。")
if not is_loan_ok:
    suggestions.append("⚠️ **優化現金流**：貸款負擔比超過月入 30%，建議評估房貸轉貸或延長年限，以減輕每月現金流壓力。")
if emergency_fund_ratio < 3:
    suggestions.append("⚠️ **補足防禦力**：緊急預備金不足，應優先累積現金儲備，暫緩新的大額投資。")
elif emergency_fund_ratio > 6:
    suggestions.append("✅ **資金活用**：現金儲備極為充裕，建議將超過 6 個月的閒置資金分批配置於具流動性的息收資產。")
if not is_expense_ok:
    suggestions.append("⚠️ **開支審查**：年度支出佔比較高，建議定期盤點固定支出（如訂閱費、非必要分期付款）以提升儲蓄率。")
if is_debt_ok and is_loan_ok and (3 <= emergency_fund_ratio <= 6) and is_expense_ok:
    suggestions.append("🌟 **財務極為穩健**：各項指標均在優良區間，建議維持現有策略，並可專注於提升投資組合的抗通膨能力。")

for s in suggestions:
    st.info(s)

if st.button("🚀 更新數據分析"):
    st.balloons()
