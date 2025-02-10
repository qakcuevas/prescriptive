import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from scipy.optimize import linprog

# 📌 Dummy Data
dates = pd.date_range(start="2024-01-01", periods=10, freq="ME")
locations = ["Manila", "Quezon City"]
data = pd.DataFrame({
    "Date": np.tile(dates, len(locations)),
    "Location": np.repeat(locations, len(dates)),
    "Active_Users": np.random.randint(1000, 7000, size=len(dates) * len(locations)),
    "Number_of_Posts": np.random.randint(50, 500, size=len(dates) * len(locations))
})

# 📌 Linear Programming Model (Prescriptive Analytics)
def prescribe_price(active_users, num_posts):
    """
    Uses linear programming to optimize pricing based on active users & posts.
    """
    c = [-1]  # Coefficient for objective function (maximize price)
    A = [[1], [-1]]  # Constraint coefficients
    b = [active_users * 0.1 + num_posts * 0.5, 5000]  # Constraints
    bounds = [(0, None)]  # Price should be non-negative

    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")
    return round(result.x[0], 2) if result.success else 0  # Get optimized price

# 📌 Streamlit UI
st.title("📊 Prescriptive Analytics: Optimized Pricing Model")
st.write("Using **Linear Programming (LP)** to prescribe the best price based on active users & posts.")

# 📌 Select Location
selected_location = st.selectbox("📍 Select a Location", locations)
filtered_data = data[data["Location"] == selected_location]

# 📌 Add **Sliders** for Interactive Adjustments 🔥
active_users = st.slider("👥 Active Users", min_value=500, max_value=10000, value=3000, step=100)
num_posts = st.slider("📝 Number of Posts", min_value=10, max_value=1000, value=200, step=10)

# 📌 Calculate the **Prescribed Price** in PHP based on the user inputs
prescribed_price = prescribe_price(active_users, num_posts)

# 📌 Display the **Recommended Price**
st.metric(label="💰 Recommended Price (PHP)", value=f"₱{prescribed_price}")

# 📌 Plot Data
fig = px.line(filtered_data, x="Date", y="Prescribed_Price (PHP)", markers=True, 
              title=f"Optimal Pricing Over Time for {selected_location}")
st.plotly_chart(fig, use_container_width=True)
