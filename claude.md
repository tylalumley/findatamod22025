# DCF Valuation Suite - Multi-Page Streamlit Web Application

## Project Overview

This project converts three Python DCF (Discounted Cash Flow) analysis notebooks into a comprehensive Streamlit web application. The application now features a multi-page architecture with three main modules: WACC Calculator, Historical Analysis, and DCF Valuation.

## Current Status

### Completed Features

**Phase 1: WACC Calculator** ✅
- ✅ Complete WACC calculator with sidebar inputs
- ✅ Beta regression with 5 years of monthly data
- ✅ Visual scatter plot showing monthly returns with best fit line
- ✅ Cost of equity calculation using CAPM
- ✅ Cost of debt calculation using credit rating lookup
- ✅ Final WACC calculation with confidence intervals
- ✅ CSV download functionality

**Phase 2: Historical Analysis** ✅
- ✅ Income statement data display with growth rates
- ✅ Balance sheet data with NWC calculations
- ✅ Statement of cash flows (CapEx, D&A)
- ✅ Growth rates visualization (Revenue, EBIT)
- ✅ Margin trends over time (Gross, EBIT, EBITDA)
- ✅ Reinvestment metrics and NOPAT calculations
- ✅ Reinvestment rate trend visualization
- ✅ Summary statistics table
- ✅ CSV download functionality

**Phase 3: DCF Valuation** 🔜
- 🔜 Placeholder page with detailed feature preview
- 🔜 Coming soon (full implementation pending)

**Application Architecture** ✅
- ✅ Multi-page Streamlit app with automatic navigation
- ✅ Home page with project overview
- ✅ Three separate page modules
- ✅ Consistent styling and branding

## Project Structure

```
website/
├── app.py                          # Home page (main entry point)
├── pages/
│   ├── 1_WACC_Calculator.py       # Phase 1: WACC Calculator
│   ├── 2_Historical_Analysis.py   # Phase 2: Historical Analysis
│   └── 3_DCF_Valuation.py         # Phase 3: DCF Valuation (placeholder)
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── claude.md                       # This documentation file
├── app_old_backup.py              # Original single-page WACC app (backup)
├── copy_of_dcf1_wacc_tyla_lumley.py          # Original WACC notebook
├── copy_of_dcf2_historical_analysis_tyla_lumley.py  # Historical analysis notebook
└── copy_of_dcf3_dcf_model_tyla_lumley.py     # DCF model notebook
```

## Files Created

### 1. `app.py` (Home Page)
Welcome page and navigation hub for the DCF Valuation Suite:
- Project overview and introduction
- Three-column layout showcasing each module
- Recommended workflow guidance
- Key features summary
- About section with methodology details

### 2. `pages/1_WACC_Calculator.py`
Complete WACC calculator module that implements:
- Sidebar inputs for all parameters
- Company data fetching from Yahoo Finance
- Beta calculation via OLS regression (5 years monthly data)
- Credit spread lookup table (15-tier ratings)
- Interactive scatter plot with best fit line
- Cost of equity via CAPM
- Cost of debt calculation
- Final WACC with 95% confidence intervals
- Formula breakdown
- CSV download

### 3. `pages/2_Historical_Analysis.py`
Comprehensive historical financial analysis module:
- Income statement analysis (Revenue, EBIT, Gross Profit)
- Growth rate calculations (Revenue Growth, EBIT Growth)
- Margin analysis (Gross, EBIT, EBITDA margins)
- Interactive trend visualizations (Revenue/EBIT over time, Margin trends)
- Balance sheet analysis (NWC, Change in NWC)
- Cash flow statement data (CapEx, D&A)
- Reinvestment calculations (Reinvestment = CapEx - D&A + ΔnWC)
- NOPAT calculations
- Reinvestment rate analysis
- Summary statistics table
- Key insights metrics
- CSV download

### 4. `pages/3_DCF_Valuation.py`
Placeholder page for Phase 3 implementation:
- Detailed feature preview
- Methodology explanation
- Example projection patterns
- Technical details (Gordon Growth Model, PV calculations)
- Coming soon notification

### 5. `requirements.txt`
Python package dependencies:
```
streamlit
numpy
pandas
matplotlib
statsmodels
yfinance
```

