import streamlit as st
import pandas as pd
import plotly.express as px

# 設定頁面寬度與標題
st.set_page_config(layout="wide", page_title="個人財務健康看板")

st.title("📊 個人資產負債管理與財務健康檢查")

# --- 側邊欄：輸入資料 ---
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
        # 這裡帶入您於 2025-12-26 提到的房貸遞減型壽險相關資產價值
        other_assets = st.number_input("保險/其他資產 (含房貸壽險)", value=2827446)

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

# --- 第一層：核心指標看板 ---
st.subheader("💰 核心資產概況")
m1, m2, m3 = st.columns(3)
m1.metric("淨資產 (Net Worth)", f"${net_worth:,.0f} TWD")
m2.metric("總資產 (Total Assets)", f"${total_assets:,.0f}")
m3.metric("總負債 (Total Liabilities)", f"${total_liabilities:,.0f}")

st.divider()

# --- 第二層：資產配置視覺化 ---
col_chart, col_table = st.columns([6, 4])

# 準備資產分布數據
asset_dist_df = pd.DataFrame({
    "資產類別": ["現金與定存", "股票投資", "不動產", "保險與其他"],
    "金額": [total_cash, total_stock, real_estate, other_assets]
})

with col_chart:
    st.subheader("🎨 資產配置比例")
    fig = px.pie(
        asset_dist_df, 
        values='金額', 
        names='資產類別',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=350)
    st.plotly_chart(fig, use_container_width=True)

with col_table:
    st.subheader("📝 資產明細")
    asset_dist_df["佔比"] = asset_dist_df["金額"].apply(lambda x: f"{(x/total_assets)*100:.1f}%")
    asset_dist_df["金額"] = asset_dist_df["金額"].apply(lambda x: f"${x:,.0f}")
    st.table(asset_dist_df)

st.divider()

# --- 第三層：財務健康檢查 (五大指標) ---
st.subheader("🩺 財務健康診斷")
h1, h2, h3, h4, h5 = st.columns(5)

with h1:
    status = "🔴 過高" if debt_to_asset_ratio > 40 else "🟢 健康"
    st.metric("負債比", f"{debt_to_asset_ratio:.1f}%")
    st.caption(f"基準 < 40% ({status})")

with h2:
    status = "🔴 壓力大" if loan_burden_ratio > 30 else "🟢 適中"
    st.metric("貸款負擔比", f"{loan_burden_ratio:.1f}%")
    st.caption(f"基準 < 30% ({status})")

with h3:
    if 3 <= emergency_fund_ratio <= 6:
        status = "🟢 理想"
    elif emergency_fund_ratio < 3:
        status = "🔴 不足"
    else:
        status = "🟡 充裕"
    st.metric("預備金倍數", f"{emergency_fund_ratio:.1f} 倍")
    st.caption(f"基準 3-6個月 ({status})")

with h4:
    status = "🔴 過高" if expense_to_income_ratio > 60 else "🟢 良好"
    st.metric("支出收入比", f"{expense_to_income_ratio:.1f}%")
    st.caption(f"基準 < 60% ({status})")

with h5:
    st.metric("淨資產收入倍數", f"{net_worth_income_multiple:.1f} 倍")
    st.caption("財務獨立度指標")

st.divider()

# --- 底部：更新與提醒 ---
if st.button("🚀 更新數據分析"):
    st.toast("數據已根據您的輸入重新計算！")
    st.balloons()

st.info(f"💡 提醒：資產項目已包含您於 2025-12-26 加保的房貸遞減型壽險價值。建議定期檢視不動產估值以維持負債比的準確性。")
