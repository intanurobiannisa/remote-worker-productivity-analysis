import streamlit as st
import pandas as pd
import altair as alt

st.title("💻 Remote Worker Analysis")
st.write(
    """Created by Intan Nur Robi Annisa – student of Data Science and Data Analyst Bootcamp at Dibimbing.  
    [LinkedIn Profile](https://www.linkedin.com/in/intannurrobiannisa)"""
)

# Load the data from a CSV
@st.cache_data
def load_data():
    df = pd.read_csv("data/remote_worker_productivity_1000_final.csv")
    return df

df = load_data()

st.subheader("Preview")
st.write(
    """The productivity level of remote workers in a company is mostly at a medium level, with an average late task ratio of nearly 20%. To improve overall performance and efficiency, the company needs to increase productivity levels.  
    Therefore, this project aims to analyze the work behavior and demographics of its remote workers in order to improve productivity levels."""
)

st.subheader("Overall Summary")
st.write(
    "From 1000 remote workers, they are spread relatively evenly across demographic groups, showing that remote work spans various backgrounds and is not limited to specific industries, age groups, or regions. " \
    "The number of workers from cities, towns, and villages shows nearly equal representation. Industry sectors such as Education, IT, and Retail contribute similar worker counts, while Healthcare and Finance have slightly smaller numbers. " \
    "Age and experience distributions are broad yet balanced, with noticeable peaks around age 42 and 17 years of experience—indicating a mature and seasoned workforce at the core of the dataset."
)

# Show a multiselect widget with the industry sector using `st.multiselect`.
industries = st.multiselect(
    "Workers by the Industry Sector",
    df.industry_sector.unique(),
)

# Filter the DataFrame based on selection
if industries:
    filtered_df = df[df.industry_sector.isin(industries)]
else:
    filtered_df = df  # Show all data if nothing is selected

# Display the filtered data as a table
with st.expander("Display DataFrame"):
    st.dataframe(filtered_df, use_container_width=True)

# Create tabs
tab1, tab2, tab3 = st.tabs([
    "Location Type",
    "Age Distribution",
    "Experience Years"
])

with tab1:
    # Location Type Distribution
    st.subheader("Worker Distribution by Location Type")
    location_counts = filtered_df['location_type'].value_counts().reset_index()
    location_counts.columns = ['location_type', 'count']
    location_chart = alt.Chart(location_counts).mark_bar().encode(
        x=alt.X('count:Q', title='Number of Workers'),
        y=alt.Y('location_type:O', title=None),
        color=alt.Color('location_type:N', title='Location Type'),
        tooltip=['location_type', 'count']
    )
    st.altair_chart(location_chart, use_container_width=True)

with tab2:
    # Age Distribution
    st.subheader("Worker Distribution by Age")
    age_counts = filtered_df['age'].value_counts().reset_index()
    age_counts.columns = ['age', 'count']
    age_counts = age_counts.sort_values('age')
    age_chart = alt.Chart(age_counts).mark_bar().encode(
        x=alt.X('age:O', title='Age', axis=alt.Axis(labelAngle=360)),
        y=alt.Y('count:Q', title='Number of Workers'),
        color=alt.Color('count:Q', scale=alt.Scale(scheme='blues'), legend=None),
        tooltip=['age', 'count']
    )
    st.altair_chart(age_chart, use_container_width=True)

with tab3:
    # Experience Years Distribution
    st.subheader("Worker Distribution by Experience Years")
    exp_counts = filtered_df['experience_years'].value_counts().reset_index()
    exp_counts.columns = ['experience_years', 'count']
    exp_counts = exp_counts.sort_values('experience_years')
    exp_chart = alt.Chart(exp_counts).mark_bar().encode(
        x=alt.X('experience_years:O', title='Years of Experience', axis=alt.Axis(labelAngle=360)),
        y=alt.Y('count:Q', title='Number of Workers'),
        color=alt.Color('count:Q', scale=alt.Scale(scheme='greens'), legend=None),
        tooltip=['experience_years', 'count']
    )
    st.altair_chart(exp_chart, use_container_width=True)

st.subheader("Findings")
st.write(
    """Individual work habits—especially effective scheduling, focused time, and on-time task completion—are the strongest predictors of productivity, far outweighing demographic factors like location or tool frequency.  
    Then, A/B testing was used in the case implementation to compare productivity scores between workers who use AI-assisted planning tools and those who frequently use calendar scheduling tools.
    The productivity scores for users of AI-assisted planning vs. high calendar usage (top 25%) are not the same,
    where calendar Scheduling users clearly outperform AI Planning users in productivity score—both by mean (-+9.2 points) and median (-+8.8 points).
"""
)

# Create tabs
tab1, tab2, tab3 = st.tabs([
    "Calendar Scheduling Usage",
    "Focus Time (minutes)",
    "Task Completion Rate"
])

with tab1:
   # Line chart: Productivity Score vs Calendar Scheduling Usage
    st.subheader("📈 Productivity Score vs Calendar Scheduling Usage")
    line_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X("calendar_scheduled_usage:Q", title="Calendar Scheduling Usage"),
        y=alt.Y("productivity_score:Q", title="Productivity Score"),
        tooltip=["calendar_scheduled_usage", "productivity_score"]
        ).properties(
        width=700,
        height=400
    )
    st.altair_chart(line_chart, use_container_width=True)

with tab2:
    # Line chart: Productivity Score vs Focus Time (minutes)
    st.subheader("📈 Productivity Score vs Focus Time (minutes)")
    line_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X("focus_time_minutes:Q", title="Focus Time (minutes)"),
        y=alt.Y("productivity_score:Q", title="Productivity Score"),
        tooltip=["task_completion_rate", "productivity_score"]
        ).properties(
        width=700,
        height=400
    )
    st.altair_chart(line_chart, use_container_width=True)

with tab3:
    # Line chart: Productivity Score vs Task Completion Rate
    st.subheader("📈 Productivity Score vs Task Completion Rate")
    line_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X("task_completion_rate:Q", title="Task Completion Rate"),
        y=alt.Y("productivity_score:Q", title="Productivity Score"),
        tooltip=["task_completion_rate", "productivity_score"]
        ).properties(
        width=700,
        height=400
    )
    st.altair_chart(line_chart, use_container_width=True)

st.write(
        "Higher values are associated with higher productivity."
)

