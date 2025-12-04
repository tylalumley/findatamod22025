import streamlit as st

# Page configuration
st.set_page_config(
    page_title="DCF Valuation Suite",
    layout="wide",
    page_icon="📈"
)

# Main title
st.title("📈 DCF Valuation Suite")
st.markdown("### A Comprehensive Tool for Discounted Cash Flow Analysis")

# Introduction
st.markdown("""
Welcome to the **DCF Valuation Suite** - your complete toolkit for performing professional-grade
discounted cash flow analysis on publicly traded companies.

This application guides you through the entire DCF valuation process, from calculating the cost of capital
to projecting future cash flows and determining intrinsic share value.
""")

st.divider()

# Three-column layout for the three modules
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💼 WACC Calculator")
    st.markdown("""
    **Phase 1: Cost of Capital**

    Calculate the Weighted Average Cost of Capital (WACC) using:
    - Beta regression with 5 years of monthly data
    - CAPM for cost of equity
    - Credit rating-based cost of debt
    - Statistical confidence intervals

    *Status: ✅ Complete*
    """)

with col2:
    st.markdown("### 📊 Historical Analysis")
    st.markdown("""
    **Phase 2: Understanding the Past**

    Analyze historical financial performance:
    - Income statement trends
    - Balance sheet metrics
    - Cash flow analysis
    - Growth rates and margins
    - Reinvestment patterns

    *Status: ✅ Complete*
    """)

with col3:
    st.markdown("### 🎯 DCF Valuation")
    st.markdown("""
    **Phase 3: Valuation Model**

    Project future cash flows and value:
    - Custom projection assumptions
    - Free cash flow forecasting
    - Terminal value calculation
    - Intrinsic share price
    - Sensitivity analysis

    *Status: ✅ Complete*
    """)

st.divider()

# How to use section
st.markdown("## 🚀 How to Use This Tool")

st.markdown("""
### Recommended Workflow:

1. **Start with WACC Calculator** (Page 1)
   - Input your target company's ticker symbol
   - Calculate the discount rate you'll need for valuation
   - Note the WACC values for use in the DCF model

2. **Analyze Historical Performance** (Page 2)
   - Review past financial statements
   - Understand growth patterns and margins
   - Identify trends to inform your projections

3. **Build DCF Model** (Page 3)
   - Project future revenues and cash flows
   - Apply your calculated WACC as the discount rate
   - Determine if the stock is over/undervalued

Each module can also be used independently for specific analyses.
""")

st.divider()

# Key features
st.markdown("## ✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Technical Capabilities
    - Real-time data from Yahoo Finance
    - Statistical regression analysis
    - 95% confidence intervals
    - Interactive visualizations
    - CSV export functionality
    """)

with col2:
    st.markdown("""
    ### User-Friendly Design
    - Intuitive sidebar controls
    - Progressive disclosure of results
    - Clear formula breakdowns
    - Professional formatting
    - Responsive layout
    """)

st.divider()

# Footer
st.markdown("## 📚 About This Project")
st.markdown("""
This tool was developed as part of an MSF (Master of Science in Finance) program, converting
three Python notebooks into an integrated web application. The methodology follows academic
best practices for corporate valuation.

**Data Source:** Yahoo Finance
**Framework:** Streamlit
**Statistical Methods:** OLS Regression, CAPM, Gordon Growth Model
""")

st.info("👈 Use the sidebar to navigate between different modules")
