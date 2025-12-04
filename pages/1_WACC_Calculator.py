import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import yfinance as yf

# Page configuration
st.set_page_config(page_title="WACC Calculator", layout="wide")

# Title
st.title("📊 WACC Calculator")
st.markdown("Calculate the Weighted Average Cost of Capital for any publicly traded company")

# Quick navigation at top
col1, col2, col3 = st.columns([3, 1, 1])
with col2:
    if st.button("📊 Historical Analysis →", use_container_width=True):
        st.switch_page("pages/2_Historical_Analysis.py")
with col3:
    if st.button("🎯 DCF Valuation →", use_container_width=True):
        st.switch_page("pages/3_DCF_Valuation.py")

st.divider()

# Sidebar for inputs
st.sidebar.header("Input Parameters")

# Ticker input
ticker_symbol = st.sidebar.text_input("Ticker Symbol", value="MSFT").upper()

# Risk-free rate input
rf = st.sidebar.number_input("Risk-Free Rate (%)", min_value=0.0, max_value=20.0, value=4.5, step=0.1) / 100

# EMRP input
emrp = st.sidebar.number_input("Equity Market Risk Premium (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1) / 100

# Credit rating input
firm_rating = st.sidebar.text_input("Credit Rating (e.g., Aaa/AAA, A2/A)", value="Aaa/AAA")

# Marginal tax rate input
marg_tax_rate = st.sidebar.number_input("Marginal Tax Rate (%)", min_value=0.0, max_value=100.0, value=25.0, step=1.0) / 100

# Market index selection
index_symbol = st.sidebar.selectbox("Market Index for Beta", options=["^GSPC", "^DJI", "^IXIC"], index=0)
index_names = {"^GSPC": "S&P 500", "^DJI": "Dow Jones", "^IXIC": "NASDAQ"}

# Credit spreads lookup table
credit_spreads = [
    {"GreaterThan": -100000, "LessThan": 0.199999, "Rating": "D2/D", "Spread": 19.00},
    {"GreaterThan": 0.2, "LessThan": 0.649999, "Rating": "C2/C", "Spread": 15.50},
    {"GreaterThan": 0.65, "LessThan": 0.799999, "Rating": "Ca2/CC", "Spread": 10.10},
    {"GreaterThan": 0.8, "LessThan": 1.249999, "Rating": "Caa/CCC", "Spread": 7.28},
    {"GreaterThan": 1.25, "LessThan": 1.499999, "Rating": "B3/B-", "Spread": 4.42},
    {"GreaterThan": 1.5, "LessThan": 1.749999, "Rating": "B2/B", "Spread": 3.00},
    {"GreaterThan": 1.75, "LessThan": 1.999999, "Rating": "B1/B+", "Spread": 2.61},
    {"GreaterThan": 2.0, "LessThan": 2.2499999, "Rating": "Ba2/BB", "Spread": 1.83},
    {"GreaterThan": 2.25, "LessThan": 2.49999, "Rating": "Ba1/BB+", "Spread": 1.55},
    {"GreaterThan": 2.5, "LessThan": 2.999999, "Rating": "Baa2/BBB", "Spread": 1.20},
    {"GreaterThan": 3.0, "LessThan": 4.249999, "Rating": "A3/A-", "Spread": 0.95},
    {"GreaterThan": 4.25, "LessThan": 5.499999, "Rating": "A2/A", "Spread": 0.85},
    {"GreaterThan": 5.5, "LessThan": 6.499999, "Rating": "A1/A+", "Spread": 0.77},
    {"GreaterThan": 6.5, "LessThan": 8.499999, "Rating": "Aa2/AA", "Spread": 0.60},
    {"GreaterThan": 8.5, "LessThan": 100000, "Rating": "Aaa/AAA", "Spread": 0.45}
]

# Function to get credit spread
def get_credit_spread(rating, credit_spreads):
    """Returns the credit spread for a given credit rating."""
    for entry in credit_spreads:
        if entry["Rating"].strip().lower() == rating.strip().lower():
            return float(entry["Spread"]) / 100
    st.warning(f"Warning: No spread found for rating '{rating}'. Using 0%.")
    return 0.0

# Calculate button
if st.sidebar.button("Calculate WACC", type="primary"):
    try:
        with st.spinner(f"Fetching data for {ticker_symbol}..."):
            # Create ticker object
            ticker = yf.Ticker(ticker_symbol)

            # Get market cap and total debt
            scale_factor = 1000000
            market_cap = ticker.info.get('marketCap', 0) / scale_factor
            total_debt = ticker.info.get('totalDebt', 0) / scale_factor
            company_name = ticker.info.get('longName', ticker_symbol)

            if market_cap == 0:
                st.error(f"Could not fetch data for ticker {ticker_symbol}. Please check the ticker symbol.")
                st.stop()

            # Calculate weights
            w_E = market_cap / (market_cap + total_debt)
            w_D = total_debt / (market_cap + total_debt)

            # Display company info
            st.header(f"{company_name} ({ticker_symbol})")

            # Section 1: Capital Structure
            st.subheader("1. Capital Structure")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Market Cap ($M)", f"{market_cap:,.2f}")
            with col2:
                st.metric("Total Debt ($M)", f"{total_debt:,.2f}")
            with col3:
                st.metric("Total Value ($M)", f"{market_cap + total_debt:,.2f}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Equity Weight", f"{w_E:.2%}")
            with col2:
                st.metric("Debt Weight", f"{w_D:.2%}")

            # Section 2: Cost of Equity
            st.subheader("2. Cost of Equity (CAPM)")

            with st.spinner("Calculating Beta..."):
                # Download historical data
                stock_data = yf.download(ticker_symbol, period='5y', interval='1mo', progress=False)["Close"]
                index_data = yf.download(index_symbol, period='5y', interval='1mo', progress=False)["Close"]

                # Calculate returns
                stock_returns = stock_data.pct_change().dropna() - rf
                index_returns = index_data.pct_change().dropna() - rf

                # Run regression
                X = sm.add_constant(index_returns)
                model = sm.OLS(stock_returns, X)
                results = model.fit()

                # Get beta and confidence intervals
                beta = results.params[index_symbol]
                beta_lower = results.conf_int().loc[index_symbol, 0]
                beta_upper = results.conf_int().loc[index_symbol, 1]

                # Calculate cost of equity
                cost_of_equity = rf + beta * emrp
                cost_of_equity_lower = rf + beta_lower * emrp
                cost_of_equity_upper = rf + beta_upper * emrp

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Beta", f"{beta:.2f}")
            with col2:
                st.metric("Risk-Free Rate", f"{rf:.2%}")
            with col3:
                st.metric("EMRP", f"{emrp:.2%}")

            st.metric("Cost of Equity", f"{cost_of_equity:.2%}", help=f"95% CI: [{cost_of_equity_lower:.2%}, {cost_of_equity_upper:.2%}]")

            # Beta regression plot with monthly returns and best fit line
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(index_returns, stock_returns, alpha=0.6, s=50, edgecolors='black', linewidths=0.5)

            # Plot best fit line
            x_line = np.linspace(index_returns.min(), index_returns.max(), 100)
            y_line = results.params['const'] + results.params[index_symbol] * x_line
            ax.plot(x_line, y_line, color='red', linewidth=2, label=f'Best Fit Line (β = {beta:.2f})')

            ax.set_xlabel(f'{index_names[index_symbol]} Monthly Excess Returns', fontsize=12)
            ax.set_ylabel(f'{ticker_symbol} Monthly Excess Returns', fontsize=12)
            ax.set_title(f'Beta Regression: {ticker_symbol} vs {index_names[index_symbol]} (5 Years Monthly Data)', fontsize=14, fontweight='bold')
            ax.legend(fontsize=11)
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
            ax.axvline(x=0, color='black', linestyle='--', linewidth=0.5)

            # Add R-squared to plot
            r_squared = results.rsquared
            ax.text(0.05, 0.95, f'R² = {r_squared:.3f}', transform=ax.transAxes,
                   fontsize=11, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

            st.pyplot(fig)

            # Section 3: Cost of Debt
            st.subheader("3. Cost of Debt")

            credit_spread = get_credit_spread(firm_rating, credit_spreads)
            cost_of_debt = rf + credit_spread

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Credit Rating", firm_rating)
            with col2:
                st.metric("Credit Spread", f"{credit_spread:.2%}")
            with col3:
                st.metric("Cost of Debt", f"{cost_of_debt:.2%}")

            # Section 4: WACC
            st.subheader("4. Weighted Average Cost of Capital (WACC)")

            wacc = (w_E * cost_of_equity) + (w_D * cost_of_debt * (1 - marg_tax_rate))
            wacc_lower = (w_E * cost_of_equity_lower) + (w_D * cost_of_debt * (1 - marg_tax_rate))
            wacc_upper = (w_E * cost_of_equity_upper) + (w_D * cost_of_debt * (1 - marg_tax_rate))

            # Display WACC prominently
            st.markdown("### 🎯 Final WACC")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Lower CI (95%)", f"{wacc_lower:.2%}")
            with col2:
                st.metric("WACC Estimate", f"{wacc:.2%}", help="Weighted Average Cost of Capital")
            with col3:
                st.metric("Upper CI (95%)", f"{wacc_upper:.2%}")

            # WACC formula breakdown
            with st.expander("📝 WACC Calculation Breakdown"):
                st.latex(r"WACC = w_E \times k_E + w_D \times k_D \times (1-t)")
                st.write(f"WACC = {w_E:.4f} × {cost_of_equity:.4f} + {w_D:.4f} × {cost_of_debt:.4f} × (1 - {marg_tax_rate:.4f})")
                st.write(f"WACC = {w_E * cost_of_equity:.4f} + {w_D * cost_of_debt * (1 - marg_tax_rate):.4f}")
                st.write(f"WACC = {wacc:.4f} or {wacc:.2%}")

            # Summary table
            st.subheader("📊 Summary Table")
            summary_df = pd.DataFrame({
                "Metric": ["Lower CI", "Estimate", "Upper CI"],
                "WACC": [f"{wacc_lower:.2%}", f"{wacc:.2%}", f"{wacc_upper:.2%}"]
            })
            st.dataframe(summary_df, hide_index=True, use_container_width=True)

            # Download results
            results_df = pd.DataFrame({
                "Parameter": ["Market Cap ($M)", "Total Debt ($M)", "Equity Weight", "Debt Weight",
                             "Beta", "Beta Lower CI", "Beta Upper CI", "R-Squared",
                             "Risk-Free Rate", "EMRP", "Cost of Equity",
                             "Credit Rating", "Credit Spread", "Cost of Debt", "Tax Rate",
                             "WACC", "WACC Lower CI", "WACC Upper CI"],
                "Value": [f"{market_cap:,.2f}", f"{total_debt:,.2f}", f"{w_E:.4f}", f"{w_D:.4f}",
                         f"{beta:.4f}", f"{beta_lower:.4f}", f"{beta_upper:.4f}", f"{r_squared:.4f}",
                         f"{rf:.4f}", f"{emrp:.4f}", f"{cost_of_equity:.4f}",
                         firm_rating, f"{credit_spread:.4f}", f"{cost_of_debt:.4f}", f"{marg_tax_rate:.4f}",
                         f"{wacc:.4f}", f"{wacc_lower:.4f}", f"{wacc_upper:.4f}"]
            })

            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name=f"{ticker_symbol}_WACC_results.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your inputs and try again.")

else:
    st.info("👈 Enter parameters in the sidebar and click 'Calculate WACC' to begin")

    # Show example
    st.markdown("### Example Usage")
    st.markdown("""
    1. Enter a ticker symbol (e.g., MSFT, AAPL, GOOGL)
    2. Input the current risk-free rate (e.g., 4.5%)
    3. Adjust other parameters if needed
    4. Click 'Calculate WACC'

    The calculator will:
    - Fetch company financial data
    - Calculate Beta using 5 years of monthly data
    - Determine cost of equity using CAPM
    - Look up credit spread based on rating
    - Compute the final WACC with confidence intervals
    """)

# Navigation buttons at the bottom
st.divider()
st.markdown("### 🔄 Next Steps")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("📊 Go to Historical Analysis →", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Historical_Analysis.py")
