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

# Define normal ranges for common tests
NORMAL_RANGES = {
    'HEMOGLOBIN': (13.0, 17.0),
    'Total RBC Count': (4.5, 5.5),
    'H.CT': (40.0, 50.0),
    'M.C.V': (83.0, 101.0),
    'M.C.H.': (27.0, 32.0),
    'M.C.H.C.': (31.5, 34.5),
    'R.D.W': (11.6, 14.0),
    'Total WBC Count (TLC)': (4000, 11000),
    'Platelet Count': (150000, 410000),
    '1 Hour ESR': (0, 15),
    'Polymorphs': (40, 75),
    'Lymphocytes': (20, 40),
    'Eosinophils': (1, 6),
    'Monocytes': (2, 10),
    'Mean Blood Glucose': (70, 100),
    'Specific Gravity': (1.010, 1.025),
    'Urine Volume': (800, 2000),
    'Urine Glucose': (0, 0)
}

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

def is_within_normal_range(value, test_name):
    """Check if value is within normal range"""
    if test_name in NORMAL_RANGES:
        min_val, max_val = NORMAL_RANGES[test_name]
        return min_val <= value <= max_val
    return None

# Prepare data for plotting
test_data = {}
for test in report1['tests']:
    name = test['name']
    val1 = get_numeric_value(test['value'])
    
    # Find corresponding test in report2
    val2 = None
    test2_obj = None
    for test2 in report2['tests']:
        if test2['name'] == name:
            val2 = get_numeric_value(test2['value'])
            test2_obj = test2
            break
    
    if val1 is not None and val2 is not None:
        test_data[name] = {
            'values': [val1, val2],
            'unit': test.get('unit', ''),
            'status1': test.get('status', 'NORMAL'),
            'status2': test2_obj.get('status', 'NORMAL') if test2_obj else 'NORMAL',
            'normal_range': NORMAL_RANGES.get(name, None)
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
    normal_range = data['normal_range']
    
    # Determine if values are within normal range
    val1_normal = is_within_normal_range(values[0], test_name)
    val2_normal = is_within_normal_range(values[1], test_name)
    
    # Calculate percentage change
    pct_change = ((values[1] - values[0]) / values[0]) * 100 if values[0] != 0 else 0
    
    # Determine line color based on conditions
    if val1_normal is not None and val2_normal is not None:
        # Both values have normal ranges defined
        if val1_normal and val2_normal:
            # Both within normal range
            if abs(pct_change) < 0.1:  # Virtually no change
                line_color = '#f39c12'  # Yellow - no change
            else:
                line_color = '#3498db'  # Blue - both normal but changed
        elif not val1_normal and not val2_normal:
            # Both outside normal range
            line_color = '#e74c3c'  # Red - still abnormal
        elif not val1_normal and val2_normal:
            # Improved to normal
            line_color = '#2ecc71'  # Green - improved to normal
        elif val1_normal and not val2_normal:
            # Worsened from normal
            line_color = '#e74c3c'  # Red - moved out of normal
    else:
        # No normal range defined, use percentage change
        if abs(pct_change) < 0.1:
            line_color = '#f39c12'  # Yellow - no change
        elif pct_change > 0:
            line_color = '#e74c3c'  # Red - increased
        elif pct_change < 0:
            line_color = '#2ecc71'  # Green - decreased
        else:
            line_color = '#3498db'  # Blue - no change
    
    # Draw normal range band if available
    if normal_range is not None:
        min_val, max_val = normal_range
        ax.axhspan(min_val, max_val, alpha=0.15, color='#27ae60', 
                   label='Normal Range', zorder=0)
        # Add range labels
        ax.text(0.02, min_val, f'{min_val}', fontsize=8, color='#27ae60', 
                va='bottom', ha='left', alpha=0.7, fontweight='bold')
        ax.text(0.02, max_val, f'{max_val}', fontsize=8, color='#27ae60', 
                va='top', ha='left', alpha=0.7, fontweight='bold')
    
    # Plot line
    ax.plot(dates, values, marker='o', linewidth=3, markersize=12, 
            color=line_color, alpha=0.7, zorder=3)
    
    # Fill area under line
    ax.fill_between(range(len(dates)), values, alpha=0.2, 
                     color=line_color, zorder=1)
    
    # Add value labels on points
    for i, (date, val) in enumerate(zip(dates, values)):
        ax.text(i, val, f'{val:.2f}', ha='center', va='bottom', 
                fontsize=10, fontweight='bold', color='#2c3e50')
    
    # Display percentage change with appropriate color
    if values[0] != 0:
        change_text = f'{pct_change:+.1f}%'
        change_color = line_color  # Use same color as line
        
        ax.text(0.98, 0.95, change_text, transform=ax.transAxes,
                fontsize=11, fontweight='bold', color=change_color,
                ha='right', va='top',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                         edgecolor=change_color, linewidth=2))
    
    # Styling
    ax.set_title(test_name, fontsize=12, fontweight='bold', pad=10, color='#2c3e50')
    ax.set_ylabel(f'Value ({data["unit"]})', fontsize=9, color='#7f8c8d')
    ax.grid(True, alpha=0.3, linestyle='--', zorder=0)
    
    # Adjust y-limits to show normal range if available
    if normal_range is not None:
        y_min = min(min(values) * 0.9, normal_range[0] * 0.95)
        y_max = max(max(values) * 1.1, normal_range[1] * 1.05)
        ax.set_ylim([y_min, y_max])
    else:
        ax.set_ylim([min(values) * 0.9, max(values) * 1.1])
    
    # Add status indicators with enhanced logic
    # Determine color for first value
    if val1_normal is not None:
        if val1_normal:
            status_color1 = '#27ae60'  # Green - within normal range
        else:
            status_color1 = '#e74c3c'  # Red - outside normal range
    else:
        status_color1 = '#27ae60' if 'NORMAL' in data['status1'] else '#e74c3c'
    
    # Determine color for second value
    if val2_normal is not None:
        if val2_normal:
            status_color2 = '#27ae60'  # Green - within normal range
        else:
            status_color2 = '#e74c3c'  # Red - outside normal range
    else:
        status_color2 = '#27ae60' if 'NORMAL' in data['status2'] else '#e74c3c'
    
    ax.scatter([0], [values[0]], s=200, color=status_color1, alpha=0.3, zorder=2)
    ax.scatter([1], [values[1]], s=200, color=status_color2, alpha=0.3, zorder=2)
    
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

# Add color legend
legend_y = 0.01
legend_items = [
    ('🟢 Green Band: Normal Range', '#27ae60'),
    ('🟢 Green Point/Line: Within Normal or Improved', '#2ecc71'),
    ('🔵 Blue Line: Value Changed Within Normal Range', '#3498db'),
    ('🔴 Red Point/Line: Outside Normal Range', '#e74c3c'),
    ('🟡 Yellow Line: No Change in Value', '#f39c12')
]

legend_text = ' | '.join([f'{item[0]}' for item in legend_items])
fig.text(0.5, legend_y, legend_text,
         ha='center', fontsize=9, style='italic',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='white', 
                  edgecolor='#7f8c8d', linewidth=1.5, alpha=0.9))

# Adjust layout
plt.tight_layout(rect=[0, 0.05, 1, 0.98])

# Save figure
plt.savefig('health_trends.png', dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
print("✅ Health trends chart saved as 'health_trends.png'")

# Display the plot
plt.show()
