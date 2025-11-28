# Interview Preparation Guide: Retail Sales Analysis Project

## Common Interview Questions & Answers

### 1. Can you walk me through your Retail Sales Analysis project?
**Answer**: "I built an end-to-end analytics system to analyze and forecast retail sales. I started by generating and cleaning a dataset of 15,000 transactions. I performed extensive EDA to understand seasonal trends and category performance. Then, I engineered time-series features like lags and rolling averages. I built two forecasting models, SARIMA and Prophet, to predict future sales. Finally, I created an interactive dashboard using Plotly Dash to present KPIs and insights to stakeholders."

### 2. Why did you choose Prophet over SARIMA (or vice versa)?
**Answer**: "I implemented both to compare performance. Prophet handled the strong holiday effects and multiple seasonality (weekly, yearly) better and was faster to tune. SARIMA provided a good baseline and helped understand the autoregressive nature of the data. Ultimately, Prophet gave a slightly lower MAPE and was more robust to outliers."

### 3. How did you handle missing values and outliers?
**Answer**: "For missing values, I used median imputation for numerical features and mode for categorical ones. For outliers, I used the IQR method. However, instead of removing high-value orders (which are valid business events), I capped them at the upper bound to prevent them from skewing the model while retaining the information."

### 4. What feature engineering techniques did you use?
**Answer**: "I focused on capturing temporal patterns. I created lag features (1, 7, 30 days) to capture autocorrelation. I added rolling means and standard deviations (7, 30 days) to capture trends. I also created 'IsHoliday' and 'IsWeekend' flags, which were critical given the retail nature of the data."

### 5. How would you deploy this model in production?
**Answer**: "I would containerize the application using Docker. The data pipeline would run on a schedule (e.g., Airflow) to retrain the model weekly with new data. The dashboard would be hosted on a cloud platform like AWS or Heroku, serving the latest forecasts and insights."

### 6. What was the most challenging part of this project?
**Answer**: "The most challenging part was handling the high variance in daily sales. Retail data is noisy. I solved this by aggregating data to a weekly level for some analyses and using robust scaling. Also, tuning the SARIMA parameters (p, d, q) required careful analysis of ACF/PACF plots."

### 7. What business value did this project provide?
**Answer**: "The forecasting model allows for better inventory planning, reducing stockouts during peak seasons. The discount analysis revealed that discounts >20% were hurting profits without driving enough volume, leading to a recommendation to cap discounts, potentially improving margins by 10-15%."

### 8. How did you evaluate your models?
**Answer**: "I used a time-series cross-validation approach, splitting the last 3 months as a test set. I looked at RMSE (Root Mean Squared Error) to penalize large errors and MAPE (Mean Absolute Percentage Error) to interpret the error in percentage terms, which is easier for business stakeholders to understand."

### 9. Did you detect any anomalies?
**Answer**: "Yes, using Isolation Forest, I detected about 1% of transactions as anomalies. These were mostly bulk orders with unusually high quantities or extremely low prices (deep discounts). identifying these helped in cleaning the training data for better forecasting."

### 10. How would you improve this project further?
**Answer**: "I would incorporate external factors like economic indicators (inflation, GDP) or weather data, which often influence retail sales. I would also try deep learning models like LSTM if the dataset was larger."
