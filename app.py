import streamlit as st
import pandas as pd

# 設定頁面寬度
st.set_page_config(layout="wide", page_title="個人資產負債表")

st.title("📊 個人資產負債表管理")

# --- 側邊欄：輸入資料 ---
with st.sidebar:
    st.header("數據輸入")
    date_val = st.date_input("報告日期")
    
    st.subheader("資產輸入")
    cash_tw = st.number_input("台幣現金", value=315905)
    cash_ext = st.number_input("外幣現金", value=588203)
    cash_fixed = st.number_input("台幣定存", value=1800000)
    
    stock_tw = st.number_input("台股", value=1134698)
    stock_us = st.number_input("美股", value=10463977)
    
    st.subheader("負債輸入")
    loan_short = st.number_input("短期負債 (信貸/質押)", value=3119392)
    loan_long = st.number_input("長期負債 (房貸)", value=15252853)

# --- 計算邏輯 ---
total_cash = cash_tw + cash_ext + cash_fixed
total_stock = stock_tw + stock_us
# 這裡固定資產先用你圖片中的數字作為範例
real_estate = 16200000 + 30690000 
total_assets = total_cash + total_stock + real_estate + 412082 + 2415364

total_liabilities = loan_short + loan_long
net_worth = total_assets - total_liabilities
debt_ratio = (total_liabilities / total_assets) * 100

# --- 介面呈現 ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🟠 資產 (Assets)")
    asset_df = pd.DataFrame({
        "項目": ["現金小計", "股票小計", "固定資產", "保險/其他"],
        "金額 (TWD)": [total_cash, total_stock, real_estate, 2827446]
    })
    asset_df["佔比"] = asset_df["金額 (TWD)"].apply(lambda x: f"{(x/total_assets)*100:.1f}%")
    st.table(asset_df)
    st.metric("總資產計", f"{total_assets:,.0f}")

with col2:
    st.markdown("### 🟢 負債 (Liabilities)")
    debt_df = pd.DataFrame({
        "項目": ["短期負債", "長期負債"],
        "金額 (TWD)": [loan_short, loan_long]
    })
    st.table(debt_df)
    st.metric("負債總計", f"{total_liabilities:,.0f}", delta=f"負債比 {debt_ratio:.1f}%", delta_color="inverse")

st.divider()

# --- 淨資產呈現 ---
st.balloons() if st.button("更新數據") else None
st.subheader(f"💰 淨資產 (Net Worth): {net_worth:,.0f} TWD")
