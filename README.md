# Interactive Stock Market Analysis Tool

## Overview

This is an interactive web application built with **Streamlit** for analyzing and comparing the stock performance of major technology companies. The tool provides real-time data visualization, technical indicators, and comparative metrics to support investment analysis and financial decision-making.

**Target Audience:** Investors, financial analysts, and economics students interested in understanding stock market trends and technical analysis.

## Features

- **Multi-Company Analysis**: Compare up to 8 major tech companies (Apple, Microsoft, Tesla, NVIDIA, Amazon, Google, Meta, Intel)
- **Flexible Time Periods**: Analyze stock performance over 1 month, 3 months, 6 months, 1 year, or 2 years
- **Technical Indicators**: 
  - 20-day and 50-day Moving Averages (MA20, MA50)
  - Trading Volume Analysis
  - Price Trend Visualization
- **Performance Metrics**:
  - Current price and price change percentage
  - 52-week highs and lows
  - Average trading volume
  - Daily returns and volatility
  - Normalized price comparison (base = 100)
- **Interactive Visualizations**: Built with Plotly for dynamic, responsive charts
- **Data Export**: Download analyzed data as CSV for further analysis
- **Real-Time Data**: Powered by Yahoo Finance API

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository** (or download the files):
```bash
git clone https://github.com/yourusername/stock-analysis-tool.git
cd stock-analysis-tool
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### How to Use

1. **Select Companies**: Use the multiselect box in the left sidebar to choose which companies to analyze (default: Apple, Microsoft, Tesla)
2. **Choose Time Period**: Select your desired analysis period from the dropdown menu
3. **Configure Indicators**: Toggle technical indicators (Moving Averages, Trading Volume) on/off as needed
4. **Analyze Results**: 
   - View key metrics (current price, 52-week highs/lows) in the metrics section
   - Study price trends with moving averages
   - Compare normalized performance across companies
   - Examine trading volume patterns
   - Review statistical summaries
5. **Export Data**: Click the "Download Data as CSV" button to export the analyzed data

## Project Structure

```
stock-analysis-tool/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── stock_analysis.ipynb  # Jupyter notebook with analytical workflow
```

## Technical Implementation

### Data Processing Workflow

1. **Data Acquisition**: Fetch historical stock data from Yahoo Finance using `yfinance` library
2. **Data Cleaning**: Handle missing values and ensure data consistency
3. **Feature Engineering**: Calculate moving averages and technical indicators
4. **Analysis**: Compute statistical metrics (mean, standard deviation, returns, volatility)
5. **Visualization**: Create interactive charts using Plotly
6. **Export**: Prepare data for CSV export

### Key Libraries

| Library | Purpose |
|---------|---------|
| **Streamlit** | Web application framework and UI components |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computing and array operations |
| **yfinance** | Yahoo Finance data retrieval |
| **Plotly** | Interactive data visualization |

### Performance Considerations

- **Caching**: Stock data is cached using `@st.cache_data` to improve performance and reduce API calls
- **Lazy Loading**: Data is only fetched when companies are selected
- **Efficient Calculations**: NumPy and Pandas operations are vectorized for speed

## Data Source

- **Provider**: Yahoo Finance
- **Data Type**: Historical stock prices (Open, High, Low, Close, Volume)
- **Update Frequency**: Real-time (updated daily during market hours)
- **Reliability**: Yahoo Finance is a trusted source for educational and research purposes

### Data Limitations

- Historical data extends back approximately 20+ years for major companies
- Weekend and holiday data points are excluded (market closed)
- Data accuracy is subject to Yahoo Finance's data quality standards
- Real-time data may have slight delays (typically 15-20 minutes)

## Analysis Methods

### Technical Indicators

**Moving Averages (MA)**
- **20-day MA**: Short-term trend indicator, responsive to recent price changes
- **50-day MA**: Medium-term trend indicator, smooths out short-term volatility
- **Interpretation**: Prices above MA indicate uptrend; below MA indicate downtrend

### Statistical Metrics

- **Daily Return**: Percentage change from start to end of period
- **Volatility**: Standard deviation of returns, measures price fluctuation risk
- **Normalized Performance**: All prices indexed to 100 at the start date for fair comparison

### Comparative Analysis

- **Volume Analysis**: Identifies trading activity patterns and market interest
- **Normalized Comparison**: Eliminates price differences, focuses on percentage performance
- **Statistical Summary**: Provides standardized metrics for cross-company comparison

## Limitations and Future Improvements

### Current Limitations

1. **Limited Company Coverage**: Currently includes only 8 major tech companies; could be expanded to all S&P 500 stocks
2. **No Advanced Models**: Does not include predictive models or machine learning-based forecasting
3. **No Fundamental Analysis**: Focuses on technical analysis; does not incorporate P/E ratios, earnings, or other fundamental metrics
4. **Single Asset Class**: Limited to stock prices; does not include bonds, commodities, or cryptocurrencies
5. **No Portfolio Optimization**: Does not calculate optimal portfolio allocations or risk metrics

### Possible Improvements

- Add more companies and allow custom ticker input
- Implement advanced technical indicators (RSI, MACD, Bollinger Bands)
- Include fundamental analysis metrics (P/E ratio, dividend yield, earnings)
- Add predictive models (ARIMA, Prophet) for price forecasting
- Implement portfolio analysis with risk metrics (Sharpe ratio, correlation matrix)
- Add news sentiment analysis integration
- Support for multiple asset classes (crypto, commodities, bonds)
- Real-time alerts for price movements or technical signals

## Academic Integrity and AI Disclosure

This project was developed as part of ACC102 coursework at Xi'an Jiaotong-Liverpool University.

### AI Tools Used

| Tool | Model | Purpose | Date Accessed |
|------|-------|---------|---------------|
| ChatGPT | GPT-4 | Code structure and Streamlit best practices | April 2026 |
| GitHub Copilot | Codex | Function documentation and minor code suggestions | April 2026 |

### Student Contribution

- **Problem Definition**: Identified the need for an interactive tool to compare tech stock performance
- **Data Source Selection**: Chose Yahoo Finance for reliability and ease of access
- **Architecture Design**: Designed the modular structure with separate data fetching, processing, and visualization functions
- **Implementation**: Wrote all core application code, including UI logic, data processing, and visualization
- **Testing**: Manually tested all features and verified data accuracy
- **Documentation**: Wrote comprehensive README and reflection report

The use of AI tools was limited to code structure suggestions and best practices. All analytical logic, data processing workflows, and application design are the student's own work.

## Deployment

### Local Deployment

The application is ready to run locally with the installation steps above.

### Cloud Deployment Options

**Option 1: Streamlit Cloud (Recommended)**
```bash
# Push code to GitHub, then deploy via Streamlit Cloud dashboard
# Free tier available, automatic updates from GitHub
```

**Option 2: Heroku**
```bash
# Create Procfile and deploy using Heroku CLI
# Requires paid tier for persistent deployment
```

**Option 3: AWS/Azure/GCP**
- Deploy as containerized application (Docker)
- Use managed services (EC2, App Service, Cloud Run)
- Requires more configuration but offers full control

## Testing

### Manual Testing Checklist

- [ ] Application starts without errors
- [ ] All 8 companies load successfully
- [ ] Time period selection works correctly
- [ ] Moving averages display correctly
- [ ] Volume chart shows data
- [ ] Normalized comparison is accurate
- [ ] Statistical summary calculates correctly
- [ ] CSV export contains all data
- [ ] Charts are interactive (hover, zoom, pan)
- [ ] Sidebar controls update visualizations

### Automated Testing

To add automated tests:
```bash
pip install pytest streamlit-testing-util
pytest tests/
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError: No module named 'streamlit'" | Run `pip install -r requirements.txt` |
| "No data available for ticker" | Check ticker symbol; Yahoo Finance may not have data for that company |
| "Slow performance with large date ranges" | Data is cached; clear cache with `streamlit cache clear` |
| "Charts not displaying" | Check internet connection; Plotly requires CDN access |

### Debug Mode

Enable debug logging:
```bash
streamlit run app.py --logger.level=debug
```

## License

This project is provided for educational purposes as part of ACC102 coursework.

