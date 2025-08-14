#!/usr/bin/env python3
"""
Clean script to fix all corrupted emoji characters in combined-ui.html
"""

import re

def fix_combined_ui():
    """Fix all encoding issues in combined-ui.html"""
    
    input_file = 'combined-ui.html'
    
    # Read the file
    try:
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        print(f"Original file size: {len(content)} characters")
        
        # Define all corrupted emoji patterns and their replacements
        emoji_fixes = [
            # Static HTML content fixes
            (r'â„¹ï¸', '<i class="fas fa-info-circle text-blue-500"></i>'),
            (r'ðŸŸ¢', '<i class="fas fa-circle text-green-500"></i>'),
            (r'ðŸš€', '<i class="fas fa-rocket"></i>'),
            
            # JavaScript content fixes
            (r"type === 'error' \? 'âŒ' : type === 'success' \? 'âœ…' : type === 'warning' \? 'âš ï¸' : 'â„¹ï¸'", 
             """type === 'error' ? '<i class="fas fa-times-circle text-red-500"></i>' : type === 'success' ? '<i class="fas fa-check-circle text-green-500"></i>' : type === 'warning' ? '<i class="fas fa-exclamation-triangle text-yellow-500"></i>' : '<i class="fas fa-info-circle text-blue-500"></i>'"""),
            
            # Individual character fixes
            (r'âŒ', '<i class="fas fa-times-circle text-red-500"></i>'),
            (r'âœ…', '<i class="fas fa-check-circle text-green-500"></i>'),
            (r'âš ï¸', '<i class="fas fa-exclamation-triangle text-yellow-500"></i>'),
            
            # Additional patterns
            (r'ðŸ"', '<i class="fas fa-search"></i>'),
            (r'ðŸ"Š', '<i class="fas fa-chart-bar"></i>'),
            (r'ðŸŽ¯', '<i class="fas fa-bullseye"></i>'),
            (r'ðŸ"'', '<i class="fas fa-lock"></i>'),
            (r'ðŸ¤–', '<i class="fas fa-robot"></i>'),
            (r'ðŸ›¡ï¸', '<i class="fas fa-shield-alt"></i>'),
        ]
        
        # Apply all fixes
        for pattern, replacement in emoji_fixes:
            old_content = content
            content = re.sub(pattern, replacement, content)
            if content != old_content:
                print(f"✅ Fixed pattern: {pattern[:20]}...")
        
        # Write the fixed content back
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed file saved. New size: {len(content)} characters")
        print("🎉 All emoji encoding issues should now be resolved!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_combined_ui()
