import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, date, time, timedelta
import time as time_module

# Set page configuration
st.set_page_config(
    page_title="Nicotine Tracker & Motivator",
    page_icon="🚭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and description
st.title("🚭 Nicotine Tracker & Motivator")
st.markdown(
    """
    Quitting nicotine is tough, but you're tougher! This tracker helps you visualize the nicotine decay process in your body, shows health milestones, and motivates you to stay strong.  
    **Every second you resist is progress. Let's do this together!**
    """
)

# Sidebar inputs
st.sidebar.header("Nicotine Parameters")

# Set nicotine half-life (fixed for simplicity)
half_life = 2.0  # Nicotine half-life in hours
st.sidebar.markdown(f"**Nicotine Half-Life (fixed):** {half_life} hours")

# Nicotine dose amount input
dose_amount = st.sidebar.number_input(
    "Nicotine Dose Amount (mg)",
    min_value=0.0,
    value=20.0,
    step=1.0,
    format="%.2f",
    help="Enter the estimated amount of nicotine in your last dose. For reference, a cigarette contains ~10-12 mg, while a vape puff is ~1 mg."
)

st.sidebar.header("Last Nicotine Use")

# Placeholder date and time
placeholder_date = date.today()
placeholder_time = time(0, 0)

dose_date = st.sidebar.date_input(
    "Date of last nicotine use",
    value=placeholder_date,
    min_value=date(1900, 1, 1),
    max_value=date.today(),
    help="Please select the date of your last nicotine use."
)

dose_time = st.sidebar.time_input(
    "Time of last nicotine use",
    value=placeholder_time,
    help="Please select the time of your last nicotine use."
)

# Check if the user has changed both the placeholder date and time
if dose_date == placeholder_date and dose_time == placeholder_time:
    st.error("Please enter the date and time of your last nicotine use.")
    st.stop()

dose_datetime = datetime.combine(dose_date, dose_time)
current_datetime = datetime.now()

# Time difference in hours
time_diff = (current_datetime - dose_datetime).total_seconds() / 3600

if time_diff < 0:
    st.error("Last nicotine use time cannot be in the future.")
    st.stop()

# Additional simulation time into the future
future_time = st.sidebar.number_input(
    "Track Time into the Future (hours)",
    min_value=1.0,
    value=24.0,
    step=1.0,
)

# Number of time points
time_points = st.sidebar.slider(
    "Number of Time Points",
    min_value=50,
    max_value=1000,
    value=500,
    step=50,
)

# Function to calculate nicotine decay
def calculate_nicotine_decay(dose_amount, half_life, time_diff, future_time, time_points):
    total_hours = time_diff + future_time
    time_array = np.linspace(0, total_hours, int(time_points))
    remaining_amount = dose_amount * (0.5 ** (time_array / half_life))
    timestamps = [dose_datetime + timedelta(hours=hr) for hr in time_array]
    return time_array, remaining_amount, timestamps

# Calculate nicotine decay
time_array, remaining_amount, timestamps = calculate_nicotine_decay(
    dose_amount, half_life, time_diff, future_time, time_points
)

# Calculate remaining amount at current time
current_remaining_amount = dose_amount * (0.5 ** (time_diff / half_life))

# Health milestone times
milestones = [
    {"time": 0.33, "label": "Heart Rate Normalizes"},  # 20 minutes
    {"time": 8, "label": "Oxygen Levels Normalize"},
    {"time": 24, "label": "Carbon Monoxide Eliminated"},
    {"time": 48, "label": "Improved Taste"},
    {"time": 72, "label": "Cravings Drop"},
    {"time": 120, "label": "Lungs Improve"},  # 5 days
    {"time": 168, "label": "Energy Increased"},  # 7 days
    {"time": 336, "label": "Improved Circulation"},  # 14 days
    {"time": 720, "label": "Lung Health Improvement"},  # 30 days
]

# Create the plot
fig = go.Figure()

# Decay curve
fig.add_trace(
    go.Scatter(
        x=timestamps,
        y=remaining_amount,
        mode="lines",
        name="Nicotine Decay Curve",
        line=dict(color="cyan"),
    )
)

# Current nicotine level
fig.add_trace(
    go.Scatter(
        x=[current_datetime],
        y=[current_remaining_amount],
        mode="markers",
        marker=dict(color="red", size=15),
        name="Nicotine Level Now",
    )
)

# Add milestones to plot
for milestone in milestones:
    milestone_time = dose_datetime + timedelta(hours=milestone["time"])
    if dose_datetime <= milestone_time <= dose_datetime + timedelta(hours=time_array[-1]):
        fig.add_trace(
            go.Scatter(
                x=[milestone_time],
                y=[0],
                mode="markers+text",
                marker=dict(color="green", size=2),
                text=[milestone["label"]],
                textposition="top center",
                name=milestone["label"],
            )
        )

# Customize layout
fig.update_layout(
    title="Nicotine Decay and Health Milestones",
    xaxis_title="Time",
    yaxis_title="Nicotine Remaining (mg)",
    template="plotly_dark",
    hovermode="x unified",
    legend_title_text="Legend",
)

# Display plot
st.plotly_chart(fig, use_container_width=True)

# Display progress and milestones
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        ### Your Progress:
        - **Last Nicotine Use**: {dose_datetime.strftime('%Y-%m-%d %H:%M:%S')}
        - **Current Time**: {current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
        - **Time Since Last Use**: {time_diff:.2f} hours
        - **Nicotine Remaining**: {current_remaining_amount:.2f} mg
        """
    )

with col2:
    st.markdown("### Health Milestones:")
    for milestone in milestones:
        milestone_time = dose_datetime + timedelta(hours=milestone["time"])
        if milestone_time > current_datetime and milestone_time <= current_datetime + timedelta(hours=future_time):
            hours_left = (milestone_time - current_datetime).total_seconds() / 3600
            st.markdown(f"- **{milestone['label']}** in {hours_left:.1f} hours ({milestone_time:%Y-%m-%d %H:%M})")
        elif milestone_time <= current_datetime:
            st.markdown(f"- **{milestone['label']}** achieved at {milestone_time:%Y-%m-%d %H:%M}")



# Footer with encouragement
st.markdown("---")
st.markdown(
    """
    Thanks for checking out my Tracker!
    """,
    unsafe_allow_html=True,
)
