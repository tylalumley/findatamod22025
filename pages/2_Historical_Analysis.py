import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Page configuration
st.set_page_config(page_title="Historical Analysis", layout="wide")

# Title
st.title("📊 Historical Financial Analysis")
st.markdown("Analyze historical performance to understand growth patterns, margins, and reinvestment behavior")

# Quick navigation at top
col1, col2, col3 = st.columns([3, 1, 1])
with col2:
    if st.button("💼 ← WACC Calculator", use_container_width=True):
        st.switch_page("pages/1_WACC_Calculator.py")
with col3:
    if st.button("🎯 DCF Valuation →", use_container_width=True):
        st.switch_page("pages/3_DCF_Valuation.py")

st.divider()

# Sidebar for inputs
st.sidebar.header("Input Parameters")

# Ticker input
ticker_symbol = st.sidebar.text_input("Ticker Symbol", value="MSFT").upper()

# Tax rate inputs
eff_tax_rate = st.sidebar.number_input("Effective Tax Rate (%)", min_value=0.0, max_value=100.0, value=19.0, step=1.0) / 100
marg_tax_rate = st.sidebar.number_input("Marginal Tax Rate (%)", min_value=0.0, max_value=100.0, value=25.0, step=1.0) / 100

# Scale factor
scale_factor = 1000000
scale_name = 'M'

