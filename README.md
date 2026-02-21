# -Real-Time-Social-Media-Sentiment-Analytics-Dashboard
🚀 Project Overview

This project builds an end-to-end analytics pipeline to monitor real-time social media sentiment using:

MySQL for data storage and querying

Python (VADER NLP) for sentiment analysis

Power BI for interactive dashboards and viral trend detection

It helps brands track public perception, detect sentiment spikes, and identify viral content early.

🧠 Business Problem

Companies lose revenue and reputation when negative sentiment trends go unnoticed.

This system:

Monitors thousands of posts

Flags viral spikes

Tracks emotion trends

Provides real-time KPI alerts

🏗 Tech Stack
Layer	Tools
Data Storage	MySQL
Processing	Python, Pandas, VADER
Visualization	Power BI
Version Control	GitHub
📂 Project Structure
data/        → raw & processed datasets  
sql/         → table creation + analytics queries  
python/      → NLP sentiment pipeline  
powerbi/     → interactive dashboard  
screenshots/ → dashboard visuals  

📈 Key Features

✅ Real-time sentiment scoring
✅ Viral trend detection
✅ KPI alerts for reputation risk
✅ Engagement vs sentiment analysis
✅ Emotion heatmaps

🧪 Sample SQL Join Used
SELECT p.platform, s.sentiment, COUNT(*) 
FROM social_posts p
JOIN sentiment_scores s ON p.post_id = s.post_id
GROUP BY p.platform, s.sentiment;

📸 Dashboard Preview

(Add screenshot here)

🚀 How to Run

Import CSV into MySQL

Run SQL table scripts

Execute Python sentiment pipeline

Connect Power BI to MySQL

Load dashboard

📌 Skills Demonstrated

SQL joins & analytics

NLP sentiment modeling

Data pipelines

KPI dashboard design

Business storytelling

⭐ Future Improvements

Live API streaming

Topic modeling

Automated refresh

Brand-specific monitoring
