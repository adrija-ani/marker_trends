import json
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import seaborn as sns
from datetime import datetime

class HealthRadarChart:
    def __init__(self, json_file_path):
        """Initialize with JSON file path"""
        self.json_file_path = json_file_path
        self.data = None
        self.health_categories = {
            'Blood Health': [],
            'Metabolic Health': [],
            'Immune Function': [],
            'Kidney Function': [],
            'Liver Health': [],
            'Inflammation': []
        }
        self.load_data()
    
    def load_data(self):
        """Load JSON data from file"""
        try:
            with open(self.json_file_path, 'r') as file:
                self.data = json.load(file)
            print(f"✓ Successfully loaded data for {self.data['patient_info']['name']}")
        except FileNotFoundError:
            print(f"Error: File '{self.json_file_path}' not found!")
            return False
        except json.JSONDecodeError:
            print("Error: Invalid JSON file!")
            return False
        return True
    
    def calculate_test_score(self, test):
        """Calculate individual test score (0-100)"""
        status = test.get('status', 'NORMAL')
        
        if status == 'NORMAL':
            return 100
        elif status in ['HIGH', 'LOW']:
            return 70
        elif status == 'ABNORMAL':
            return 40
        else:
            return 50
    
    def categorize_tests(self):
        """Categorize tests into health categories"""
        if not self.data:
            return
        
        tests = self.data.get('tests', [])
        
        for test in tests:
            name_lower = test['name'].lower()
            score = self.calculate_test_score(test)
            test_info = {
                'name': test['name'],
                'value': test['value'],
                'unit': test.get('unit', ''),
                'status': test.get('status', 'NORMAL'),
                'score': score
            }
            
            # Categorize based on test name
            if any(keyword in name_lower for keyword in ['hemoglobin', 'rbc', 'hct', 'mcv', 'mch', 'platelet', 'rdw']):
                self.health_categories['Blood Health'].append(test_info)
            
            elif any(keyword in name_lower for keyword in ['glucose', 'hba1c', 'sugar', 'mean blood glucose']):
                self.health_categories['Metabolic Health'].append(test_info)
            
            elif any(keyword in name_lower for keyword in ['wbc', 'lymphocyte', 'polymorphs', 'eosinophil', 'monocyte', 'basophil', 'hiv', 'hbsag']):
                self.health_categories['Immune Function'].append(test_info)
            
            elif any(keyword in name_lower for keyword in ['urine', 'protein', 'creatinine', 'urea', 'kidney']):
                self.health_categories['Kidney Function'].append(test_info)
            
            elif any(keyword in name_lower for keyword in ['bile', 'bilirubin', 'alt', 'ast', 'liver', 'sgpt', 'sgot']):
                self.health_categories['Liver Health'].append(test_info)
            
            elif any(keyword in name_lower for keyword in ['esr', 'crp', 'inflammation']):
                self.health_categories['Inflammation'].append(test_info)
    
    def calculate_category_scores(self):
        """Calculate average scores for each category"""
        category_scores = {}
        
        for category, tests in self.health_categories.items():
            if tests:
                avg_score = sum(test['score'] for test in tests) / len(tests)
                category_scores[category] = round(avg_score, 1)
            else:
                category_scores[category] = 0
        
        return category_scores
    
    def calculate_overall_health_score(self, category_scores):
        """Calculate overall health score out of 100"""
        valid_scores = [score for score in category_scores.values() if score > 0]
        
        if valid_scores:
            overall_score = round(sum(valid_scores) / len(valid_scores), 1)
        else:
            overall_score = 0
        
        return overall_score
    
    def get_health_condition(self, score):
        """Determine health condition based on score"""
        if score >= 90:
            return "Excellent", "green"
        elif score >= 75:
            return "Good", "blue"
        elif score >= 60:
            return "Fair", "orange"
        else:
            return "Needs Attention", "red"
    
    def print_chart_explanation(self):
        """Print explanation about the radar chart"""
        explanation = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                      HEALTH BALANCE RADAR CHART EXPLANATION                    ║
╚════════════════════════════════════════════════════════════════════════════════╝

WHAT IS A RADAR CHART?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A radar chart (also called a spider chart) provides a visual representation of 
your health across multiple dimensions. Each axis represents a different health 
category, making it easy to see your overall wellness profile at a glance.

