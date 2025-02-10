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

# 📌 Linear Programming Model (Inverse Pricing)
def prescribe_price(active_users, num_posts):
    """
    Uses linear programming to determine pricing:
    - Higher active users → Lower price
    - Higher posts → Higher price
    """
    c = [-1]  # Maximize price

    # Constraints:
    # - Active users should **decrease** price (+ coefficient)
    # - Number of posts should **increase** price (- coefficient)
    A = [[1], [-1]]  # Flip inequalities
    b = [5000, active_users * 0.05 - num_posts * 0.5]  # Upper limit on price

    bounds = [(0, None)]  # Price should be non-negative

    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

    return round(result.x[0], 2) if result.success else 0  


# 📌 Streamlit UI
st.title("📊 Prescriptive Analytics: Inverse Pricing Model")
st.write("Using **Linear Programming (LP)** to prescribe the best price based on active users & posts.")

# 📌 Select Location
selected_location = st.selectbox("📍 Select a Location", locations)
filtered_data = data[data["Location"] == selected_location].copy()  # Ensure it's a copy

# 📌 Add **Sliders** for Interactive Adjustments 🔥
active_users = st.slider("👥 Active Users", min_value=500, max_value=10000, value=3000, step=100)
num_posts = st.slider("📝 Number of Posts", min_value=10, max_value=1000, value=200, step=10)

# 📌 Calculate the **Prescribed Price** in PHP based on the user inputs
prescribed_price = prescribe_price(active_users, num_posts)

# 📌 Add the prescribed price column to `filtered_data`
filtered_data["Prescribed_Price (PHP)"] = filtered_data.apply(
    lambda row: prescribe_price(row["Active_Users"], row["Number_of_Posts"]), axis=1
)

# 📌 Display the **Recommended Price**
st.metric(label="💰 Recommended Price (PHP)", value=f"₱{prescribed_price}")

# 📌 Plot Data
fig = px.line(filtered_data, x="Date", y="Prescribed_Price (PHP)", markers=True, 
              title=f"Optimal Pricing Over Time for {selected_location}")

st.plotly_chart(fig, use_container_width=True)
