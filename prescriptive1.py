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

# 📌 Linear Programming Model (Dynamic Pricing)
def prescribe_price(active_users, num_posts):
    """
    Uses linear programming to determine pricing:
    - Higher active users → Lower price
    - Higher posts → Higher price
    """

    # Objective Function: Maximize price (-1 for minimization in linprog)
    c = [-1]

    # Constraints:
    # - More active users → Lower price
    # - More posts → Higher price
    A = [[1]]  # Needs to be a 2D array
    b = [1000 - (active_users * 0.2) + (num_posts * 0.5)]  # Needs to be a 1D list

    # Bounds: Allow price to be any non-negative value
    bounds = [(0, None)]  

    # Solve linear program
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

    return round(result.x[0], 2) if result.success else 0  


# 📌 Streamlit UI
st.title("📊 Prescriptive Analytics: Dynamic Pricing Model")
st.write("Using **Linear Programming (LP)** to adjust pricing dynamically based on active users & posts.")

# 📌 Select Location
selected_location = st.selectbox("📍 Select a Location", locations)
filtered_data = data[data["Location"] == selected_location].copy()

# 📌 Interactive Sliders 🔥
active_users = st.slider("👥 Active Users", min_value=500, max_value=10000, value=3000, step=100)
num_posts = st.slider("📝 Number of Posts", min_value=10, max_value=1000, value=200, step=10)

# 📌 Calculate Prescribed Price
prescribed_price = prescribe_price(active_users, num_posts)

# 📌 Add to DataFrame
filtered_data["Prescribed_Price (PHP)"] = filtered_data.apply(
    lambda row: prescribe_price(row["Active_Users"], row["Number_of_Posts"]), axis=1
)

# 📌 Display **Recommended Price**
st.metric(label="💰 Recommended Price (PHP)", value=f"₱{prescribed_price}")

# 📌 Plot Pricing Over Time
fig = px.line(filtered_data, x="Date", y="Prescribed_Price (PHP)", markers=True, 
              title=f"Optimal Pricing Over Time for {selected_location}")

st.plotly_chart(fig, use_container_width=True)
