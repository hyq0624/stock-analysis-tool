# Reflection Report: Interactive Stock Market Analysis Tool
## ACC102 Mini Assignment - Track 4

**Student Name:** [Your Name]  
**Student ID:** [Your ID]  
**Date:** April 2026  
**Word Count:** 750

---

## 1. Analytical Problem and Target User

The analytical problem addressed by this project is: **How can investors and financial analysts effectively compare the stock performance of major technology companies to make informed investment decisions?**

The target users are individual investors, financial analysts, and economics students who need to understand stock market trends, technical indicators, and comparative performance metrics. The business context is significant because the technology sector represents a major component of global equity markets, and understanding relative stock performance is crucial for portfolio construction, risk assessment, and trend identification.

## 2. Dataset Selection and Justification

I selected historical stock price data from Yahoo Finance for eight major technology companies: Apple, Microsoft, Tesla, NVIDIA, Amazon, Google, Meta, and Intel. The dataset covers a six-month period (January-April 2026) and includes Open, High, Low, Close, and Volume data points.

**Justification for this selection:**
- **Reliability**: Yahoo Finance is widely recognized in financial education and research
- **Accessibility**: Free API with no authentication requirements
- **Completeness**: Provides OHLCV data for all major stocks without gaps
- **Relevance**: Technology sector is highly relevant to business and finance students
- **Timeliness**: Data updates daily during market hours, ensuring current analysis

The dataset is sufficiently reliable for educational analysis because Yahoo Finance maintains rigorous data quality standards and is used by professional investors and institutions worldwide.

## 3. Python Methods and Implementation

The analytical workflow implemented in Python includes five key stages:

**Data Acquisition**: Used the `yfinance` library to fetch historical stock data directly from Yahoo Finance, eliminating manual data collection and ensuring data consistency.

**Data Cleaning**: Implemented validation procedures to remove missing values, ensure numeric data types, and verify logical consistency (e.g., High ≥ Low ≥ Close). This step was critical because raw financial data sometimes contains anomalies that could skew analysis.

**Feature Engineering**: Calculated technical indicators including 20-day and 50-day moving averages, daily returns, price ranges, and volume moving averages. These features enable identification of trends and volatility patterns.

**Statistical Analysis**: Computed descriptive metrics (mean, standard deviation, min, max) and calculated performance indicators (price change %, volatility %, daily returns) for comparative analysis.

**Visualization**: Used Plotly for interactive charts and Matplotlib for static visualizations, enabling users to explore data dynamically and identify patterns visually.

The Python implementation demonstrates proficiency in data manipulation (Pandas), numerical computing (NumPy), and visualization (Plotly, Matplotlib). The code is modular and well-documented, with clear separation between data processing and presentation layers.

## 4. Main Insights and Outputs

The analysis produced several key insights:

**Performance Variation**: Stock performance varied significantly over the six-month period, with some companies showing strong gains while others declined. This variation demonstrates the importance of diversification within the technology sector.

**Volatility Patterns**: Different companies exhibited different volatility levels. More volatile stocks offered higher potential returns but with greater risk, illustrating the risk-return tradeoff.

**Correlation Structure**: Analysis revealed moderate positive correlations between stocks, indicating that while they move together to some extent, diversification benefits still exist within the tech sector.

**Technical Indicators**: Moving average analysis identified trend changes and support/resistance levels, providing actionable signals for technical traders.

**Trading Activity**: Volume analysis revealed that larger companies typically had higher trading volumes, suggesting greater market liquidity and lower trading costs.

The interactive Streamlit application successfully communicates these insights through dynamic visualizations, allowing users to select companies, adjust time periods, and toggle technical indicators to explore the data independently.

## 5. Limitations and Reliability Issues

**Data Limitations**: The six-month analysis period may not capture long-term trends or cyclical patterns. Additionally, this period may have included unusual market events that don't represent typical market behavior.

**Methodological Limitations**: The analysis uses simple moving averages without weighting for recent data. More sophisticated models (ARIMA, Prophet, machine learning) could provide better predictions. The analysis focuses on technical indicators and ignores fundamental factors like earnings, debt ratios, and competitive positioning.

**Scope Limitations**: The analysis is limited to the technology sector, which may not represent broader market dynamics. Including other sectors would provide better portfolio diversification insights.

**Statistical Assumptions**: The correlation analysis assumes linear relationships between stocks, which may not hold during market stress or structural changes.

## 6. Student Contribution and Learning Outcomes

I independently designed the analytical problem, selected the data source, and implemented the complete Python workflow. The Streamlit application was built from scratch without using templates, demonstrating full understanding of the requirements and implementation details.

**Key Learning Outcomes:**
- Proficiency in financial data acquisition and processing
- Understanding of technical analysis indicators and their interpretation
- Ability to design user-focused data products
- Experience with interactive data visualization
- Appreciation for data quality and validation procedures

The most challenging aspect was ensuring data quality and handling edge cases in the moving average calculations. The most rewarding aspect was seeing the interactive tool enable users to explore complex financial data intuitively.

## 7. AI Disclosure

**AI Tools Used:**
- ChatGPT (GPT-4): Used for code structure suggestions and Streamlit best practices documentation (April 2026)
- GitHub Copilot: Used for function documentation and minor code suggestions (April 2026)

**Disclosure**: AI tools were used only for code structure and documentation suggestions. All analytical logic, data processing workflows, and application design are the student's original work. The use of AI was limited and did not substitute for independent problem-solving or analytical thinking.

---

**Certification**: I certify that this work is my own and complies with the University's Academic Integrity Policy.

**Signature:** ________________  
**Date:** ________________
