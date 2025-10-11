import json
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np
from datetime import datetime

def calculate_health_score(tests):
    """Calculate overall health score based on test results"""
    total_tests = len([t for t in tests if t.get('status') is not None])
    normal_tests = sum(1 for test in tests if test.get('status') == 'NORMAL')
    score = (normal_tests / total_tests) * 100 if total_tests > 0 else 0
    return round(score, 1)

def get_bar_color(value, normal_min, normal_max):
    """Get intelligent color for bar based on value position"""
    try:
        val = float(value)
        min_val = float(normal_min)
        max_val = float(normal_max)
        
        if val < min_val:
            return '#f39c12'  # Orange for low
        elif val > max_val:
            return '#e74c3c'  # Red for high
        else:
            return '#27ae60'  # Green for normal
    except:
        return '#95a5a6'

def parse_numeric_value(value_str):
    """Parse numeric value from string"""
    try:
        if isinstance(value_str, (int, float)):
            return float(value_str)
        cleaned = ''.join(c for c in str(value_str) if c.isdigit() or c in '.-')
        return float(cleaned) if cleaned and cleaned not in ['.', '-', ''] else None
    except:
        return None

def create_blood_panel_report(json_file_path, output_file='health_blood.png'):
    """Generate professional blood panel report"""
    
    # Load JSON data
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    patient_info = data.get('patient_info', {})
    tests = data.get('tests', [])
    
    # Calculate health score
    health_score = calculate_health_score(tests)
    
    # Categorize tests
    hematology_keywords = ['hemoglobin', 'rbc', 'h.ct', 'hct', 'mcv', 'mch', 'rdw', 
                           'wbc', 'tlc', 'platelet', 'esr', 'glucose', 'hbsag', 'hiv']
    differential_keywords = ['polymorph', 'lymphocyte', 'eosinophil', 'monocyte', 'basophil']
    
    hematology_tests = []
    differential_tests = []
    urine_tests = []
    
    for test in tests:
        name_lower = test.get('name', '').lower()
        if any(kw in name_lower for kw in hematology_keywords):
            hematology_tests.append(test)
        elif any(kw in name_lower for kw in differential_keywords):
            differential_tests.append(test)
        elif 'urine' in name_lower or any(x in name_lower for x in 
            ['bile', 'pus', 'epithelial', 'cast', 'fungus', 'crystal', 'bacteria', 
             'specific gravity', 'volume', 'colour', 'appearance', 'reaction']):
            urine_tests.append(test)
    
    # Create figure with light gray background
    fig, ax = plt.subplots(figsize=(18, 12), facecolor='#e8e8e8')
    
    # Remove default axes
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # White content box background
    white_box = FancyBboxPatch((2, 2), 96, 96, 
                               boxstyle="round,pad=1", 
                               facecolor='white', 
                               edgecolor='#d0d0d0', 
                               linewidth=2,
                               zorder=1)
    ax.add_patch(white_box)
    
    # Title
    ax.text(50, 96.5, 'Detailed Blood Panel & Urine Analysis Report', 
           ha='center', fontsize=24, fontweight='bold', family='sans-serif', zorder=10)
    ax.text(50, 93.5, datetime.now().strftime('%B %d, %Y'), 
           ha='center', fontsize=12, color='#666', zorder=10)
    
    # Overall Health Score Box
    score_color = '#27ae60' if health_score >= 80 else '#f39c12' if health_score >= 60 else '#e74c3c'
    score_box = FancyBboxPatch((40, 88.5), 20, 4, 
                              boxstyle="round,pad=0.3",
                              facecolor=score_color, 
                              edgecolor='none',
                              alpha=0.2,
                              zorder=5)
    ax.add_patch(score_box)
    ax.text(50, 91, f'Overall Health Score: {health_score}%', 
           ha='center', fontsize=13, fontweight='bold', color=score_color, zorder=10)
    
    # Section headers
    ax.text(8, 84, 'Hematology & Chemistry Results', 
           fontsize=14, fontweight='bold', zorder=10)
    ax.text(56, 84, 'Differential & Urine Analysis', 
           fontsize=14, fontweight='bold', zorder=10)
    
    # Left section - Hematology tests with bar charts
    y_pos = 79
    bar_width = 18
    bar_height = 2.2
    
    for test in hematology_tests[:13]:
        name = test.get('name', '')
        value = test.get('value', '')
        unit = test.get('unit', '').strip()
        status = test.get('status', 'NORMAL')
        
        # Get ranges
        ranges = test.get('ranges', {})
        ref_range = test.get('reference_range', '')
        
        if ranges:
            normal_min = ranges.get('normal_min', 0)
            normal_max = ranges.get('normal_max', 100)
        elif ref_range:
            try:
                ref_clean = ref_range.strip().replace('\n', '')
                parts = ref_clean.split('-')
                if len(parts) >= 2:
                    normal_min = float(parts[0].strip())
                    normal_max = float(parts[1].strip())
                else:
                    normal_min, normal_max = 0, 100
            except:
                normal_min, normal_max = 0, 100
        else:
            normal_min, normal_max = 0, 100
        
        # Shorten name for display
        display_name = name[:28] if len(name) > 28 else name
        
        # Test name (right-aligned)
        ax.text(26, y_pos, display_name, 
               fontsize=9.5, ha='right', va='center', zorder=10)
        
        # Draw bar chart background (gray)
        bg_bar = Rectangle((28, y_pos - bar_height/2), bar_width, bar_height, 
                          facecolor='#e8e8e8', edgecolor='#d0d0d0', 
                          linewidth=0.5, zorder=5)
        ax.add_patch(bg_bar)
        
        # Draw filled bar based on value
        val_numeric = parse_numeric_value(value)
        if val_numeric is not None and normal_min != normal_max:
            try:
                range_val = normal_max - normal_min
                
                # Calculate fill percentage
                if val_numeric <= normal_max:
                    fill_ratio = (val_numeric - normal_min) / range_val
                else:
                    # Extend beyond for high values
                    fill_ratio = 1 + ((val_numeric - normal_max) / range_val) * 0.25
                
                fill_ratio = max(0, min(fill_ratio, 1.2))
                fill_width = bar_width * fill_ratio
                
                # Get color
                bar_color = get_bar_color(val_numeric, normal_min, normal_max)
                
                # Draw filled portion
                filled_bar = Rectangle((28, y_pos - bar_height/2), fill_width, bar_height, 
                                      facecolor=bar_color, edgecolor='none', zorder=6)
                ax.add_patch(filled_bar)
            except:
                pass
        
        # Value text with color based on status
        value_color = '#e74c3c' if status in ['HIGH', 'LOW', 'ABNORMAL'] else '#27ae60'
        ax.text(47, y_pos, str(value), 
               fontsize=10, va='center', fontweight='bold', color=value_color, zorder=10)
        
        # Normal range text (smaller, gray)
        range_text = f"{normal_min}-{normal_max}"
        ax.text(51, y_pos, range_text, 
               fontsize=7.5, va='center', color='#888', zorder=10)
        
        # Status (HIGH/LOW) - moved further right
        if status == 'HIGH':
            ax.text(58, y_pos, 'HIGH', 
                   fontsize=8, color='#e74c3c', fontweight='bold', va='center', zorder=10)
        elif status == 'LOW':
            ax.text(58, y_pos, 'LOW', 
                   fontsize=8, color='#f39c12', fontweight='bold', va='center', zorder=10)
        
        y_pos -= 5.2
    
    # Right section - Differential tests
    y_pos = 79
    diff_x = 62
    
    # Differential table header
    ax.text(diff_x, y_pos, 'Polymorphs (%)', fontsize=9.5, zorder=10)
    ax.text(diff_x + 20, y_pos, '4.0-10.0', fontsize=9.5, color='#666', zorder=10)
    
    y_pos -= 3.5
    ax.text(diff_x, y_pos, 'Lymphocytes (%)', fontsize=9.5, zorder=10)
    ax.text(diff_x + 15, y_pos, 'Eosinophils (%)', fontsize=9.5, zorder=10)
    
    # Find lymphocytes value
    for test in differential_tests:
        if 'lymphocyte' in test.get('name', '').lower():
            value = test.get('value', '')
            status = test.get('status', 'NORMAL')
            if status == 'HIGH':
                ax.text(diff_x + 30, y_pos, f"{value} HIGH", 
                       fontsize=9.5, color='#e74c3c', fontweight='bold', zorder=10)
            else:
                ax.text(diff_x + 30, y_pos, str(value), fontsize=9.5, zorder=10)
    
    y_pos -= 3.5
    ax.text(diff_x, y_pos, 'Monocytes (%)', fontsize=9.5, zorder=10)
    ax.text(diff_x + 15, y_pos, 'Monocytes (%)', fontsize=9.5, zorder=10)
    
    y_pos -= 3.5
    ax.text(diff_x, y_pos, 'Baseln (%)', fontsize=9.5, zorder=10)
    
    # Urine Analysis section
    y_pos -= 6
    ax.text(diff_x, y_pos, 'Urine Analysis', 
           fontsize=13, fontweight='bold', zorder=10)
    
    # Urine table
    y_pos -= 5
    urine_data = [
        ['Volume', 'Colour', 'Appearance'],
        ['Reaction', 'Specific Gravity', 'Bile Salts'],
        ['Protein', 'Bile Pigments', ''],
        ['Red Cells', 'NIL', ''],
        ['Fungus', 'Present (++)', ''],
        ['Crystals', 'Bacteria', '']
    ]
    
    for row in urine_data:
        for i, param in enumerate(row):
            if param:
                x_pos = diff_x + i * 13
                ax.text(x_pos, y_pos, param, fontsize=8.5, zorder=10)
                if i == 2 and param:
                    ax.text(x_pos + 9, y_pos, 'NORMAL', 
                           fontsize=7.5, color='#666', zorder=10)
        y_pos -= 3
    
    # Legend at bottom left
    legend_y = 14
    ax.add_patch(Rectangle((7, legend_y - 0.7), 1.2, 1.2, 
                          facecolor='#3498db', edgecolor='none', zorder=5))
    ax.text(9, legend_y, 'Your Result', fontsize=9.5, va='center', zorder=10)
    
    ax.add_patch(Rectangle((7, legend_y - 3.5), 1.2, 1.2, 
                          facecolor='#27ae60', edgecolor='none', zorder=5))
    ax.text(9, legend_y - 2.8, 'Healthy Reference Range', 
           fontsize=9.5, va='center', zorder=10)
    
    # Warning banner at bottom
    warning_box = FancyBboxPatch((6, 4), 88, 4.5, 
                                boxstyle="round,pad=0.4",
                                facecolor='#e74c3c', edgecolor='none', zorder=5)
    ax.add_patch(warning_box)
    
    ax.text(50, 6.8, 
           'IMPORTANT: Several results are HIGH. Consult with a physician for accurate interpretation and', 
           ha='center', fontsize=10.5, color='white', fontweight='bold', zorder=10)
    ax.text(50, 5.2, 'recommendations.', 
           ha='center', fontsize=10.5, color='white', fontweight='bold', zorder=10)
    
    # Save with tight layout
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', 
               facecolor='#e8e8e8', edgecolor='none')
    plt.close()
    
    # Print summary
    print(f"✓ Blood panel report saved to: {output_file}")
    print(f"✓ Overall Health Score: {health_score}%")
    
    abnormal = [t for t in tests if t.get('status') in ['HIGH', 'LOW', 'ABNORMAL']]
    if abnormal:
        print(f"\n⚠ ATTENTION REQUIRED - Abnormal Results Found: {len(abnormal)}")
        print("=" * 60)
        for test in abnormal:
            print(f"  ⚠ {test.get('name')}: {test.get('value')} {test.get('unit', '')} [{test.get('status')}]")
        print("=" * 60)
        print("Please consult with a physician for proper interpretation.")
    else:
        print("\n✓ All results within normal range")
    
    return health_score, abnormal

# Usage
if __name__ == "__main__":
    create_blood_panel_report('health_report_data1.json', 'health_blood.png')