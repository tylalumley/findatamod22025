# DCF Valuation Suite

A comprehensive web application for performing professional-grade Discounted Cash Flow (DCF) analysis on publicly traded companies.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Overview

The DCF Valuation Suite is a three-phase financial analysis tool built with Streamlit that guides you through the complete DCF valuation process:

1. **WACC Calculator** - Calculate the Weighted Average Cost of Capital
2. **Historical Analysis** - Analyze past financial performance
3. **DCF Valuation** - Project future cash flows and determine intrinsic share value

## ✨ Features

### Phase 1: WACC Calculator
- Beta regression with 5 years of monthly data
- CAPM-based cost of equity calculation
- Credit rating-based cost of debt
- 95% confidence intervals
- Interactive scatter plot visualization

### Phase 2: Historical Analysis
- Income statement analysis (Revenue, EBIT, margins)
- Balance sheet metrics (Net Working Capital)
- Cash flow analysis (CapEx, D&A)
- Growth rates and trend visualizations
- Reinvestment rate calculations

### Phase 3: DCF Valuation
- LTM (Last Twelve Months) revenue baseline
- Customizable projection assumptions
- Financial projections (Revenue → EBIT → NOPAT → FCF)
- Gordon Growth Model for terminal value
- Sensitivity analysis across WACC scenarios
- Stock price comparison visualization
- Valuation conclusion (over/under/fairly valued)

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/dcf-valuation-suite.git
cd dcf-valuation-suite
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

## 📊 How to Use

### Recommended Workflow

1. **WACC Calculator**
   - Enter ticker symbol (e.g., MSFT, AAPL, GOOGL)
   - Input risk-free rate and other parameters
   - Calculate WACC with confidence intervals
   - Note the WACC values for Phase 3

2. **Historical Analysis**
   - Use the same ticker symbol
   - Review historical financial metrics
   - Observe growth patterns and margins
   - Use insights to inform Phase 3 projections

3. **DCF Valuation**
   - Input projection assumptions (growth rates, margins, reinvestment)
   - Enter WACC values from Phase 1
   - Build DCF model
   - Compare intrinsic value to current market price

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[yfinance](https://github.com/ranaroussi/yfinance)** - Yahoo Finance data fetching
- **[statsmodels](https://www.statsmodels.org/)** - Statistical modeling (OLS regression)
- **[pandas](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[matplotlib](https://matplotlib.org/)** - Data visualization
- **[numpy](https://numpy.org/)** - Numerical computing

## 📁 Project Structure

```
dcf-valuation-suite/
├── app.py                          # Home page
├── pages/
│   ├── 1_WACC_Calculator.py       # Phase 1: WACC Calculator
│   ├── 2_Historical_Analysis.py   # Phase 2: Historical Analysis
│   └── 3_DCF_Valuation.py         # Phase 3: DCF Valuation
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── CLAUDE.md                       # Detailed documentation
└── .gitignore                      # Git ignore rules
```

## 📖 Documentation

See [CLAUDE.md](CLAUDE.md) for detailed documentation including:
- Feature descriptions
- Technical implementation details
- Development timeline
- Troubleshooting guide

## 🔍 Example Analysis

**Company:** Microsoft (MSFT)

**Phase 1 Results:**
- Beta: 0.88
- WACC: 9.25% (Range: 7.96% - 10.54%)

**Phase 2 Insights:**
- Avg Revenue Growth: 12-15%
- Avg EBIT Margin: 42-46%
- Avg Reinvestment Rate: 25-30%

**Phase 3 Valuation:**
- DCF-Implied Value Range: $380 - $450
- Current Market Price: $420
- Conclusion: Fairly valued ✅

## ⚠️ Disclaimer

This tool is for educational and research purposes only. The valuations and analyses provided should not be considered as investment advice. Always consult with a qualified financial advisor before making investment decisions.

The data is sourced from Yahoo Finance and may not be completely accurate or up-to-date. Use at your own risk.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💼 Author

Developed as part of an MSF (Master of Science in Finance) program.

## 🙏 Acknowledgments

- Credit spread data based on Aswath Damodaran's research
- Built with the Streamlit framework
- Financial data provided by Yahoo Finance

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Last Updated:** December 2025
**Version:** 3.0 - Complete DCF Valuation Suite
