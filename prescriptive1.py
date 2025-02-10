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

# Apply LP Model to Data
data["Prescribed_Price (PHP)"] = data.apply(lambda row: prescribe_price(row["Active_Users"], row["Number_of_Posts"]), axis=1)

# 📌 Streamlit UI
st.title("📊 Prescriptive Analytics: Optimized Pricing Model")
st.write("Using **Linear Programming (LP)** to prescribe the best price based on active users & posts.")

# 📌 Select Location
selected_location = st.selectbox("Select a Location", locations)
filtered_data = data[data["Location"] == selected_location]

# 📌 Plot Data
fig = px.line(filtered_data, x="Date", y="Prescribed_Price (PHP)", markers=True, title=f"Optimal Pricing Over Time for {selected_location}")
st.plotly_chart(fig, use_container_width=True)
