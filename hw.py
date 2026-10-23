import pandas as pd, matplotlib as mpl, plotly.graph_objects as go
from plotly.subplots import make_subplots
# from google.colab import drive
import os

# Mount Google Drive
# drive.mount('/content/drive')

# Define the path to the folder containing the sensor data
folder_path = './Hourly Sensor Data'

# Initialize an empty list to store patient data
patients = []

# Check if the folder exists
if os.path.exists(folder_path):
    # List all files in the directory
    for filename in os.listdir(folder_path):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        # Ensure it's a file and not a directory
        if os.path.isfile(file_path):
            try:
                # Assuming the files are CSV. Adjust if different format (e.g., pd.read_excel)
                df = pd.read_csv(file_path)
                patients.append(df)
                print(f"Successfully loaded {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
else:
    print(f"Error: Folder not found at {folder_path}")

# You can now access the data for each patient in the 'patients' list.
# For example, patients[0] will be the DataFrame from the first file.


df_patient_0 = patients[0].copy()
# Convert 'time' column to datetime objects
df_patient_0['time'] = pd.to_datetime(df_patient_0['time'])

# Sort by time to ensure correct plotting
df_patient_0 = df_patient_0.sort_values(by='time').reset_index(drop=True)

# Create subplots with shared x-axis
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, 
                    subplot_titles=('Evolution of Steps Over Time (Patient 0)', 'Evolution of Heartrate Over Time (Patient 0)'))

# Add alternating day backgrounds for Plotly
def add_alternating_day_backgrounds_plotly(fig, df, row, col):
    dates = df['time'].dt.normalize().unique()
    colors = ['rgba(240, 240, 240, 0.5)', 'rgba(255, 255, 255, 0.5)'] # Light gray and white with alpha
    current_color_idx = 0
    shapes = []
    for i in range(len(dates)):
        start_day = dates[i]
        end_day = start_day + pd.Timedelta(days=1)
        shapes.append(go.layout.Shape(
            type="rect",
            xref=f"x{row}", yref=f"y{row}",
            x0=start_day,
            y0=0,
            x1=end_day,
            y1=1,  # Cover the full y-axis range (will be adjusted by yaxis.range)
            fillcolor=colors[current_color_idx],
            layer="below",
            line_width=0,
            opacity=1
        ))
        current_color_idx = 1 - current_color_idx # Alternate color
    fig.update_layout(shapes=shapes)

# Plot steps over time
fig.add_trace(go.Scatter(x=df_patient_0['time'], y=df_patient_0['steps'], mode='lines', name='Steps', 
                         line=dict(color='blue')), row=1, col=1)

# Plot heartrate over time
fig.add_trace(go.Scatter(x=df_patient_0['time'], y=df_patient_0['heartrate'], mode='lines', name='Heartrate', 
                         line=dict(color='red')), row=2, col=1)

# Apply alternating backgrounds to both subplots
add_alternating_day_backgrounds_plotly(fig, df_patient_0, 1, 1)
add_alternating_day_backgrounds_plotly(fig, df_patient_0, 2, 1)

# Update layout for synchronized zooming, axis labels, and remove x-axis tick labels for the top plot
fig.update_layout(
    height=700,
    showlegend=False,
    hovermode="x unified"
)

fig.update_xaxes(title_text='Time (s)', showticklabels=False, row=1, col=1) # No x-axis tick labels for top plot
fig.update_yaxes(title_text='Steps', row=1, col=1)

fig.update_xaxes(title_text='Time (s)', row=2, col=1)
fig.update_yaxes(title_text='Heartrate (bpm)', row=2, col=1)

fig.show()