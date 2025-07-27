
import streamlit as st
import pandas as pd
import json
import altair as alt
import joblib

# ----------- Load Data Functions ----------- #
@st.cache_data
def load_activity(file_path, source):
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    records = []

    for r in data:
        time = r.get("time")
        title = r.get("title", "")
        url = r.get("titleUrl", "")
        header = r.get("header", "")
        extra = ""
        if source == "YouTube":
            extra = r.get("subtitles", [{}])[0].get("name", "")
        elif source == "Maps":
            extra = r.get("description", "")
        else:
            extra = header

        records.append({
            "time": time,
            "title": title,
            "url": url,
            "source": source,
            "extra": extra,
            "header": header
        })

    df = pd.DataFrame(records)
    df['time'] = pd.to_datetime(df['time'], format='mixed', errors='coerce')
    df = df.dropna(subset=['time'])
    df['date'] = df['time'].dt.date
    df['hour'] = df['time'].dt.hour
    df['weekday'] = df['time'].dt.day_name()
    return df

# ----------- Main Script ----------- #
st.set_page_config("Your Life in Data", layout="wide")
st.title("📊 Your Life in Data Dashboard")

df_chrome = load_activity('data/chrome_activity.json', 'Chrome')
df_youtube = load_activity('data/youtube_activity.json', 'YouTube')
df_maps = load_activity('data/maps_activity.json', 'Maps')

df = pd.concat([df_chrome, df_youtube, df_maps])

# After loading data and concatenating, check for 'source'
activity_by_day = df.groupby(['date', 'source']).size().reset_index(name='activity_count')

st.markdown("### 🌟 Highlights")
col1, col2, col3 = st.columns(3)
col1.metric("Total Activities", len(df))
col2.metric("Most Active Day", df['weekday'].value_counts().idxmax())
col3.metric("Most Used Platform", df['source'].value_counts().idxmax())

st.markdown("---")

model = joblib.load('notebook/activity_predictor_model.pkl')
activity_by_day = pd.read_pickle('notebook/activity_by_day.pkl')

# Feature extraction for prediction
latest_day = activity_by_day.iloc[-1]
next_features = pd.DataFrame([{
    'weekday': (latest_day['weekday'] + 1) % 7,  # Next day (circular, 0-6)
    'prev_day': latest_day['activity_count'],
    'prev_2day': activity_by_day.iloc[-2]['activity_count']
}])

# Feature extraction for prediction
latest_day = activity_by_day.iloc[-1]
next_features = pd.DataFrame([{
    'weekday': (latest_day['weekday'] + 1) % 7,  # Next day (circular, 0-6)
    'prev_day': latest_day['activity_count'],
    'prev_2day': activity_by_day.iloc[-2]['activity_count']
}])

# Prediction for tomorrow's activity
prediction = model.predict(next_features)[0]
prediction_prob = model.predict_proba(next_features)[0][1]


# --------------- Tab 1: Activity Prediction ---------------
with st.sidebar:
    
    tab1, tab2, tab3 = st.tabs(["Prediction", "Filters", "Insights"])
    with tab1:
        st.subheader("Tomorrow's Activity Prediction")

        if prediction == 1:
            st.markdown(f"💪 **Prediction**: You will be active tomorrow! (Confidence: {prediction_prob*100:.2f}%)")
        else:
            st.markdown(f"😌 **Prediction**: You will likely be inactive tomorrow. (Confidence: {prediction_prob*100:.2f}%)")


    with tab2:
        st.header("🔎 Filters")
        sources = st.multiselect("Filter by Source", df['source'].unique(), default=list(df['source'].unique()))
        df = df[df['source'].isin(sources)]

        keyword = st.text_input("Search Keyword in Title")
        if keyword:
            df = df[df['title'].str.contains(keyword, case=False, na=False)]


    with tab3:
        st.header("Highlighted Insights")
        active_dates = pd.Series(df['date'].unique()).sort_values()
        streak = 1
        max_streak = 1

        for i in range(1, len(active_dates)):
            if (active_dates.iloc[i] - active_dates.iloc[i - 1]).days == 1:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 1

        st.markdown(f"🔥 **Longest Active Streak**: `{max_streak}` days")

        full_range = pd.date_range(df['date'].min(), df['date'].max())
        missing = full_range.difference(pd.to_datetime(df['date'].unique()))
        st.markdown(f"🧘 **Digital Detox Days**: `{len(missing)}` days with 0 activity")

        hour_mode = df.groupby(['date'])['hour'].agg(lambda x: x.mode().iloc[0])
        top_hour = hour_mode.mode().iloc[0]
        st.markdown(f"⏱️ **Most Consistent Activity Hour**: `{top_hour}:00`")

# Download Button
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name='your_life_data.csv',
    mime='text/csv'
)
st.markdown('---')
# Top Platforms
st.markdown("### 📌 Most Used Platforms")
st.markdown("This chart shows which platforms you use the most—great for spotting digital patterns.")

platform_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('source:N', title='Platform'),
    y=alt.Y('count()', title='Activity Count'),
    color='source:N',
    tooltip=['source', 'count()']
).properties(width=600, height=300)

st.altair_chart(platform_chart, use_container_width=True)

# Activity by Hour
st.markdown("### ⏰ Hourly Activity Trend")
st.markdown("Understand when you're most active in a day. Are you a night owl or early riser?")

hour_chart = alt.Chart(df).mark_bar(color='#08fdd8').encode(
    x=alt.X('hour:O', title='Hour of Day'),
    y='count()',
    tooltip=['hour', 'count()']
).properties(width=600, height=300)

st.altair_chart(hour_chart, use_container_width=True)

# Activity by Weekday
st.markdown("### 📆 Weekday Activity Trend")
st.markdown("See which days you’re most digitally active. Helps find patterns in your weekly routine.")

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['weekday'] = pd.Categorical(df['weekday'], categories=weekday_order, ordered=True)

weekday_chart = alt.Chart(df).mark_bar(color='#f54291').encode(
    x=alt.X('weekday:N', title='Day of Week'),
    y='count()',
    tooltip=['weekday', 'count()']
).properties(width=600, height=300)

st.altair_chart(weekday_chart, use_container_width=True)

# Daily Timeline
st.markdown("### 📅 Daily Activity Timeline")
st.markdown("Tracks how your activity fluctuates across dates. Useful to detect binge days or break periods.")

daily_chart = alt.Chart(df).mark_line(color='#ffaa00').encode(
    x=alt.X('date:T', title='Date'),
    y='count()',
    tooltip=['date', 'count()']
).properties(width=800, height=300)

st.altair_chart(daily_chart, use_container_width=True)

# Raw Data
with st.expander("🔍 Raw Activity Data"):
    st.dataframe(df[['time', 'title', 'source', 'extra']].sort_values('time', ascending=False))


