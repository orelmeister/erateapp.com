import glob
import re

author_bio = '''
        <div class="author-bio" style="margin-top: 3rem; padding: 2rem; background: #f8fafc; border-radius: 12px; display: flex; gap: 1.5rem; align-items: center; border-left: 4px solid #1976d2;">
            <div style="flex: 1;">
                <h4 style="margin-bottom: 0.5rem; font-size: 1.25rem; color: #1e293b;">Written by Jennifer Martinez</h4>
                <p style="color: #1976d2; font-weight: 600; font-size: 0.9rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.5px;">E-Rate Consultant</p>
                <p style="color: #475569; font-size: 1rem; line-height: 1.6; margin-bottom: 0;">Jennifer is a senior E-Rate consultant at erateapp with over a decade of experience helping K-12 schools and libraries secure millions in federal technology funding. She specializes in competitive bidding compliance and PIA review strategies.</p>
            </div>
        </div>
'''

for filepath in glob.glob(r'c:\Users\orelm\OneDrive\Documents\GitHub\Skyrate-Super-Project\erateapp.com\blog\*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'Jennifer Martinez' in content:
        continue
        
    # Replace author in schema
    content = re.sub(
        r'"author":\s*{\s*"@type":\s*"Organization",\s*"name":\s*"erateapp",\s*"legalName":\s*"SkyRate LLC"\s*}',
        r'"author": { "@type": "Person", "name": "Jennifer Martinez", "jobTitle": "E-Rate Consultant" }',
        content
    )
    
    # Inject author bio before </div></article>
    content = content.replace('</div></article>', author_bio + '\n    </div></article>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {filepath}')
