#!/usr/bin/env python3
"""
Script to fix corrupted emoji encoding issues in HTML files
"""

import re

def fix_html_encoding(input_file, output_file):
    """Fix corrupted emoji characters in HTML file"""
    
    # Read file with proper encoding
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Define replacements for corrupted emojis
    replacements = {
        # Corrupted rocket emoji
        'ðŸš€': '<i class="fas fa-rocket"></i>',
        # Corrupted green circle
        'ðŸŸ¢': '<i class="fas fa-circle text-green-500"></i>',
        # Corrupted info emoji  
        'â„¹ï¸': '<i class="fas fa-info-circle text-blue-500"></i>',
        # Corrupted X emoji
        'âŒ': '<i class="fas fa-times-circle text-red-500"></i>',
        # Corrupted check emoji
        'âœ…': '<i class="fas fa-check-circle text-green-500"></i>',
        # Corrupted warning emoji
        'âš ï¸': '<i class="fas fa-exclamation-triangle text-yellow-500"></i>',
        # Alternative corrupted patterns
        'ðŸ'': '<i class="fas fa-thumbs-up text-green-500"></i>',
        'ðŸ"': '<i class="fas fa-search"></i>',
        'ðŸ"Š': '<i class="fas fa-chart-bar"></i>',
        'ðŸŽ¯': '<i class="fas fa-bullseye"></i>',
        'ðŸ"'': '<i class="fas fa-lock"></i>',
        'ðŸ¤–': '<i class="fas fa-robot"></i>',
        'ðŸ›¡ï¸': '<i class="fas fa-shield-alt"></i>',
    }
    
    # Apply replacements
    for corrupted, replacement in replacements.items():
        content = content.replace(corrupted, replacement)
    
    # Write fixed content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed encoding issues in {input_file} -> {output_file}")

if __name__ == "__main__":
    fix_html_encoding('combined-ui.html', 'combined-ui-fixed.html')
