# ACC102 Mini Assignment - Submission Guide
## Track 4: Interactive Data Analysis Tool

**Project Name:** Interactive Stock Market Analysis Tool  
**Submission Deadline:** April 27, 2026 (23:59)  
**Total Mark:** 100 (with up to 20 bonus marks possible)

---

## 📦 Deliverables Checklist

This project includes all required components for Track 4 submission:

### ✅ Core Requirements

| Component | File/Link | Status | Notes |
|-----------|-----------|--------|-------|
| **Interactive Tool** | Streamlit App (`app.py`) | ✓ Complete | Ready to deploy on Streamlit Cloud or GitHub |
| **Python Notebook** | `stock_analysis.ipynb` | ✓ Complete | Shows complete analytical workflow |
| **README** | `README.md` | ✓ Complete | Comprehensive documentation for GitHub |
| **Reflection Report** | `REFLECTION_REPORT.md` | ✓ Complete | 750 words, covers all required sections |
| **Demo Video Script** | `DEMO_VIDEO_SCRIPT.md` | ✓ Complete | 2-3 minute script with recording instructions |

### ✅ Supporting Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies for reproducibility |
| `.gitignore` | Git configuration for clean repository |
| `SUBMISSION_GUIDE.md` | This file - complete submission instructions |

---

## 🚀 Quick Start Guide

### Step 1: Local Testing (Optional)

Before deploying, test the application locally:

```bash
# Navigate to project directory
cd /home/ubuntu/stock_analysis_streamlit

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The application will open at `http://localhost:8501`

### Step 2: Create GitHub Repository

1. **Create a new repository** on GitHub:
   - Repository name: `stock-analysis-tool` (or similar)
   - Description: "Interactive Stock Market Analysis Tool - ACC102 Mini Assignment"
   - Make it **Public** (so the marker can access it)
   - Initialize with README (optional - we have our own)

2. **Clone the repository locally**:
   ```bash
   git clone https://github.com/yourusername/stock-analysis-tool.git
   cd stock-analysis-tool
   ```

3. **Copy all project files** to the repository:
   ```bash
   # Copy all files from stock_analysis_streamlit to the cloned repo
   cp -r /home/ubuntu/stock_analysis_streamlit/* .
   ```

4. **Commit and push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit: Interactive Stock Market Analysis Tool"
   git push origin main
   ```

### Step 3: Deploy on Streamlit Cloud

1. **Sign up for Streamlit Cloud** at https://streamlit.io/cloud
2. **Connect your GitHub account**
3. **Deploy the app**:
   - Click "New app"
   - Select your GitHub repository
   - Select `app.py` as the main file
   - Click "Deploy"

Your app will be live at: `https://[your-username]-stock-analysis-tool.streamlit.app`

**Alternative Deployment Options:**
- **Heroku**: Requires Procfile and additional configuration
- **AWS/Azure/GCP**: More complex but offers full control
- **GitHub Pages**: Not suitable for Streamlit apps (requires backend)

### Step 4: Record Demo Video

1. **Prepare your script**:
   - Use the provided `DEMO_VIDEO_SCRIPT.md`
   - Adjust timing and examples as needed

2. **Recording options**:
   - **Option A**: Record your own voice using screen recording software
   - **Option B**: Use text-to-speech (MiniMax, Google Text-to-Speech, Amazon Polly)
   - **Option C**: Use AI narration tools

3. **Recording software**:
   - **Free**: OBS Studio, built-in screen recorder
   - **Paid**: Camtasia, ScreenFlow, Snagit

4. **Upload video**:
   - YouTube (unlisted or public)
   - GitHub (as release asset)
   - Streamlit Cloud (embed in app)
   - Any video hosting service

5. **Keep video length**: 1-3 minutes as required

### Step 5: Prepare Submission Package

Before submitting to Learning Mall Core (LMO), ensure you have:

1. **GitHub Repository Link**
   - Example: `https://github.com/yourusername/stock-analysis-tool`
   - Must be accessible to the marker

2. **Streamlit App Link**
   - Example: `https://[username]-stock-analysis-tool.streamlit.app`
   - Must be live and functional

3. **Demo Video Link**
   - Example: `https://www.youtube.com/watch?v=xxxxx`
   - Duration: 1-3 minutes

4. **Python Notebook**
   - File: `stock_analysis.ipynb`
   - To be submitted via LMO

5. **Reflection Report**
   - File: `REFLECTION_REPORT.md` (or convert to PDF/Word)
   - Word count: 500-800 words
   - To be submitted via LMO

---

## 📋 Submission Checklist

### Before Submitting to LMO

- [ ] GitHub repository created and all files pushed
- [ ] Streamlit app deployed and tested
- [ ] Demo video recorded, edited, and uploaded
- [ ] Python notebook verified (can be opened and run)
- [ ] Reflection report finalized (500-800 words)
- [ ] README.md is comprehensive and clear
- [ ] All external links are accessible to the marker
- [ ] No personal information or credentials in code/documentation
- [ ] All materials are in English

### LMO Submission (April 27, 2026, 23:59)

Submit the following files via Learning Mall Core:

1. **GitHub Repository Link** (in submission text)
   - Paste the full GitHub URL
   - Ensure it's public and accessible