HOW TO READ THE CHART:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• CENTER (0) = Poor health in that category
• OUTER EDGE (100) = Optimal health in that category
• BLUE FILLED AREA = Your current health scores
• GREEN DASHED LINE = Optimal healthy range (target)
• LARGER BLUE AREA = Better overall health

HEALTH CATEGORIES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Blood Health: Red blood cells, hemoglobin, platelets
2. Metabolic Health: Blood sugar, glucose levels
3. Immune Function: White blood cells, infection markers
4. Kidney Function: Urine tests, filtration markers
5. Liver Health: Liver enzymes, bile function
6. Inflammation: ESR, inflammatory markers

SCORING SYSTEM:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 100 points = Test result is NORMAL (within healthy range)
• 70 points = Test result is HIGH or LOW (slightly outside range)
• 40 points = Test result is ABNORMAL (significantly outside range)

Each category score is the average of all tests in that category.
Your overall health score is the average of all category scores.

HEALTH CONDITION RATINGS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 90-100: EXCELLENT - Maintain your healthy lifestyle
• 75-89:  GOOD - Minor improvements recommended
• 60-74:  FAIR - Several areas need attention
• <60:    NEEDS ATTENTION - Consult healthcare provider

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        print(explanation)
    
    def create_radar_chart(self, category_scores, overall_score):
        """Create the radar chart visualization"""
        # Filter out categories with 0 scores
        active_categories = {k: v for k, v in category_scores.items() if v > 0}
        
        if not active_categories:
            print("No valid categories to plot!")
            return
        
        categories = list(active_categories.keys())
        values = list(active_categories.values())
        
        # Number of variables
        N = len(categories)
        
        # Compute angle for each axis
        angles = [n / float(N) * 2 * pi for n in range(N)]
        values += values[:1]  # Complete the circle
        angles += angles[:1]
        
        # Create figure with larger size
        fig = plt.figure(figsize=(20, 14))
        
        # Create grid spec: 4 rows, 2 columns for better spacing
        gs = fig.add_gridspec(4, 2, height_ratios=[0.3, 0.8, 0.1, 1.3], width_ratios=[1.2, 1], 
                             hspace=0.25, wspace=0.2, left=0.05, right=0.97, top=0.95, bottom=0.03)
        
        # Patient Info
        patient_info = self.data['patient_info']
        
        # Get abnormal tests
        abnormal_tests = [test for test in self.data['tests'] 
                         if test.get('status') in ['ABNORMAL', 'HIGH', 'LOW']]
        normal_tests = [test for test in self.data['tests'] 
                       if test.get('status') == 'NORMAL']
        
        # Overall title at top
        fig.suptitle(f'Health Balance Report - {patient_info["name"]}', 
                    fontsize=18, weight='bold')
        
        # TOP RIGHT - OVERALL HEALTH SCORE
        ax_score = fig.add_subplot(gs[0, 1])
        ax_score.axis('off')
        
        condition, color = self.get_health_condition(overall_score)
        
        # Color mapping
        score_colors = {
            'green': '#d4edda',
            'blue': '#cce5ff',
            'orange': '#fff3cd',
            'red': '#f8d7da'
        }
        edge_colors = {
            'green': '#28a745',
            'blue': '#007bff',
            'orange': '#ffc107',
            'red': '#dc3545'
        }
        
        score_text = f"""OVERALL HEALTH SCORE

{overall_score}/100

{condition}"""
        
        ax_score.text(0.5, 0.5, score_text, transform=ax_score.transAxes, 
                     fontsize=11, weight='bold', ha='center', va='center',
                     bbox=dict(boxstyle='round,pad=0.8', facecolor=score_colors[color], 
                              edgecolor=edge_colors[color], linewidth=3))
        
        # LEFT SIDE - RADAR CHART (spanning rows 0-3 on left)
        ax_radar = fig.add_subplot(gs[0:4, 0], polar=True)
        
        # Draw one axis per variable and add labels
        plt.xticks(angles[:-1], categories, size=11, weight='bold')
        
        # Draw ylabels
        ax_radar.set_rlabel_position(0)
        plt.yticks([25, 50, 75, 100], ["25", "50", "75", "100"], color="grey", size=9)
        plt.ylim(0, 100)
        
        # Plot data - Your health score (solid line)
        ax_radar.plot(angles, values, linewidth=2.5, linestyle='solid', color='#3b82f6', 
                     label='Your Health', marker='o', markersize=6)
        ax_radar.fill(angles, values, color='#3b82f6', alpha=0.3)
        
        # Plot optimal range (dashed line)
        optimal_values = [100] * (N + 1)
        ax_radar.plot(angles, optimal_values, linewidth=2, linestyle='--', 
                     color='#10b981', label='Optimal', alpha=0.7)
        ax_radar.fill(angles, optimal_values, color='#10b981', alpha=0.08)
        
        # Add legend at upper right to avoid overlap
        legend = ax_radar.legend(loc='upper right', bbox_to_anchor=(1.12, 1.05), fontsize=10, framealpha=0.9)
        legend.get_frame().set_facecolor('white')
        legend.get_frame().set_edgecolor('gray')
        
        # MIDDLE RIGHT - PATIENT DETAILS BOX
        ax_patient = fig.add_subplot(gs[1, 1])
        ax_patient.axis('off')
        
        patient_text = f"""PATIENT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {patient_info['name']}
Age: {patient_info['age']} | Sex: {patient_info['sex']}
Lab: {patient_info['lab_name']}
Registration: {patient_info['registration_number']}

CATEGORY SCORES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        for cat, score in active_categories.items():
            bar = "█" * int(score/10) + "░" * (10 - int(score/10))
            patient_text += f"{cat[:20]:20s} [{bar}] {score}\n"
        
        patient_text += f"""
