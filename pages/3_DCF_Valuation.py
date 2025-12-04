import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime

# Page configuration
st.set_page_config(page_title="DCF Valuation", layout="wide")

# Title
st.title("🎯 DCF Valuation Model")
st.markdown("Project future cash flows and determine intrinsic share value using discounted cash flow analysis")

# Quick navigation at top
col1, col2, col3 = st.columns([3, 1, 1])
with col2:
    if st.button("💼 ← WACC Calculator", use_container_width=True):
        st.switch_page("pages/1_WACC_Calculator.py")
with col3:
    if st.button("📊 ← Historical Analysis", use_container_width=True):
        st.switch_page("pages/2_Historical_Analysis.py")

st.divider()

# Sidebar for inputs
st.sidebar.header("📊 DCF Model Inputs")

# Ticker input
ticker_symbol = st.sidebar.text_input("Ticker Symbol", value="MSFT").upper()

# Projection time horizon
time_horizon = st.sidebar.number_input("Projection Time Horizon (years)", min_value=5, max_value=15, value=10, step=1)

# Steady-state growth rate
ss_growth = st.sidebar.number_input("Steady-State Growth Rate (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.5) / 100

# Tax rate
eff_tax_rate = st.sidebar.number_input("Effective Tax Rate (%)", min_value=0.0, max_value=100.0, value=19.0, step=1.0) / 100

st.sidebar.divider()

# WACC Inputs
st.sidebar.markdown("### WACC (Discount Rate)")
st.sidebar.markdown("*You can enter WACC manually or use values from the WACC Calculator page*")

wacc_lower_input = st.sidebar.number_input("WACC Lower Bound (%)", min_value=0.0, max_value=50.0, value=7.96, step=0.1) / 100
wacc_mid_input = st.sidebar.number_input("WACC Middle Estimate (%)", min_value=0.0, max_value=50.0, value=9.25, step=0.1) / 100
wacc_upper_input = st.sidebar.number_input("WACC Upper Bound (%)", min_value=0.0, max_value=50.0, value=10.54, step=0.1) / 100

st.sidebar.divider()

# Projection Pattern Inputs
st.sidebar.markdown("### Projection Patterns")
st.sidebar.markdown("*Enter comma-separated values for each year*")

# Growth rate pattern
growth_pattern_str = st.sidebar.text_area(
    "Revenue Growth Rates (%)",
    value="20, 15, 15, 15, 10, 10, 10, 8, 8, 6",
    help=f"Enter {time_horizon} comma-separated growth rates"
)

# EBIT margin pattern
ebit_margin_str = st.sidebar.text_area(
    "EBIT Margins (%)",
    value="46, 46, 46, 46, 46, 46, 46, 46, 46, 46",
    help=f"Enter {time_horizon} comma-separated EBIT margins"
)

# Reinvestment rate pattern
reinv_rate_str = st.sidebar.text_area(
    "Reinvestment Rates (%)",
    value="40, 40, 30, 20, 20, 20, 20, 20, 20, 20",
    help=f"Enter {time_horizon} comma-separated reinvestment rates"
)

# Scale factor
scale_factor = 1000000
scale_name = 'M'

# Build DCF Model button
if st.sidebar.button("Build DCF Model", type="primary"):
    try:
        # Parse projection patterns
        try:
            growth_pattern = [float(x.strip())/100 for x in growth_pattern_str.split(',')]
            ebit_margin = [float(x.strip())/100 for x in ebit_margin_str.split(',')]
            reinv_rate_pattern = [float(x.strip())/100 for x in reinv_rate_str.split(',')]

            # Validate lengths
            if len(growth_pattern) != time_horizon:
                st.error(f"Growth pattern must have exactly {time_horizon} values. You provided {len(growth_pattern)}.")
                st.stop()
            if len(ebit_margin) != time_horizon:
                st.error(f"EBIT margin pattern must have exactly {time_horizon} values. You provided {len(ebit_margin)}.")
                st.stop()
            if len(reinv_rate_pattern) != time_horizon:
                st.error(f"Reinvestment rate pattern must have exactly {time_horizon} values. You provided {len(reinv_rate_pattern)}.")
                st.stop()

        except ValueError as e:
            st.error(f"Error parsing input patterns. Please ensure all values are numbers separated by commas: {str(e)}")
            st.stop()

        with st.spinner(f"Fetching data for {ticker_symbol}..."):
            # Create ticker object
            ticker = yf.Ticker(ticker_symbol)
            company_name = ticker.info.get('longName', ticker_symbol)

            # Get shares outstanding
            shares_outstanding = ticker.info.get('sharesOutstanding', 0)
            if shares_outstanding == 0:
                st.error(f"Could not fetch shares outstanding for {ticker_symbol}. Please check the ticker symbol.")
                st.stop()

            # Get total debt and cash
            total_debt = ticker.info.get('totalDebt', 0)
            total_cash = ticker.info.get('totalCash', 0)

            # Get LTM (Last Twelve Months) data
            ltm_data = ticker.quarterly_income_stmt.T.sort_index()

            if ltm_data.empty:
                st.error(f"Could not fetch quarterly data for {ticker_symbol}. Please check the ticker symbol.")
                st.stop()

            # Keep last 4 quarters
            ltm_data = ltm_data.iloc[-4:]
            ltm_revenue = ltm_data['Total Revenue'].sum()
            most_recent_date = ltm_data.index[-1]

        # Display company info
        st.header(f"{company_name} ({ticker_symbol})")

        # ====================
        # SECTION 1: LTM DATA
        # ====================
        st.subheader("1. Last Twelve Months (LTM) Starting Point")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("LTM Revenue ($M)", f"{ltm_revenue/scale_factor:,.2f}")
        with col2:
            st.metric("Shares Outstanding (M)", f"{shares_outstanding/scale_factor:,.2f}")
        with col3:
            st.metric("Most Recent Quarter", most_recent_date.strftime("%Y-%m-%d"))

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Debt ($M)", f"{total_debt/scale_factor:,.2f}")
        with col2:
            st.metric("Total Cash ($M)", f"{total_cash/scale_factor:,.2f}")

        # ====================
        # SECTION 2: PROJECTIONS
        # ====================
        st.subheader("2. Financial Projections")

        # Create projections dataframe
        # Generate future dates
        freq_dict = {1:'YE-JAN',2:'YE-FEB',3:'YE-MAR',4:'YE-APR', 5:'YE-MAY',6:'YE-JUN',
                     7:'YE-JUL',8:'YE-AUG', 9:'YE-SEP',10:'YE-OCT',11:'YE-NOV',12:'YE-DEC'}
        f = freq_dict[most_recent_date.month]
        new_dates = pd.date_range(start=most_recent_date, periods=time_horizon+1, freq=f)

        projections = pd.DataFrame(index=new_dates[1:])
        projections['Growth Rate'] = growth_pattern
        projections['EBIT Margin'] = ebit_margin
        projections['Reinvestment Rate'] = reinv_rate_pattern

        # Calculate projected financials
        projections['Revenue'] = ltm_revenue * (1 + projections['Growth Rate']).cumprod()
        projections['EBIT'] = projections['Revenue'] * projections['EBIT Margin']
        projections['NOPAT'] = projections['EBIT'] * (1 - eff_tax_rate)
        projections['FCF'] = projections['NOPAT'] * (1 - projections['Reinvestment Rate'])

        # Add year column for PV calculations
        projections = projections.reset_index(drop=True)
        projections['Year'] = projections.index + 1

        # Display projection patterns
        st.markdown("#### Projection Assumptions")
        ratios_df = pd.DataFrame({
            'Year': projections['Year'],
            'Growth Rate': projections['Growth Rate'],
            'EBIT Margin': projections['EBIT Margin'],
            'Reinvestment Rate': projections['Reinvestment Rate']
        })
        st.dataframe(ratios_df.style.format({
            'Year': '{:.0f}',
            'Growth Rate': '{:.2%}',
            'EBIT Margin': '{:.2%}',
            'Reinvestment Rate': '{:.2%}'
        }), use_container_width=True)

        # Display projected values
        st.markdown("#### Projected Financials ($M)")
        values_df = pd.DataFrame({
            'Year': projections['Year'],
            'Revenue': projections['Revenue'] / scale_factor,
            'EBIT': projections['EBIT'] / scale_factor,
            'NOPAT': projections['NOPAT'] / scale_factor,
            'FCF': projections['FCF'] / scale_factor
        })
        st.dataframe(values_df.style.format({
            'Year': '{:.0f}',
            'Revenue': '{:,.2f}',
            'EBIT': '{:,.2f}',
            'NOPAT': '{:,.2f}',
            'FCF': '{:,.2f}'
        }), use_container_width=True)

        # Visualization: Projected Revenue and FCF
        st.markdown("#### Projected Revenue & Free Cash Flow")
        fig, ax = plt.subplots(figsize=(12, 5))

        years = projections['Year']
        ax.plot(years, projections['Revenue'] / scale_factor, marker='o', linewidth=2, label='Revenue', color='#1f77b4')
        ax.plot(years, projections['FCF'] / scale_factor, marker='s', linewidth=2, label='Free Cash Flow', color='#2ca02c')

        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel(f'Amount (${scale_name})', fontsize=12)
        ax.set_title(f'{ticker_symbol} Projected Revenue & FCF', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

        # ====================
        # SECTION 3: VALUATION
        # ====================
        st.subheader("3. DCF Valuation")

        # Create WACC dataframe
        wacc_scenarios = {
            'Lower Bound': wacc_lower_input,
            'Mid Estimate': wacc_mid_input,
            'Upper Bound': wacc_upper_input
        }

        st.markdown("#### WACC Scenarios")
        wacc_df = pd.DataFrame({
            'Scenario': list(wacc_scenarios.keys()),
            'WACC': [f"{v:.2%}" for v in wacc_scenarios.values()]
        })
        st.dataframe(wacc_df, use_container_width=True, hide_index=True)

        # Calculate valuation for each WACC scenario
        results = []

        for scenario_name, wacc in wacc_scenarios.items():
            # Validate WACC > steady-state growth
            if wacc <= ss_growth:
                st.error(f"WACC ({wacc:.2%}) must be greater than steady-state growth rate ({ss_growth:.2%}) for the Gordon Growth Model.")
                st.stop()

            # Calculate PV of FCF
            projections[f'PV of FCF ({scenario_name})'] = projections['FCF'] / (1 + wacc) ** projections['Year']
            pv_fcf = projections[f'PV of FCF ({scenario_name})'].sum()

            # Calculate Terminal Value
            terminal_value = projections['FCF'].iloc[-1] * (1 + ss_growth) / (wacc - ss_growth)
            pv_terminal = terminal_value / ((1 + wacc) ** time_horizon)

            # Calculate Firm Value
            firm_value = pv_fcf + pv_terminal

            # Calculate Equity Value and Share Price
            equity_value = firm_value - total_debt + total_cash
            share_price = equity_value / shares_outstanding

            results.append({
                'Scenario': scenario_name,
                'WACC': wacc,
                'PV of FCF': pv_fcf,
                'Terminal Value': terminal_value,
                'PV of Terminal Value': pv_terminal,
                'Firm Value': firm_value,
                'Equity Value': equity_value,
                'Share Price': share_price
            })

        results_df = pd.DataFrame(results)

        # Display valuation summary
        st.markdown("#### Valuation Summary ($M, except per share)")
        display_results = pd.DataFrame({
            'Scenario': results_df['Scenario'],
            'WACC': results_df['WACC'] * 100,
            'PV of FCF': results_df['PV of FCF'] / scale_factor,
            'PV of Terminal Value': results_df['PV of Terminal Value'] / scale_factor,
            'Firm Value': results_df['Firm Value'] / scale_factor,
            'Equity Value': results_df['Equity Value'] / scale_factor,
            'Share Price': results_df['Share Price']
        })

        st.dataframe(display_results.style.format({
            'WACC': '{:.2f}%',
            'PV of FCF': '{:,.2f}',
            'PV of Terminal Value': '{:,.2f}',
            'Firm Value': '{:,.2f}',
            'Equity Value': '{:,.2f}',
            'Share Price': '${:.2f}'
        }), use_container_width=True, hide_index=True)

        # ====================
        # SECTION 4: SHARE PRICE COMPARISON
        # ====================
        st.subheader("4. Share Price Analysis")

        # Get current stock price
        try:
            hist = ticker.history(period="1d")
            current_price = hist['Close'].iloc[-1] if not hist.empty else None
        except:
            current_price = None

        # Display share price metrics
        st.markdown("### 🎯 DCF-Implied Share Price")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            lower_price = results_df[results_df['Scenario'] == 'Lower Bound']['Share Price'].iloc[0]
            st.metric("Lower Bound", f"${lower_price:.2f}")

        with col2:
            mid_price = results_df[results_df['Scenario'] == 'Mid Estimate']['Share Price'].iloc[0]
            st.metric("Mid Estimate", f"${mid_price:.2f}")

        with col3:
            upper_price = results_df[results_df['Scenario'] == 'Upper Bound']['Share Price'].iloc[0]
            st.metric("Upper Bound", f"${upper_price:.2f}")

        with col4:
            if current_price:
                st.metric("Current Price", f"${current_price:.2f}")
            else:
                st.metric("Current Price", "N/A")

        # Valuation conclusion
        if current_price:
            if current_price < lower_price:
                valuation_msg = f"📊 **Undervalued**: Current price (${current_price:.2f}) is below the DCF valuation range."
                valuation_color = "green"
            elif current_price > upper_price:
                valuation_msg = f"📊 **Overvalued**: Current price (${current_price:.2f}) is above the DCF valuation range."
                valuation_color = "red"
            else:
                valuation_msg = f"📊 **Fairly Valued**: Current price (${current_price:.2f}) is within the DCF valuation range."
                valuation_color = "blue"

            st.markdown(f":{valuation_color}[{valuation_msg}]")

        # ====================
        # SECTION 5: VISUALIZATION
        # ====================
        st.subheader("5. Historical Stock Price vs. DCF Estimates")

        # Download 1 year historical stock prices
        try:
            hist_1y = ticker.history(period="1y")

            if not hist_1y.empty:
                fig2, ax2 = plt.subplots(figsize=(14, 7))

                # Plot historical stock price
                ax2.plot(hist_1y.index, hist_1y['Close'], label='Historical Stock Price', linewidth=2, color='#1f77b4')

                # Plot DCF estimates as horizontal lines
                ax2.axhline(y=lower_price, color='r', linestyle='--', linewidth=2, label=f'Lower Estimate (${lower_price:.2f})')
                ax2.axhline(y=mid_price, color='g', linestyle='--', linewidth=2, label=f'Mid Estimate (${mid_price:.2f})')
                ax2.axhline(y=upper_price, color='b', linestyle='--', linewidth=2, label=f'Upper Estimate (${upper_price:.2f})')

                # Shade area between upper and lower
                ax2.fill_between(hist_1y.index, lower_price, upper_price, color='grey', alpha=0.2, label='Valuation Range')

                # Labels and title
                ax2.set_title(f"{company_name} Stock Price vs DCF Valuation Estimates", fontsize=16, fontweight='bold')
                ax2.set_xlabel('Date', fontsize=14)
                ax2.set_ylabel('Stock Price (USD)', fontsize=14)
                ax2.legend(loc='best', fontsize=11)
                ax2.grid(True, alpha=0.3)

                st.pyplot(fig2)
            else:
                st.warning("Could not fetch historical stock price data for visualization.")

        except Exception as e:
            st.warning(f"Could not create stock price visualization: {str(e)}")

        # ====================
        # SECTION 6: DETAILED BREAKDOWN
        # ====================
        with st.expander("📝 Valuation Calculation Details"):
            st.markdown(f"""
            ### Calculation Methodology

            **1. Free Cash Flow (FCF) Projections:**
            - Revenue(t) = Revenue(t-1) × (1 + Growth Rate)
            - EBIT(t) = Revenue(t) × EBIT Margin
            - NOPAT(t) = EBIT(t) × (1 - Tax Rate)
            - FCF(t) = NOPAT(t) × (1 - Reinvestment Rate)

            **2. Present Value of FCF:**
            - PV(FCF) = Σ [FCF(t) / (1 + WACC)^t] for t = 1 to {time_horizon}

            **3. Terminal Value (Gordon Growth Model):**
            - TV = FCF(Year {time_horizon}) × (1 + g) / (WACC - g)
            - Where g = {ss_growth:.2%} (steady-state growth)
            - PV(TV) = TV / (1 + WACC)^{time_horizon}

            **4. Firm Value:**
            - Firm Value = PV(FCF) + PV(TV)

            **5. Equity Value:**
            - Equity Value = Firm Value - Total Debt + Total Cash
            - = ${results_df.iloc[1]['Firm Value']/scale_factor:,.2f}M - ${total_debt/scale_factor:,.2f}M + ${total_cash/scale_factor:,.2f}M

            **6. Share Price:**
            - Share Price = Equity Value / Shares Outstanding
            - = ${results_df.iloc[1]['Equity Value']/scale_factor:,.2f}M / {shares_outstanding/scale_factor:,.2f}M
            - = ${results_df.iloc[1]['Share Price']:.2f}
            """)

        # ====================
        # DOWNLOAD SECTION
        # ====================
        st.subheader("📥 Download Results")

        # Prepare comprehensive export
        export_data = {
            'Company': company_name,
            'Ticker': ticker_symbol,
            'Valuation Date': datetime.now().strftime("%Y-%m-%d"),
            'LTM Revenue ($M)': ltm_revenue / scale_factor,
            'Shares Outstanding (M)': shares_outstanding / scale_factor,
            'Total Debt ($M)': total_debt / scale_factor,
            'Total Cash ($M)': total_cash / scale_factor,
            'Time Horizon (years)': time_horizon,
            'Effective Tax Rate': eff_tax_rate,
            'Steady-State Growth': ss_growth,
            'WACC Lower': wacc_lower_input,
            'WACC Mid': wacc_mid_input,
            'WACC Upper': wacc_upper_input,
            'Share Price (Lower)': lower_price,
            'Share Price (Mid)': mid_price,
            'Share Price (Upper)': upper_price,
            'Current Market Price': current_price if current_price else 'N/A'
        }

        export_df = pd.DataFrame([export_data])
        csv = export_df.to_csv(index=False)

        st.download_button(
            label="Download DCF Valuation Summary as CSV",
            data=csv,
            file_name=f"{ticker_symbol}_DCF_valuation_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

        # Also offer projections download
        projections_export = projections[['Year', 'Growth Rate', 'EBIT Margin', 'Reinvestment Rate',
                                          'Revenue', 'EBIT', 'NOPAT', 'FCF']].copy()
        projections_export['Revenue'] = projections_export['Revenue'] / scale_factor
        projections_export['EBIT'] = projections_export['EBIT'] / scale_factor
        projections_export['NOPAT'] = projections_export['NOPAT'] / scale_factor
        projections_export['FCF'] = projections_export['FCF'] / scale_factor

        projections_csv = projections_export.to_csv(index=False)

        st.download_button(
            label="Download Projected Financials as CSV",
            data=projections_csv,
            file_name=f"{ticker_symbol}_projections_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your inputs and try again. Ensure the ticker symbol is valid and all input patterns are correctly formatted.")
        import traceback
        st.code(traceback.format_exc())

else:
    st.info("👈 Enter parameters in the sidebar and click 'Build DCF Model' to begin")

    st.markdown("### How the DCF Model Works")
    st.markdown("""
    This DCF (Discounted Cash Flow) valuation module helps you determine the intrinsic value of a company
    based on its projected future cash flows.

    #### Step-by-Step Process:

    **1. LTM Starting Point**
    - Fetches the last 4 quarters of revenue data
    - Aggregates to get Last Twelve Months (LTM) revenue
    - This becomes the baseline for projections

    **2. Define Projection Assumptions**
    - **Revenue Growth Rates**: How fast will revenue grow each year?
    - **EBIT Margins**: What will operating profitability be?
    - **Reinvestment Rates**: How much capital needs to be reinvested?
    - **Time Horizon**: Typically 5-10 years
    - **Steady-State Growth**: Long-term perpetual growth rate

    **3. Project Future Cash Flows**
    - Calculate Revenue, EBIT, NOPAT, and Free Cash Flow for each year
    - Apply your assumptions to generate a complete financial forecast

    **4. Discount to Present Value**
    - Use WACC (from WACC Calculator) as the discount rate
    - Calculate present value of all future cash flows
    - Apply Gordon Growth Model for terminal value

    **5. Calculate Intrinsic Share Price**
    - Firm Value = PV of FCF + PV of Terminal Value
    - Equity Value = Firm Value - Debt + Cash
    - Share Price = Equity Value / Shares Outstanding

    **6. Compare to Market Price**
    - See if the stock is overvalued or undervalued
    - Visualize with historical price chart
    - Understand the range of possible values based on WACC uncertainty

    #### Tips for Best Results:

    - Start with **Historical Analysis** to understand past growth and margins
    - Use **WACC Calculator** to get appropriate discount rates
    - Be conservative with growth rates (high growth can't continue forever)
    - Ensure steady-state growth is reasonable (typically 2-4%)
    - Run sensitivity analysis with different WACC values
    """)

    st.markdown("### Example Projection Pattern")
    st.markdown("""
    For a mature tech company like Microsoft, you might use:

    | Parameter | Early Years | Mid Years | Late Years |
    |-----------|-------------|-----------|------------|
    | Revenue Growth | 15-20% | 10-12% | 6-8% |
    | EBIT Margin | 45-46% | 45-46% | 44-46% |
    | Reinvestment Rate | 30-40% | 20-25% | 15-20% |

    Adjust these based on:
    - Company's historical performance
    - Industry trends
    - Competitive position
    - Market maturity
    """)

# Navigation buttons at the bottom
st.divider()
st.markdown("### 🔄 Next Steps")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("← Back to Historical Analysis", use_container_width=True):
        st.switch_page("pages/2_Historical_Analysis.py")
with col2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")
with col3:
    if st.button("💼 Back to WACC Calculator", use_container_width=True):
        st.switch_page("pages/1_WACC_Calculator.py")
