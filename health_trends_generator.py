import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = '#f8f9fa'
plt.rcParams['axes.facecolor'] = 'white'

# Load JSON data
with open('health_report_data.json', 'r') as f:
    report1 = json.load(f)

with open('health_report_data1.json', 'r') as f:
    report2 = json.load(f)

# Extract test data
def get_numeric_value(value):
    """Convert test values to numeric"""
    if isinstance(value, str):
        # Remove non-numeric characters except dots and minus
        value = value.replace('++', '2').replace('+', '1')
        try:
            return float(''.join(c for c in value if c.isdigit() or c == '.' or c == '-'))
        except:
            return None
    return float(value) if value else None

# Prepare data for plotting
test_data = {}
for test in report1['tests']:
    name = test['name']
    val1 = get_numeric_value(test['value'])
    
    # Find corresponding test in report2
    val2 = None
    for test2 in report2['tests']:
        if test2['name'] == name:
            val2 = get_numeric_value(test2['value'])
            break
    
    if val1 is not None and val2 is not None:
        test_data[name] = {
            'values': [val1, val2],
            'unit': test.get('unit', ''),
            'status1': test.get('status', 'NORMAL'),
            'status2': test2.get('status', 'NORMAL') if test2 else 'NORMAL'
        }

# Create subplots - 6 rows x 3 columns
fig = plt.figure(figsize=(20, 28))
fig.suptitle('Health Marker Trend Analysis - KIRANKUMAR PADAPUDI (38Y, Male)', 
             fontsize=24, fontweight='bold', y=0.995)

# Add subtitle
fig.text(0.5, 0.985, '', 
         ha='center', fontsize=14, style='italic', color='#666')

# Select key tests to visualize (adjust as needed)
key_tests = [
    'HEMOGLOBIN', 'Total RBC Count', 'H.CT', 'M.C.V', 'M.C.H.', 'M.C.H.C.',
    'R.D.W', 'Total WBC Count (TLC)', 'Platelet Count', '1 Hour ESR',
    'Polymorphs', 'Lymphocytes', 'Eosinophils', 'Monocytes',
    'Mean Blood Glucose', 'Specific Gravity', 'Urine Volume', 'Urine Glucose'
]

# Filter available tests
available_tests = [t for t in key_tests if t in test_data]

# Plot each test
for idx, test_name in enumerate(available_tests[:18], 1):  # Limit to 18 charts (6x3 grid)
    ax = plt.subplot(6, 3, idx)
    
    data = test_data[test_name]
    values = data['values']
    dates = ['Report 1\n(Jan 2025)', 'Report 2\n(Sep 2025)']
    
    # Create line plot with markers
    colors = ['#3498db', '#e74c3c']
    
    # Plot line
    ax.plot(dates, values, marker='o', linewidth=3, markersize=12, 
            color='#2ecc71' if values[1] < values[0] and 'Glucose' in test_name 
            else '#e74c3c' if values[1] > values[0] and 'HIGH' in data['status2']
            else '#3498db', alpha=0.7)
    
    # Fill area under line
    ax.fill_between(range(len(dates)), values, alpha=0.2, 
                     color='#2ecc71' if values[1] < values[0] and 'Glucose' in test_name
                     else '#3498db')
    
    # Add value labels on points
    for i, (date, val) in enumerate(zip(dates, values)):
        ax.text(i, val, f'{val:.2f}', ha='center', va='bottom', 
                fontsize=10, fontweight='bold', color='#2c3e50')
    
    # Calculate percentage change
    if values[0] != 0:
        pct_change = ((values[1] - values[0]) / values[0]) * 100
        change_text = f'{pct_change:+.1f}%'
        change_color = '#27ae60' if pct_change < 0 and 'Glucose' in test_name else \
                       '#e74c3c' if pct_change > 5 else '#f39c12' if abs(pct_change) > 1 else '#95a5a6'
        
        ax.text(0.98, 0.95, change_text, transform=ax.transAxes,
                fontsize=11, fontweight='bold', color=change_color,
                ha='right', va='top',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                         edgecolor=change_color, linewidth=2))
    
    # Styling
    ax.set_title(test_name, fontsize=12, fontweight='bold', pad=10, color='#2c3e50')
    ax.set_ylabel(f'Value ({data["unit"]})', fontsize=9, color='#7f8c8d')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_ylim([min(values) * 0.9, max(values) * 1.1])
    
    # Add status indicators
    status_color1 = '#e74c3c' if 'HIGH' in data['status1'] or 'ABNORMAL' in data['status1'] else '#27ae60'
    status_color2 = '#e74c3c' if 'HIGH' in data['status2'] or 'ABNORMAL' in data['status2'] else '#27ae60'
    
    ax.scatter([0], [values[0]], s=200, color=status_color1, alpha=0.3, zorder=1)
    ax.scatter([1], [values[1]], s=200, color=status_color2, alpha=0.3, zorder=1)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Add summary box at the bottom
fig.text(0.5, 0.02, 
         '📊 Key Observations: Blood Glucose improved by 19.6% (271.87 → 218.45 mg/dL) | '
         'Hemoglobin normalized (16.2 → 15.4 gm%) | MCHC within range (36.7 → 36.0%) | '
         'All infectious disease markers negative',
         ha='center', fontsize=11, 
         bbox=dict(boxstyle='round,pad=1', facecolor='#ecf0f1', edgecolor='#34495e', linewidth=2),
         wrap=True)

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.98])

# Save figure
plt.savefig('health_trends.png', dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
print("✅ Health trends chart saved as 'health_trends.png'")

# Display the plot
plt.show()