TEST SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Tests: {len(self.data['tests'])}
✓ Normal: {len(normal_tests)}
⚠ Attention Required: {len(abnormal_tests)}

RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        if overall_score >= 90:
            patient_text += "• Maintain healthy lifestyle\n• Continue regular check-ups"
        elif overall_score >= 75:
            patient_text += "• Minor improvements needed\n• Monitor abnormal parameters"
        elif overall_score >= 60:
            patient_text += "• Several areas need attention\n• Consult healthcare provider"
        else:
            patient_text += "• Multiple parameters outside range\n• Immediate medical consultation needed"
        
        ax_patient.text(0.05, 0.98, patient_text, transform=ax_patient.transAxes, 
                       fontsize=8.5, verticalalignment='top', fontfamily='monospace',
                       bbox=dict(boxstyle='round,pad=0.6', facecolor='#e8f4f8', alpha=0.7, 
                                edgecolor='#5dade2', linewidth=2))
        
        # BOTTOM RIGHT - TESTS REQUIRING ATTENTION BOX
        ax_tests = fig.add_subplot(gs[3, 1])
        ax_tests.axis('off')
        
        if abnormal_tests:
            # Create a text box for abnormal tests
            tests_text = "⚠️  TESTS REQUIRING IMMEDIATE ATTENTION ⚠️\n"
            tests_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            for i, test in enumerate(abnormal_tests[:6], 1):  # Show up to 6 tests
                status_symbol = "🔴" if test.get('status') == 'ABNORMAL' else "🟡"
                tests_text += f"{status_symbol} {i}. {test['name']}\n"
                tests_text += f"   Value: {test['value']} {test.get('unit', '')} ({test.get('status')})\n"
                
                # Add meaning if available
                if test.get('meaning'):
                    meaning = test['meaning'][:70] + "..." if len(test['meaning']) > 70 else test['meaning']
                    tests_text += f"   ℹ️  {meaning}\n"
                
                # Add tips if available
                if test.get('tips'):
                    tips = test['tips'][:70] + "..." if len(test['tips']) > 70 else test['tips']
                    tests_text += f"   💡 {tips}\n"
                tests_text += "\n"
            
            if len(abnormal_tests) > 6:
                tests_text += f"... and {len(abnormal_tests) - 6} more tests requiring attention\n"
            
            tests_text += "\n⚠️  Please consult your healthcare provider immediately ⚠️"
            
            # Larger highlighted box with red background
            ax_tests.text(0.05, 0.98, tests_text, transform=ax_tests.transAxes, 
                         fontsize=8.5, verticalalignment='top', fontfamily='monospace',
                         bbox=dict(boxstyle='round,pad=0.6', facecolor='#ffe6e6', alpha=0.95, 
                                  edgecolor='#dc3545', linewidth=3))
        else:
            tests_text = "✅ EXCELLENT NEWS! ✅\n"
            tests_text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            tests_text += "All your test results are within the normal healthy range!\n\n"
            tests_text += "This is a great sign of overall good health. Keep maintaining your\n"
            tests_text += "current lifestyle and continue with:\n\n"
            tests_text += "• Balanced and nutritious diet\n"
            tests_text += "• Regular physical exercise (at least 30 mins daily)\n"
            tests_text += "• Adequate sleep (7-8 hours)\n"
            tests_text += "• Stress management and mental wellness\n"
            tests_text += "• Regular health check-ups\n"
            tests_text += "• Stay hydrated and avoid harmful substances\n"
            
            ax_tests.text(0.05, 0.98, tests_text, transform=ax_tests.transAxes, 
                         fontsize=9, verticalalignment='top', fontfamily='monospace',
                         bbox=dict(boxstyle='round,pad=0.6', facecolor='#e6ffe6', alpha=0.95, 
                                  edgecolor='#28a745', linewidth=3))
        
        # Save with fixed filename
        filename = "health_radar.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Chart saved as '{filename}'")
        
        # Show the plot
        plt.show()
    
    def generate_detailed_report(self):
        """Generate a detailed text report"""
        if not self.data:
            return
        
        print("\n" + "="*80)
        print(f"DETAILED HEALTH REPORT - {self.data['patient_info']['name']}")
        print("="*80)
        
        # Calculate scores
        category_scores = self.calculate_category_scores()
        overall_score = self.calculate_overall_health_score(category_scores)
        condition, color = self.get_health_condition(overall_score)
        
        print(f"\nOVERALL HEALTH SCORE: {overall_score}/100 - {condition}")
        print("-"*80)
        
        # Category breakdown
        print("\nCATEGORY BREAKDOWN:")
        for category, score in category_scores.items():
            if score > 0:
                bar = "█" * int(score/5) + "░" * (20 - int(score/5))
                print(f"{category:20s}: [{bar}] {score}/100")
        
        # Abnormal tests - HIGHLIGHTED
        abnormal_tests = [test for test in self.data['tests'] 
                         if test.get('status') in ['ABNORMAL', 'HIGH', 'LOW']]
        
        if abnormal_tests:
            print("\n" + "="*80)
            print("⚠️  TESTS REQUIRING IMMEDIATE ATTENTION ⚠️")
            print("="*80)
            for i, test in enumerate(abnormal_tests, 1):
                print(f"\n{i}. {test['name']}:")
                print(f"   Value: {test['value']} {test.get('unit', '')}")
                print(f"   Status: *** {test.get('status')} ***")
                print(f"   Meaning: {test.get('meaning', 'N/A')}")
                print(f"   Recommendation: {test.get('tips', 'Consult your healthcare provider')}")
                print("-"*80)
        
        print("\n" + "="*80 + "\n")
    
    def generate_report(self):
        """Main method to generate complete health report"""
        if not self.data:
            print("Error: No data loaded!")
            return
        
        # Print explanation first
        self.print_chart_explanation()
        
        print("\nGenerating Health Balance Radar Chart...\n")
        
        # Categorize tests
        self.categorize_tests()
        
        # Calculate scores
        category_scores = self.calculate_category_scores()
        overall_score = self.calculate_overall_health_score(category_scores)
        
        # Generate detailed text report
        self.generate_detailed_report()
        
        # Create visualization
        self.create_radar_chart(category_scores, overall_score)


# Example usage
if __name__ == "__main__":
    # Initialize with your JSON file
    json_file = "health_report_data.json"
    
    print("="*80)
    print("HEALTH BALANCE RADAR CHART GENERATOR")
    print("="*80)
    
    # Create health radar chart
    health_chart = HealthRadarChart(json_file)
    
    # Generate complete report with visualization
    health_chart.generate_report()
    
    print("\n✓ Health report generation complete!")
    print("✓ Chart saved as 'health_radar.png'")
