# Credit Card Fraud Detection Using Snowflake ML


## Project Overview

This project demonstrates how to build an end-to-end credit card fraud detection pipeline using Snowflake ML and Streamlit in Snowflake, enhanced with geospatial visualization via PyDeck.

Credit card fraud detection involves identifying suspicious or unauthorized transactions by analyzing behavioral and transactional patterns. This solution focuses on post-transaction analysis using historical data and Snowflake’s machine learning capabilities to detect potential fraud based on engineered features.


## 📊 Features
- Streamlit UI with interactive map of transactions
- Fraud prediction logic with sample or real data
- PyDeck map with red/green markers by fraud class
- SQL-based feature engineering with Snowflake

## 🛠 Tech Stack
- Snowflake (SQL, Snowpark, Feature Store)
- Streamlit in Snowsight
- PyDeck, Pandas, Altair

## 📁 Project Structure

```
fraud-detection-snowflake-streamlit/
├── app/
│   ├── Fraud_Detection_Optimized.py        # Python packages
│   └── environment.yml
│
├── notebooks/
│   ├── 0_start_here.ipynb
│   └── 1_CC_FRAUD_DETECTION.ipynb│   
│
├── streamlit_code/
│   └── app.py                                      # Streamlit app
│
├── screenshots/
│   └── sis_app_preview.png                         # Screenshot from final email
│
└── README.md
```



##  Run in Snowflake worksheet 
1. Upload the app folder to a Snowflake internal stage
2. Create or replace the Streamlit app:
```sql
CREATE OR REPLACE STREAMLIT CC_FINS_DB.ANALYTICS.FRAUDDETECTION_APP
ROOT_LOCATION = '@CC_FINS_DB.ANALYTICS.FRAUD_DETECTION_APP'
MAIN_FILE = 'Fraud_Detection_Optimized.py'
QUERY_WAREHOUSE = 'CC_FINS_WH';
```