# Analyze button
if st.sidebar.button("Analyze Company", type="primary"):
    try:
        with st.spinner(f"Fetching data for {ticker_symbol}..."):
            # Create ticker object
            ticker = yf.Ticker(ticker_symbol)
            company_name = ticker.info.get('longName', ticker_symbol)

            # Get financial statements
            income_statement_df = ticker.income_stmt.T.sort_index()
            balance_sheet_df = ticker.balance_sheet.T.sort_index()
            cash_flows_df = ticker.cashflow.T.sort_index()

            if income_statement_df.empty:
                st.error(f"Could not fetch data for ticker {ticker_symbol}. Please check the ticker symbol.")
                st.stop()

        # Display company name
        st.header(f"{company_name} ({ticker_symbol})")
        st.markdown(f"**Historical Analysis based on {len(income_statement_df)} years of annual data**")

        # ====================
        # SECTION 1: INCOME STATEMENT ANALYSIS
        # ====================
        st.subheader("1. Income Statement Analysis")

        # Extract key columns
        key_is_cols = ['Total Revenue', 'EBIT', 'Gross Profit']

        # Check if EBITDA exists, if not calculate it
        if 'EBITDA' not in income_statement_df.columns:
            if 'EBIT' in income_statement_df.columns and 'Depreciation And Amortization' in cash_flows_df.columns:
                # Need to merge to get D&A
                income_statement_df = income_statement_df.join(cash_flows_df[['Depreciation And Amortization']], how='left')
                income_statement_df['EBITDA'] = income_statement_df['EBIT'] + income_statement_df['Depreciation And Amortization']

        # Display key metrics
        is_display_df = income_statement_df[key_is_cols].copy() / scale_factor
        st.dataframe(is_display_df.style.format("{:,.2f}"), use_container_width=True)

        # Calculate margins
        income_statement_df['Gross Margin'] = income_statement_df['Gross Profit'] / income_statement_df['Total Revenue']
        income_statement_df['EBIT Margin'] = income_statement_df['EBIT'] / income_statement_df['Total Revenue']

        if 'EBITDA' in income_statement_df.columns:
            income_statement_df['EBITDA Margin'] = income_statement_df['EBITDA'] / income_statement_df['Total Revenue']

        # Calculate growth rates
        income_statement_df['Revenue Growth'] = income_statement_df['Total Revenue'].pct_change()
        income_statement_df['EBIT Growth'] = income_statement_df['EBIT'].pct_change()

        # Display growth rates and margins
        st.markdown("#### Growth Rates & Margins")

        if 'EBITDA Margin' in income_statement_df.columns:
            growth_margin_cols = ['Revenue Growth', 'EBIT Growth', 'Gross Margin', 'EBIT Margin', 'EBITDA Margin']
        else:
            growth_margin_cols = ['Revenue Growth', 'EBIT Growth', 'Gross Margin', 'EBIT Margin']

        growth_margin_df = income_statement_df[growth_margin_cols].copy()
        st.dataframe(growth_margin_df.style.format("{:.2%}"), use_container_width=True)

        # Visualization: Revenue and EBIT trends
        st.markdown("#### Revenue & EBIT Trends")
        fig, ax = plt.subplots(figsize=(12, 5))

        years = income_statement_df.index.year
        ax.plot(years, income_statement_df['Total Revenue'] / scale_factor, marker='o', linewidth=2, label='Revenue', color='#1f77b4')
        ax.plot(years, income_statement_df['EBIT'] / scale_factor, marker='s', linewidth=2, label='EBIT', color='#ff7f0e')

        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel(f'Amount (${scale_name})', fontsize=12)
        ax.set_title(f'{ticker_symbol} Revenue & EBIT Over Time', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

        # Visualization: Margins over time
        st.markdown("#### Margin Trends")
        fig2, ax2 = plt.subplots(figsize=(12, 5))

        ax2.plot(years, income_statement_df['Gross Margin'] * 100, marker='o', linewidth=2, label='Gross Margin', color='#2ca02c')
        ax2.plot(years, income_statement_df['EBIT Margin'] * 100, marker='s', linewidth=2, label='EBIT Margin', color='#d62728')

        if 'EBITDA Margin' in income_statement_df.columns:
            ax2.plot(years, income_statement_df['EBITDA Margin'] * 100, marker='^', linewidth=2, label='EBITDA Margin', color='#9467bd')

        ax2.set_xlabel('Year', fontsize=12)
        ax2.set_ylabel('Margin (%)', fontsize=12)
        ax2.set_title(f'{ticker_symbol} Margin Trends', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=11)
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linestyle='--', linewidth=0.5)

        st.pyplot(fig2)

        # ====================
        # SECTION 2: BALANCE SHEET ANALYSIS
        # ====================
        st.subheader("2. Balance Sheet Analysis - Net Working Capital")

        # Calculate NWC components
        balance_sheet_df['Adj CA'] = balance_sheet_df['Current Assets'] - balance_sheet_df['Cash Cash Equivalents And Short Term Investments']
        balance_sheet_df['Adj CL'] = balance_sheet_df['Current Liabilities'] - balance_sheet_df.get('Current Debt', 0)
        balance_sheet_df['NWC'] = balance_sheet_df['Adj CA'] - balance_sheet_df['Adj CL']
        balance_sheet_df['Ch in NWC'] = balance_sheet_df['NWC'].diff()

        # Display NWC
        nwc_cols = ['Current Assets', 'Current Liabilities', 'Cash Cash Equivalents And Short Term Investments', 'NWC', 'Ch in NWC']
        nwc_display_cols = [col for col in nwc_cols if col in balance_sheet_df.columns or col in ['NWC', 'Ch in NWC']]

        nwc_df = balance_sheet_df[nwc_display_cols].copy() / scale_factor
        st.dataframe(nwc_df.style.format("{:,.2f}"), use_container_width=True)

        # ====================
        # SECTION 3: CASH FLOW STATEMENT ANALYSIS
        # ====================
        st.subheader("3. Cash Flow Statement Analysis")

        # Reverse sign of CapEx to make it positive
        cash_flows_df['Capital Expenditure'] = -cash_flows_df['Capital Expenditure']

        # Display key cash flow metrics
        cf_cols = ['Capital Expenditure', 'Depreciation And Amortization']
        cf_df = cash_flows_df[cf_cols].copy() / scale_factor
        st.dataframe(cf_df.style.format("{:,.2f}"), use_container_width=True)

        # ====================
        # SECTION 4: REINVESTMENT ANALYSIS
        # ====================
        st.subheader("4. Reinvestment Analysis")

        # Merge cash flows and NWC
        merged_cfs = cash_flows_df.join(balance_sheet_df[['NWC', 'Ch in NWC']])

        # Calculate Reinvestment
        merged_cfs['Reinvestment'] = merged_cfs['Capital Expenditure'] - merged_cfs['Depreciation And Amortization'] + merged_cfs['Ch in NWC']

        # Calculate NOPAT
        if 'Tax Rate For Calcs' in income_statement_df.columns:
            income_statement_df['NOPAT'] = income_statement_df['EBIT'] * (1 - income_statement_df['Tax Rate For Calcs'])
        else:
            income_statement_df['NOPAT'] = income_statement_df['EBIT'] * (1 - eff_tax_rate)

        # Merge NOPAT with reinvestment
        nopat_reinv_df = income_statement_df[['NOPAT']].join(merged_cfs[['Reinvestment']])

        # Calculate Reinvestment Rate
        nopat_reinv_df['Reinvestment Rate'] = nopat_reinv_df['Reinvestment'] / nopat_reinv_df['NOPAT']

        # Display
        st.markdown("#### NOPAT, Reinvestment & Reinvestment Rate")
        display_reinv = nopat_reinv_df.copy()
        display_reinv[['NOPAT', 'Reinvestment']] = display_reinv[['NOPAT', 'Reinvestment']] / scale_factor

        # Format differently for dollar amounts vs percentages
        styled_df = display_reinv.style.format({
            'NOPAT': '{:,.2f}',
            'Reinvestment': '{:,.2f}',
            'Reinvestment Rate': '{:.2%}'
        })
        st.dataframe(styled_df, use_container_width=True)

        # Visualization: Reinvestment Rate over time
        st.markdown("#### Reinvestment Rate Trend")
        fig3, ax3 = plt.subplots(figsize=(12, 5))

        years = nopat_reinv_df.index.year
        ax3.bar(years, nopat_reinv_df['Reinvestment Rate'] * 100, color='#17becf', alpha=0.7, edgecolor='black')

        ax3.set_xlabel('Year', fontsize=12)
        ax3.set_ylabel('Reinvestment Rate (%)', fontsize=12)
        ax3.set_title(f'{ticker_symbol} Reinvestment Rate Over Time', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

        st.pyplot(fig3)

        # ====================
        # SECTION 5: SUMMARY STATISTICS
        # ====================
        st.subheader("5. Summary Statistics Table")

        # Create final summary dataframe
        if 'Tax Rate For Calcs' in income_statement_df.columns:
            summary_cols = ['Revenue Growth', 'EBIT Growth', 'Gross Margin', 'EBIT Margin', 'Tax Rate For Calcs']
        else:
            # Add effective tax rate as a column
            income_statement_df['Effective Tax Rate'] = eff_tax_rate
            summary_cols = ['Revenue Growth', 'EBIT Growth', 'Gross Margin', 'EBIT Margin', 'Effective Tax Rate']

        df_stats = income_statement_df[summary_cols].copy()
        df_stats = df_stats.join(nopat_reinv_df[['Reinvestment Rate']])

        st.dataframe(df_stats.style.format("{:.2%}"), use_container_width=True)

        # Key insights
        st.markdown("#### 📈 Key Insights")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            avg_rev_growth = income_statement_df['Revenue Growth'].mean()
            st.metric("Avg Revenue Growth", f"{avg_rev_growth:.2%}")

        with col2:
            avg_ebit_margin = income_statement_df['EBIT Margin'].mean()
            st.metric("Avg EBIT Margin", f"{avg_ebit_margin:.2%}")

        with col3:
            avg_reinv_rate = nopat_reinv_df['Reinvestment Rate'].mean()
            st.metric("Avg Reinvestment Rate", f"{avg_reinv_rate:.2%}")

        with col4:
            latest_nopat = nopat_reinv_df['NOPAT'].iloc[-1] / scale_factor
            st.metric(f"Latest NOPAT (${scale_name})", f"{latest_nopat:,.2f}")

        # ====================
        # DOWNLOAD SECTION
        # ====================
        st.subheader("📥 Download Results")

        # Prepare export dataframe
        export_df = df_stats.copy()
        export_df['NOPAT ($M)'] = nopat_reinv_df['NOPAT'] / scale_factor
        export_df['Reinvestment ($M)'] = nopat_reinv_df['Reinvestment'] / scale_factor

        csv = export_df.to_csv()
        st.download_button(
            label="Download Historical Analysis as CSV",
            data=csv,
            file_name=f"{ticker_symbol}_historical_analysis.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your inputs and try again. Make sure the ticker symbol is valid.")

else:
    st.info("👈 Enter a ticker symbol in the sidebar and click 'Analyze Company' to begin")

    # Show example
    st.markdown("### What This Tool Does")
    st.markdown("""
    This Historical Analysis module helps you understand a company's past financial performance
    by analyzing:

    **1. Income Statement Metrics**
    - Revenue and EBIT trends
    - Growth rates over time
    - Profitability margins (Gross, EBIT, EBITDA)

    **2. Balance Sheet Metrics**
    - Net Working Capital (NWC)
    - Changes in NWC over time

    **3. Cash Flow Metrics**
    - Capital Expenditures (CapEx)
    - Depreciation & Amortization (D&A)

    **4. Reinvestment Analysis**
    - Total Reinvestment = CapEx - D&A + Change in NWC
    - NOPAT (Net Operating Profit After Tax)
    - Reinvestment Rate = Reinvestment / NOPAT

    **5. Visual Trends**
    - Revenue and earnings growth
    - Margin stability
    - Reinvestment patterns

    This analysis provides the foundation for making informed projections in the DCF Valuation model.
    """)

    st.markdown("### Example Usage")
    st.markdown("""
    1. Enter a ticker symbol (e.g., MSFT, AAPL, GOOGL)
    2. Adjust tax rates if you have specific information
    3. Click 'Analyze Company'
    4. Review the historical trends and patterns
    5. Use these insights to inform your DCF projections
    """)

# Navigation buttons at the bottom
st.divider()
st.markdown("### 🔄 Next Steps")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("← Back to WACC Calculator", use_container_width=True):
        st.switch_page("pages/1_WACC_Calculator.py")
with col2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")
with col3:
    if st.button("🎯 Go to DCF Valuation →", use_container_width=True, type="primary"):
        st.switch_page("pages/3_DCF_Valuation.py")
