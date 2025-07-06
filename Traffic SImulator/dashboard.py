import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

# Initialize Dash app
app = dash.Dash(__name__)

# CSV file path
csv_file = "summarized_traffic_data.csv"  # Update with actual file path

def load_data():
    """Load and process traffic data for visualizations."""
    try:
        df = pd.read_csv(csv_file, skipinitialspace=True, low_memory=False)

        # Convert 'Start Time' to numeric format (Unix timestamp)
        df["Start Time"] = pd.to_datetime(df["Start Time"], errors="coerce").astype(int) // 10**9

        # Compute total vehicle count per time step
        df["Total Vehicles"] = df["North"] + df["South"] + df["East"] + df["West"]

        # Define 5-second bins for time grouping
        df["Time Bin"] = (df["Start Time"] // 5) * 5

        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there's an error

def plot_heatmap_from_df(df):
    """Creates a Plotly heatmap for traffic congestion over time per direction."""
    if df.empty:
        return px.imshow([[0]], labels={"color": "No Data"}, title="No Data Available")

    # Melt DataFrame to make it suitable for heatmap
    df_melted = df.melt(id_vars=["Start Time"], value_vars=["South", "North", "West", "East"],
                         var_name="Direction", value_name="Vehicle Count")

    # Remove negative values
    df_melted = df_melted[df_melted["Vehicle Count"] >= 0]

    # Create the heatmap
    fig = px.density_heatmap(
        df_melted,
        x="Start Time",
        y="Direction",
        z="Vehicle Count",
        color_continuous_scale="RdYlBu_r",
        title="Traffic Congestion Heatmap",
        labels={"Start Time": "Time (Seconds)", "Direction": "Lane Direction", "Vehicle Count": "Vehicle Count"},
    )

    fig.update_layout(xaxis=dict(tickangle=-45), template="plotly_white")
    return fig

def plot_histogram_from_df(df):
    """Creates a Plotly bar chart of vehicle counts per lane for Dash."""
    if df.empty:
        return px.bar(title="No Data Available")

    lane_counts = {
        "North": df["North"].sum(),
        "South": df["South"].sum(),
        "East": df["East"].sum(),
        "West": df["West"].sum()
    }

    # Convert to DataFrame for Plotly
    df_lanes = pd.DataFrame(lane_counts.items(), columns=["Lane", "Total Vehicles"])

    # Create bar chart
    fig = px.bar(
        df_lanes,
        x="Lane",
        y="Total Vehicles",
        title="Total Vehicle Distribution Across Lanes",
        labels={"Lane": "Traffic Lane", "Total Vehicles": "Vehicle Count"},
        text_auto=True,  # Show values on bars
        color="Lane",
        color_discrete_sequence=["blue", "red", "green", "orange"]  # Custom colors
    )

    fig.update_layout(bargap=0.3, template="plotly_white")  # Space between bars
    return fig

# Layout of Dash app
app.layout = html.Div([
    html.H1("Real-Time Traffic Congestion Dashboard", style={"textAlign": "center"}),

    # Heatmap for traffic congestion per phase
    dcc.Graph(id="heatmap"),

    # Histogram for congestion per lane
    dcc.Graph(id="histogram"),

    # Auto-update every 5 seconds
    dcc.Interval(
        id="interval-update",
        interval=5000,  # Refresh every 5 seconds
        n_intervals=0
    )
])

# Callback to update both heatmap and histogram
@app.callback(
    [Output("heatmap", "figure"), Output("histogram", "figure")],
    [Input("interval-update", "n_intervals")]
)
def update_graphs(n):
    print(f"Refreshing graphs... {n}")  # Debug: check if the callback runs
    df = load_data()
    print(df.head())  # Debug: ensure data updates
    return plot_heatmap_from_df(df), plot_histogram_from_df(df)

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
