import plotly.express as px
import pandas as pd
import numpy as np

# Dummy data for 5 locations over time
dates = pd.date_range(start="2024-01-01", periods=10, freq="M")
locations = ["New York", "Los Angeles", "Chicago", "Houston", "Miami"]
data = pd.DataFrame({
    "Date": np.tile(dates, len(locations)),
    "Location": np.repeat(locations, len(dates)),
    "Active_Users": np.random.randint(1000, 7000, size=len(dates) * len(locations))
})

# Create interactive line chart
fig = px.line(data, x="Date", y="Active_Users", color="Location",
              markers=True, title="Active Users Over Time")

fig.show()