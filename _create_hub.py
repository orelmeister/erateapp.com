import os
import re

template_path = r'c:\Users\orelm\OneDrive\Documents\GitHub\Skyrate-Super-Project\erateapp.com\guides\e-rate-deadlines-2026.html'
new_path = r'c:\Users\orelm\OneDrive\Documents\GitHub\Skyrate-Super-Project\erateapp.com\guides\ultimate-2026-erate-funding-guide.html'

with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'<title>.*?</title>', '<title>The Ultimate 2026 Guide to E-Rate Funding | erateapp</title>', content)
content = re.sub(r'<meta name="description".*?>', '<meta name="description" content="Everything you need to know about E-Rate funding for 2026. The ultimate guide for K-12 schools and libraries.">', content)
content = re.sub(r'<meta property="og:title".*?>', '<meta property="og:title" content="The Ultimate 2026 Guide to E-Rate Funding">', content)
content = re.sub(r'<meta property="og:description".*?>', '<meta property="og:description" content="Everything you need to know about E-Rate funding for 2026. The ultimate guide for K-12 schools and libraries.">', content)
content = content.replace('e-rate-deadlines-2026.html', 'ultimate-2026-erate-funding-guide.html')

content = re.sub(r'<h1>.*?</h1>', '<h1>The Ultimate 2026 Guide to E-Rate Funding</h1>', content)
content = re.sub(r'<p>Complete calendar of FY2026 E-Rate deadlines.*?</p>', '<p>Your central hub for navigating the E-Rate program in 2026. Find all the resources, deadlines, and guides you need to maximize your funding.</p>', content)

with open(new_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Hub page created!")
