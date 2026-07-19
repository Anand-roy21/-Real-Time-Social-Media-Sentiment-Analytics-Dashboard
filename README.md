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

- `social_media_posts_20000.csv` - sample source dataset for MySQL or Power BI
- `Real- Time Social Media Sentiment.pbix` - Power BI dashboard
- `Screenshot *.png` - dashboard previews
- `xquik_to_social_media_posts.py` - optional Xquik export converter

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

![Real-Time Social Media Sentiment Analytics dashboard](Screenshot%202026-02-21%20183354.png)

🚀 How to Run

Import `social_media_posts_20000.csv` into MySQL

Run the sentiment scoring or SQL analysis you want to compare

Connect Power BI to MySQL or the converted CSV

Load `Real- Time Social Media Sentiment.pbix`

Optional Xquik import:

```bash
python xquik_to_social_media_posts.py xquik-export.json social_media_posts_xquik.csv
```

The converter accepts Xquik CSV, JSON, JSONL, or NDJSON tweet exports and writes
the same `post_id,platform,username,post_text,post_time,likes,shares,followers`
columns used by the dashboard source data.

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

Xquik is an independent third-party service. Not affiliated with X Corp. "Twitter" and "X" are trademarks of X Corp.
