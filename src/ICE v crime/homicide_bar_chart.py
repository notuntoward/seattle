# %%
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('./dat/homicideVsTrumpMargin.csv')

# Filter rows with Rank <= 20
df_filtered = df[df['Rank'] <= 20].copy()

# Sort by Rank
df_filtered = df_filtered.sort_values('Rank')

# Determine bar colors based on Trump State Margin (using seaborn-like colors)
seaborn_blue = '#1f77b4'
seaborn_red = '#d62728'
colors = [seaborn_red if margin > 0 else seaborn_blue for margin in df_filtered['Trump State Margin (%)']]

# %%
# Create the bar chart
plt.figure(figsize=(12, 6))
x_pos = range(len(df_filtered))

# Create edge colors: black for Minneapolis-St. Paul, none for others
edge_colors = ['black' if city == 'Minneapolis-St. Paul' else 'none' for city in df_filtered['City']]
linewidths = [2 if city == 'Minneapolis-St. Paul' else 0 for city in df_filtered['City']]

bars = plt.bar(x_pos, df_filtered['Homicide Rate (per 100k)'], color=colors, edgecolor=edge_colors, linewidth=linewidths)

# Add labels and title with larger text and bold
plt.xlabel('City', fontsize=14, fontweight='bold')
plt.ylabel('Homicides per 100,000 (FBI RCN)', fontsize=14, fontweight='bold')
plt.title('2024 Homicide Rates (Top 20 Cities)', fontsize=16, fontweight='bold')

# Create legend with larger text
from matplotlib.patches import Patch

from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor=seaborn_red, label='Trump'),
    Patch(facecolor=seaborn_blue, label='Harris')
]

plt.legend(
    handles=legend_elements, 
    title='State Winner',
    prop={'weight': 'bold', 'size': 12},
    title_fontproperties={'weight': 'bold', 'size': 12},
    alignment='left'  # Left-aligns title and entry block
)

# Set x-axis tick labels to city names in sorted order with larger text
plt.xticks(x_pos, df_filtered['City'], rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)

# Bold the Minneapolis-St. Paul x-axis label
labels = plt.gca().get_xticklabels()
for label in labels:
    if label.get_text() == 'Minneapolis-St. Paul':
        label.set_fontweight('bold')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the chart
plt.show()

# %%
# Create second plot - all bars white with blue outlines, Minneapolis-St. Paul solid
plt.figure(figsize=(12, 6))

# Create colors: white with blue outline for all, solid for Minneapolis-St. Paul
colors = ['white'] * len(df_filtered)
edge_colors = [seaborn_blue] * len(df_filtered)
linewidths = [2] * len(df_filtered)

# Find Minneapolis-St. Paul index and make it solid
for i, city in enumerate(df_filtered['City']):
    if city == 'Minneapolis-St. Paul':
        colors[i] = seaborn_blue
        edge_colors[i] = seaborn_blue
        linewidths[i] = 0

bars2 = plt.bar(x_pos, df_filtered['Homicide Rate (per 100k)'], 
                color=colors, edgecolor=edge_colors, linewidth=linewidths)

# Add labels and title with larger text and bold
plt.xlabel('City', fontsize=14, fontweight='bold')
plt.ylabel('Homicides per 100,000 (FBI RCN)', fontsize=14, fontweight='bold')
plt.title('2024 Homicide Rates by City (and Presidential Win)', fontsize=16, fontweight='bold')

# Set x-axis tick labels to city names in sorted order with larger text
plt.xticks(x_pos, df_filtered['City'], rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)

# Bold the Minneapolis-St. Paul x-axis label
labels = plt.gca().get_xticklabels()
for label in labels:
    if label.get_text() == 'Minneapolis-St. Paul':
        label.set_fontweight('bold')

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the second chart
plt.show()

# %%
