# Credit Card Fraud Detection Using Snowflake ML


## Overview

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
├── script/app/
│     ├── Fraud_Detection_Optimized.py        # Python packages
│     └── environment.yml
│
├── notebooks/
│   ├── 0_start_here.ipynb
│   └── 1_CC_FRAUD_DETECTION.ipynb
│
│
└── README.md
```



## ⚙️ Snowflake Setup

To prepare your Snowflake environment for this project:

1. **Create Core Objects**  
   Use Snowsight to create a database, schema, warehouse, and internal stage for storing app files:
   - Database: `CC_FINS_DB`
   - Schema: `ANALYTICS`
   - Warehouse: `FD_WH`
   - Internal Stage: `CC_FINS_DB.ANALYTICS.FRAUD_DETECTION_APP`

2. **Import Notebooks in Snowsight**  
   Upload the project notebooks (`0_start_here.ipynb` and `1_CC_FRAUD_DETECTION.ipynb`) using the **Notebooks** section in Snowsight.

3. **Install Required Packages**  
   From the “Packages” button in Snowsight, ensure the following are added: altair, seaborn, matplotlib and snowflake-ml-python


This setup enables you to run feature engineering, model training, and predictions directly within Snowflake using Notebooks.




## 🧪 Initial Data Setup & Feature Engineering

The end to end architecture involving all the stages is given below.

![image](https://github.com/user-attachments/assets/f5e4240d-ccd9-4c26-be0d-031b34f6fd0e)




The first notebook, `0_start_here.ipynb`, covers initial data ingestion and feature engineering required for fraud detection.

- Synthetic transaction data is loaded from a public S3 bucket into a **Snowflake external stage**, and then into a target table.
- The dataset includes numerical and categorical features such as:
  - Transaction date, amount, location, and card number
  - Behavioral attributes like clicks, time elapsed, logins per hour, and pages visited

These fields simulate realistic card transaction behaviors and help train the model to detect fraud patterns more effectively.

Using **Snowflake’s Feature Store**, we also compute customer-centric features such as:
- Total number of transactions per user
- Average spending per week, month, and year

This engineered data becomes the foundation for training a high-performing binary classification model in the next step.


A sample output from the engineered features dataset related to Customer is seen below.

![image](https://github.com/user-attachments/assets/1bc15932-2273-4a84-b339-c1a00b58a6ae)



Similarly the features related to Transaction data is generated that includes clicks, time elapsed before a transaction,cumulative logins, pages visited and the location such transaction originates from.A sample output from the engineered features dataset related to Transactions is seen below.

![image](https://github.com/user-attachments/assets/fa0d3ea0-4614-42b5-b95a-6af283f26829)



## 🤖 Model Training & Evaluation

The second notebook, `2_CC_FRAUD_DETECTION.ipynb`, focuses on feature consumption, exploratory data analysis, model training, and validation.

Key highlights:
- Visualize trends using packages like `altair`, `matplotlib`, and `seaborn` within Snowflake Notebooks
- Join raw data with engineered features to enrich a **spine Snowpark DataFrame**
- Train a binary classification model using `snowflake.ml.classification`
- Use the trained model’s `PREDICT` method to classify new transactions

```sql
SELECT *, CC_FINS_DB.ANALYTICS.fraud_classification_model!PREDICT(INPUT_DATA => object_construct(*)) AS predictions
FROM fraud_classification_val_view;
```

### 📈 Model Evaluation

The model's performance is assessed using built-in Snowflake ML functions:


## 🌍 Streamlit App with Geospatial Fraud Detection

Build an interactive fraud detection dashboard using **Streamlit in Snowflake**, featuring geospatial analysis with **PyDeck**.

- Visualize transaction patterns on an interactive map
- Highlight fraudulent activity with color-coded markers
- Run real-time predictions and display results with tooltips and charts

### 1. Load Streamlit Files
![Screenshot 2025-04-22 at 20 09 43](https://github.com/user-attachments/assets/eb83869e-5387-4d4b-938b-ad2e3746aac3)

   
### 2. Create the Streamlit App and Run the code below in a Snowsight worksheet to build the Streamlit app.

```sql
CREATE OR REPLACE STREAMLIT CC_FINS_DB.ANALYTICS.FRAUDDETECTION_APP
ROOT_LOCATION = '@CC_FINS_DB.ANALYTICS.FRAUD_DETECTION_APP'
MAIN_FILE = 'Fraud_Detection_Optimized.py'
QUERY_WAREHOUSE = 'CC_FINS_WH';
```

### 3. Open the Streamlit app from **Snowsight > Projects > Streamlit** and launch `FRAUDDETECTION_APP`.

New transaction types appear at the top of the dashboard, ready for fraud detection and prediction.

![Screenshot 2025-04-22 at 20 24 48](https://github.com/user-attachments/assets/8784d436-2ef1-4da5-a45b-8bd21448c9b3)

