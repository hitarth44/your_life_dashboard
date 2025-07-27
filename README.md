# 📊 Your Life in Data — Personal Activity Dashboard

Ever wondered where your time _actually_ goes online?

**Your Life in Data** is an interactive Streamlit dashboard that visualizes your personal digital habits using your Google Takeout data — including Chrome, YouTube, and Google Maps activity.

---

## 🧠 What This Project Shows

| Skill Area         | What’s Demonstrated                               |
| ------------------ | ------------------------------------------------- |
| Data Engineering   | Parsed & cleaned raw Google JSON into usable form |
| Python + Pandas    | Time-based feature extraction and manipulation    |
| Streamlit Frontend | Built an interactive dashboard with filtering     |
| Data Visualization | Used Altair for time series, bar, and line charts |
| UX Thinking        | Clean layout, sidebar filters, download button    |

---

## 🎯 Features

- **Upload & analyze your own Google activity data**
- View:
  - Most used platforms (Chrome, YouTube, Maps)
  - Activity by hour, weekday, and timeline
  - Keyword search and filter
- Export filtered results as CSV
- Clean, color-coded layout with readable insights
- Uses only Python, Pandas, Altair, and Streamlit

---

## 🧾 Sample Insights

- **Most active day**: Wednesday
- **Most used platform**: YouTube
- **Most common activity hour**: 10 PM

---

## 🚀 Getting Started

1. Download your [Google Takeout](https://takeout.google.com/) data (just select YouTube, Maps, Chrome)
2. Unzip the archive and copy these 3 files to a `data/` folder:
   - `MyActivity.json` for Chrome
   - `MyActivity.json` for YouTube
   - `MyActivity.json` for Maps
3. Rename them as:

   - `chrome_activity.json`
   - `youtube_activity.json`
   - `maps_activity.json`

4. Run the app:

```bash
streamlit run app.py
```

---

## 🧰 Built With

- Python
- Pandas
- Streamlit
- Altair

---

## 🧑‍💻 Author

Made by Hitarth Bhuptani — Data & Python enthusiast
Demo link : https://yourlifedashboard-6xc93nssjaxy3b4azgrwex.streamlit.app/
