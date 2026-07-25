# medicine-predictor-app
A real-time web application that scrapes live medicine prices from Pakistani pharmacies and uses Supervised Machine Learning to predict prices for the next 7 days.

### 🎯 Problem Statement
Medicine prices in Pakistan fluctuate frequently with no central tracking system. Patients often overpay due to lack of transparency.

### ✅ Solution
Built an end-to-end data pipeline that:
1.  *Scrapes* live medicine data every time the app loads
2.  *Trains* a Supervised ML model on historical trends  
3.  *Predicts* future prices to help patients and pharmacies make informed decisions

---

### 🛠️ Tech Stack
- *Language:* Python
- *Web Scraping:* Requests, BeautifulSoup
- *ML Model:* Scikit-learn, Linear Regression
- *Data Viz:* Plotly
- *Framework:* Streamlit
- *Deployment:* Streamlit Cloud + GitHub
