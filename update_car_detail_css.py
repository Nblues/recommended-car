import os
import re
import glob

def update_car_detail_files():
    """Update all car detail HTML files to use shared CSS"""
    
    # Path to car detail directory
    car_detail_dir = "docs/car-detail"
    
    # CSS link to add
    css_link = '<link rel="stylesheet" href="../car-detail-style.css">'
    
    # Minimal critical CSS
    critical_css = '''<style>
    /* Only critical above-the-fold styles */
    body { font-family: 'Prompt', sans-serif; margin: 0; background: #f7f7fb; }
    .container { max-width: 1200px; margin: 0 auto; padding: 1rem; }
    .car-header { background: #fff; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; }
    .car-title { font-size: 2rem; font-weight: 700; color: #2c3e50; }
    .car-price { font-size: 2.5rem; color: #e74c3c; font-weight: 800; }
    img { opacity: 0; transition: opacity 0.3s ease; }
    img.loaded, .main-image img { opacity: 1; }
  </style>'''
    
    # Get all HTML files in car-detail directory
    html_files = glob.glob(os.path.join(car_detail_dir, "*.html"))
    
    print(f"Found {len(html_files)} car detail files to update")
    
    for file_path in html_files:
        try:
            # Skip if it's already been updated
            if "ford-ranger-4dr-dcab-wildtrak-auto-10sp-2wd-2-0-turbo-dct.html" in file_path:
                continue
                
            print(f"Updating: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if already has the CSS link
            if '../car-detail-style.css' in content:
                print(f"  Already updated: {file_path}")
                continue
            
            # Add CSS link after existing CSS links or before </head>
            if '<link rel="stylesheet"' in content:
                # Add after last CSS link
                content = re.sub(
                    r'(<link rel="stylesheet"[^>]*>)',
                    r'\1\n  ' + css_link,
                    content,
                    count=1
                )
            else:
                # Add before </head>
                content = content.replace('</head>', f'  {css_link}\n</head>')
            
            # Remove large inline CSS blocks (keep only critical CSS)
            # Look for large <style> blocks and replace with critical CSS
            content = re.sub(
                r'<style>\s*\/\*[^*]*\*\/.*?<\/style>',
                critical_css,
                content,
                flags=re.DOTALL
            )
            
            # Also handle CSS without comments
            content = re.sub(
                r'<style>\s*body\{font-family.*?<\/style>',
                critical_css,
                content,
                flags=re.DOTALL
            )
            
            # Fix image onerror attributes
            content = re.sub(
                r'<img([^>]*)>',
                r'<img\1 onerror="this.style.display=\'none\'">',
                content
            )
            
            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  Updated successfully: {file_path}")
            
        except Exception as e:
            print(f"  Error updating {file_path}: {e}")

if __name__ == "__main__":
    update_car_detail_files()
    print("Car detail files update completed!")
