import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="MCQ Quiz Dashboard", layout="wide")

st.title("📊 MCQ Quiz Analysis Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("quiz_analysis.xlsx")
    return df

df = load_data()

# -----------------------------
# SCORE CLEANING
# -----------------------------
if "Score" in df.columns:
    df["Calculated_Score"] = df["Score"].str.split(" / ").str[0].astype(int)

df["Calculated_Score"] = df["Calculated_Score"].astype(int)

# -----------------------------
# 1. OVERALL ANALYTICS
# -----------------------------
st.header("1. Overall Analytics")

col1, col2, col3 = st.columns(3)

avg_score = round(df["Calculated_Score"].mean(), 2)
max_score = df["Calculated_Score"].max()
min_score = df["Calculated_Score"].min()

col1.metric("Average Score", avg_score)
col2.metric("Highest Score", max_score)
col3.metric("Lowest Score", min_score)

st.info(f"""
📌 **Insights:**
- The average score is **{avg_score}**, indicating overall performance level.
- The highest score is **{max_score}**, showing top achievement.
- The lowest score is **{min_score}**, indicating scope for improvement.
""")

# -----------------------------
# 2. STUDENT LEADERBOARD
# -----------------------------
st.header("2. Student Leaderboard")

top_students = df.sort_values(by="Calculated_Score", ascending=False)

st.dataframe(top_students[["Name", "College", "Department", "Calculated_Score"]])

st.success("""
📌 **Insights:**
- Top students demonstrate strong subject understanding.
- Leaderboard helps identify high performers.
""")

# -----------------------------
# 3. DEPARTMENT PERFORMANCE
# -----------------------------
st.header("3. Department Performance")

dept_perf = df.groupby("Department")["Calculated_Score"].mean().sort_values(ascending=False)

fig1, ax1 = plt.subplots()
dept_perf.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Average Score")
ax1.set_title("Department Performance")

st.pyplot(fig1)

st.info("""
📌 **Insights:**
- Departments with higher averages show better performance.
- Helps compare academic strength across departments.
""")

# -----------------------------
# 4. COLLEGE RANKING
# -----------------------------
st.header("4. College Ranking")

college_perf = df.groupby("College")["Calculated_Score"].mean().sort_values(ascending=False)

fig2, ax2 = plt.subplots()
college_perf.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Average Score")
ax2.set_title("College Ranking")

st.pyplot(fig2)

st.info("""
📌 **Insights:**
- Colleges are ranked based on average scores.
- Highlights institutions with better performance.
""")

# -----------------------------
# 5. QUESTION ANALYSIS
# -----------------------------
st.header("5. Question Analysis")

question_cols = [col for col in df.columns if col.startswith("Q")]

correct_answers = {
    "Q1": "A",
    "Q2": "C",
    "Q3": "C",
    "Q4": "B",
    "Q5": "D"
}

accuracy = {}

for q in question_cols:
    q_name = q.split()[0]  # Extract Q1, Q2 etc.
    correct = correct_answers.get(q_name, None)
    if correct:
        accuracy[q_name] = (df[q] == correct).mean() * 100

acc_df = pd.DataFrame(list(accuracy.items()), columns=["Question", "Accuracy (%)"])

fig3, ax3 = plt.subplots()
ax3.bar(acc_df["Question"], acc_df["Accuracy (%)"])
ax3.set_ylabel("Accuracy (%)")
ax3.set_title("Question-wise Accuracy")

st.pyplot(fig3)

st.dataframe(acc_df)

st.warning("""
📌 **Insights:**
- Questions with high accuracy are easier.
- Questions with low accuracy may be difficult or confusing.
- Helps improve question quality.
""")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("📌 Developed using Streamlit | MCQ Quiz Analysis Project")