2. **Streamlit App Link** (in submission text)
   - Paste the full Streamlit Cloud URL
   - Include deployment date/time

3. **Demo Video Link** (in submission text)
   - Paste the full video URL
   - Include video duration

4. **Python Notebook** (file upload)
   - Upload: `stock_analysis.ipynb`
   - Format: Jupyter Notebook (.ipynb)

5. **Reflection Report** (file upload)
   - Upload: `REFLECTION_REPORT.md` or convert to PDF/DOCX
   - Word count: 500-800 words
   - Include AI disclosure at the end

6. **Optional: README** (file upload)
   - Upload: `README.md`
   - Helps marker understand the project

---

## 🎯 Marking Criteria (100 points total)

| Criterion | Points | How to Score Well |
|-----------|--------|-------------------|
| **Problem Definition & Data Relevance** | 20 | Clear problem statement, relevant business dataset, justified data source |
| **Python Implementation** | 30 | Correct data processing, clean code, technical soundness, appropriate methods |
| **Analysis & Insights** | 20 | Meaningful findings, goes beyond surface description, well-interpreted results |
| **Product Design & UX** | 20 | Intuitive interface, clear communication, useful visualizations, user-focused |
| **Reflection & Professional Practice** | 10 | Quality reflection, acknowledges limitations, discloses AI use, proper citations |

### Bonus Marks (up to 20 additional)

Track 4 can earn up to 20 bonus marks for:
- Advanced technical indicators (RSI, MACD, Bollinger Bands)
- Predictive modeling (ARIMA, Prophet, ML models)
- Enhanced UI/UX (custom themes, advanced interactivity)
- Additional features (portfolio analysis, risk metrics, news integration)
- Comprehensive testing and documentation

**Final mark capped at 100 overall**

---

## 🔍 Quality Assurance

### Before Final Submission

1. **Test the Streamlit app**:
   - [ ] All companies load without errors
   - [ ] Time period selection works
   - [ ] Moving averages display correctly
   - [ ] Charts are interactive
   - [ ] Data export works
   - [ ] No console errors

2. **Verify the notebook**:
   - [ ] All cells run without errors
   - [ ] Data loads successfully
   - [ ] Visualizations render
   - [ ] Markdown formatting is clear

3. **Review the reflection report**:
   - [ ] Word count is 500-800 words
   - [ ] All required sections are covered
   - [ ] AI disclosure is complete
   - [ ] No spelling/grammar errors
   - [ ] Proper academic tone

4. **Check documentation**:
   - [ ] README is comprehensive
   - [ ] Installation instructions are clear
   - [ ] Usage examples are provided
   - [ ] Limitations are documented

---

## 📝 Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError" when running app | Run `pip install -r requirements.txt` |
| Streamlit app won't deploy | Check that `requirements.txt` is in root directory |
| No data appears in charts | Check internet connection; Yahoo Finance may be temporarily unavailable |
| Video won't upload | Ensure file size < 100MB; use compression if needed |
| Reflection report too long/short | Use word counter tool; edit to meet 500-800 word requirement |
| GitHub link not accessible | Ensure repository is set to Public, not Private |

---

## 💡 Tips for Success

1. **Start Early**: Don't wait until the last day to record video or deploy app
2. **Test Thoroughly**: Run the app multiple times with different inputs
3. **Document Well**: Clear documentation shows understanding and professionalism
4. **Be Honest**: Acknowledge limitations and AI usage - markers appreciate transparency
5. **Proofread**: Check for spelling and grammar errors in all written materials
6. **Follow Instructions**: Ensure all required components are included and in correct format

---

## 📚 Additional Resources

### Python & Data Analysis
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [yfinance Documentation](https://yfinance.readthedocs.io/)
- [Plotly Documentation](https://plotly.com/python/)

### Streamlit
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cloud Deployment](https://docs.streamlit.io/deploy/streamlit-cloud)
- [Streamlit Components Gallery](https://streamlit.io/components)

### Git & GitHub
- [GitHub Guides](https://guides.github.com/)
- [Git Documentation](https://git-scm.com/doc)

### Financial Analysis
- [Yahoo Finance API](https://finance.yahoo.com/)
- [Technical Analysis Basics](https://www.investopedia.com/terms/t/technicalanalysis.asp)
- [Moving Averages Explained](https://www.investopedia.com/terms/m/movingaverage.asp)

---

## 🤝 Support

If you encounter issues:

1. **Check the README.md** for troubleshooting section
2. **Review the Jupyter notebook** for detailed explanations
3. **Consult Streamlit documentation** for deployment issues
4. **Contact course instructor** for assignment-specific questions

---

## ✨ Final Notes

This project demonstrates a complete Python data product workflow:
- **Problem Definition** → Clear analytical problem
- **Data Acquisition** → Real-time financial data
- **Data Processing** → Cleaning and transformation
- **Analysis** → Statistical and technical analysis
- **Visualization** → Interactive charts and dashboards
- **Communication** → User-focused product design
- **Documentation** → Comprehensive README and notebook

By following this guide, you'll have a professional, production-ready data product that showcases your Python skills and understanding of financial analysis.

**Good luck with your submission! 🚀**

---

**Last Updated:** April 15, 2026  
**Version:** 1.0  
**Status:** Ready for Submission
