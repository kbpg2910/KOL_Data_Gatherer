import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Function to calculate dates based on business days
def add_business_days(start_date, days):
    current_date = start_date
    while days > 0:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # Monday to Friday are <5
            days -= 1
    return current_date

# Streamlit UI
st.title("Critical Path Schedule (CPS) Generator")

# Input for base date
base_date = st.date_input("Select the base date (e.g., briefing day)", datetime.now())

# Input milestones
st.subheader("Define Milestones and Day Offsets")
milestones = {}
num_milestones = st.number_input("Number of milestones", min_value=1, max_value=20, value=5)

# Collect milestone names and offsets
for i in range(num_milestones):
    milestone_name = st.text_input(f"Milestone {i+1} Name", f"Milestone {i+1}")
    day_offset = st.number_input(f"Days after base date for '{milestone_name}'", min_value=0, step=1, value=i * 5)
    milestones[milestone_name] = day_offset

# Option for business days only
use_business_days = st.checkbox("Use business days only (skip weekends)")

# Calculate schedule dates
schedule_data = []
for milestone, days_after in milestones.items():
    if use_business_days:
        milestone_date = add_business_days(base_date, days_after)
    else:
        milestone_date = base_date + timedelta(days=days_after)
    schedule_data.append((milestone, days_after, milestone_date))

# Create DataFrame
schedule_df = pd.DataFrame(schedule_data, columns=["Milestone", "Days After Base Date", "Date"])

# Display the schedule
st.subheader("Generated Schedule")
st.write(schedule_df)

# Download option
csv = schedule_df.to_csv(index=False)
st.download_button("Download Schedule as CSV", csv, "CPS_schedule.csv", "text/csv")