### 6. `.streamlit/config.toml`
Configuration file for headless mode:
```toml
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

## Key Design Decisions

1. **Removed FRED API Integration**: User manually inputs risk-free rate instead of fetching from FRED API
2. **Credit Rating Input**: User provides credit rating as text input
3. **Market Index Selection**: Dropdown to choose between S&P 500, Dow Jones, or NASDAQ for Beta calculation
4. **5 Years Monthly Data**: Uses 5 years of monthly returns for Beta regression (same as original notebook)
5. **Minimal UI First**: Started with just WACC calculator before adding other features

## Module-Specific Features

### Page 1: WACC Calculator

**Sidebar Inputs:**
- **Ticker Symbol**: Stock ticker (e.g., MSFT, AAPL, GOOGL)
- **Risk-Free Rate (%)**: User-provided current risk-free rate
- **Equity Market Risk Premium (%)**: Default 5.0%, adjustable
- **Credit Rating**: Firm's credit rating (e.g., Aaa/AAA, A2/A)
- **Marginal Tax Rate (%)**: Default 25%, adjustable
- **Market Index**: Choose index for Beta calculation (S&P 500, Dow Jones, NASDAQ)

**Output Sections:**
1. **Capital Structure**: Market cap, total debt, equity/debt weights
2. **Cost of Equity (CAPM)**: Beta, risk-free rate, EMRP, cost of equity with CIs, scatter plot with regression line
3. **Cost of Debt**: Credit rating, credit spread, final cost of debt
4. **WACC**: Final WACC with 95% confidence intervals, formula breakdown, summary table
5. **Download**: CSV export of all results

### Page 2: Historical Analysis

**Sidebar Inputs:**
- **Ticker Symbol**: Stock ticker (e.g., MSFT, AAPL, GOOGL)
- **Effective Tax Rate (%)**: Default 19%, adjustable
- **Marginal Tax Rate (%)**: Default 25%, adjustable

**Output Sections:**
1. **Income Statement Analysis**: Revenue, EBIT, Gross Profit tables; Growth rates and margins table; Revenue/EBIT trend chart; Margin trend chart
2. **Balance Sheet Analysis**: Current assets, liabilities, NWC, Change in NWC table
3. **Cash Flow Statement**: CapEx, D&A table
4. **Reinvestment Analysis**: NOPAT, Reinvestment, Reinvestment Rate table; Reinvestment rate trend chart
5. **Summary Statistics**: Complete historical summary with all key metrics
6. **Key Insights**: Average metrics displayed as metric cards
7. **Download**: CSV export of historical analysis

### Page 3: DCF Valuation (Coming Soon)

**Planned Inputs:**
- Ticker symbol
- Revenue growth rate pattern (list)
- EBIT margin pattern (list)
- Reinvestment rate pattern (list)
- Steady-state growth rate
- Effective tax rate
- WACC (imported from Page 1 or manual input)

**Planned Outputs:**
- LTM revenue starting point
- Projected financials table (Revenue → EBIT → NOPAT → FCF)
- Present value calculations
- Terminal value
- Intrinsic share price (upper, middle, lower estimates)
- Historical stock price vs. DCF estimates chart
- Valuation range visualization

## How to Run

### First Time Setup:
```bash
cd "/Users/tylalumley/Documents/MSF/module 2/fin data analytics/website"
pip3 install -r requirements.txt
```

### Running the Application:
```bash
python3 -m streamlit run app.py --server.headless true
```

### Access the App:
Open browser to: **http://localhost:8501**

### Stopping the App:
Press `Ctrl+C` in the terminal

## Future Enhancements

### Phase 3: DCF Valuation Implementation (Next Priority)
- [ ] LTM data fetching and aggregation
- [ ] Input fields for year-by-year projection assumptions
- [ ] Automated financial projections (Revenue → FCF)
- [ ] WACC import from Phase 1 (or manual override)
- [ ] Present value calculations for FCF
- [ ] Terminal value using Gordon Growth Model
- [ ] Intrinsic share price calculation
- [ ] Sensitivity analysis across WACC range
- [ ] Historical stock price vs. DCF estimates visualization
- [ ] Valuation range chart with shaded confidence area
- [ ] CSV download for projections and valuation results

### Phase 4: Advanced Features (Future)
- [ ] Preset company examples with pre-filled assumptions
- [ ] Tooltips and help text for financial terms
- [ ] Data caching with `@st.cache_data` for performance
- [ ] Session state to persist data across pages
- [ ] Comparison mode (compare multiple companies side-by-side)
- [ ] Save/load analysis functionality
- [ ] PDF report generation
- [ ] More advanced visualizations (interactive charts)
- [ ] Historical vs. projected comparison charts
- [ ] Monte Carlo simulation for uncertainty analysis

## Technical Notes

### Dependencies:
- **Streamlit**: Web framework
- **yfinance**: Yahoo Finance data fetching
- **statsmodels**: OLS regression for Beta
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **matplotlib**: Plotting

### Data Sources:
- **Company Data**: Yahoo Finance API via yfinance
- **Market Data**: Yahoo Finance historical prices
- **Credit Spreads**: Hardcoded lookup table from Aswath Damodaran's data

### Known Limitations:
- Requires internet connection for Yahoo Finance data
- Historical data limited to what yfinance provides
- Credit spread table needs manual updates

## Testing Checklist

When testing the app:
- ✅ App loads successfully
- ✅ Default values (MSFT) work correctly
- ✅ Can change ticker symbol
- ✅ Risk-free rate input works
- ✅ Beta regression calculates correctly
- ✅ Scatter plot displays with best fit line
- ✅ WACC calculates with confidence intervals
- ✅ CSV download works
- ✅ Invalid ticker shows error message
- ✅ All metrics display with proper formatting

## Development Timeline

**Session 1** (December 2, 2025):
1. Analyzed three Python DCF notebooks
2. Created development plan
3. Built minimal WACC calculator (Phase 1)
4. Added monthly returns plot with best fit line
5. Created requirements.txt
6. Configured Streamlit for headless mode
7. Successfully deployed to localhost

**Session 2** (December 4, 2025):
1. Analyzed dcf2 and dcf3 notebooks for Phase 2 & 3 requirements
2. Designed multi-page app architecture using Streamlit pages/ directory
3. Created new home page (app.py) with project overview
4. Moved WACC calculator to pages/1_WACC_Calculator.py
5. Built comprehensive Historical Analysis page (pages/2_Historical_Analysis.py):
   - Income statement analysis with growth rates and margins
   - Balance sheet analysis with NWC calculations
   - Cash flow statement data
   - Reinvestment and NOPAT analysis
   - Multiple visualizations (trends, margins, reinvestment rate)
   - Summary statistics and key insights
6. Created placeholder DCF Valuation page (pages/3_DCF_Valuation.py)
7. Tested multi-page navigation
8. Updated documentation to reflect new structure

## Next Steps

1. **Implement Phase 3: DCF Valuation**
   - Build LTM data fetching
   - Create projection input interface
   - Implement valuation calculations
   - Add visualization comparing DCF estimates to actual stock price
   - Test with multiple companies

2. **Enhancement & Polish**
   - Add data caching for performance
   - Implement session state to share data between pages
   - Add tooltips and help documentation
   - Create preset company examples
   - Improve error handling and validation

3. **User Testing & Feedback**
   - Test with variety of tickers across different sectors
   - Gather feedback on UX and workflow
   - Identify edge cases and bugs

## Troubleshooting

### App won't start:
- Check if port 8501 is available
- Verify all dependencies are installed
- Try running with `--server.headless true` flag

### Data fetch errors:
- Verify internet connection
- Check if ticker symbol is valid
- Yahoo Finance may have rate limits

### Import errors:
- Reinstall requirements: `pip3 install -r requirements.txt`
- Check Python version (requires Python 3.7+)

---

**Last Updated**: December 4, 2025
**Version**: 2.0 - Multi-Page Application with WACC Calculator, Historical Analysis, and DCF Placeholder

**Status:**
- ✅ Phase 1 (WACC Calculator): Complete
- ✅ Phase 2 (Historical Analysis): Complete
- 🔜 Phase 3 (DCF Valuation): In Planning
