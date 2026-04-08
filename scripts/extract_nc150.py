import asyncio
import json
import sys
from playwright.async_api import async_playwright

async def extract_neetcode_150():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Navigating to NeetCode 150...")
        await page.goto("https://neetcode.io/practice")
        
        # Click the NeetCode 150 tab
        # The tabs are usually identified by text or index.
        # Based on previous research, it's the second tab.
        await page.click("text=NeetCode 150")
        
        print("Expanding categories...")
        # Expand all accordion buttons
        accordions = await page.query_selector_all("button.accordion")
        for acc in accordions:
            is_active = await acc.evaluate("el => el.classList.contains('active')")
            if not is_active:
                await acc.click()
        
        # Wait a moment for expansion
        await asyncio.sleep(1)
        
        print("Extracting problems...")
        # Extract data using the same logic we verified
        data = await page.evaluate('''() => {
            const results = [];
            const accordions = Array.from(document.querySelectorAll('button.accordion'));
            
            accordions.forEach((acc, index) => {
                const category = acc.querySelector('p').innerText.trim();
                const container = acc.nextElementSibling;
                if (!container) return;
                
                const problemLinks = Array.from(container.querySelectorAll('a.table-text'));
                problemLinks.forEach((link, rowIdx) => {
                    const row = link.closest('tr');
                    if (!row) return;
                    
                    const leetcodeLink = row.querySelector('a[href*="leetcode.com"]');
                    const diffBtn = row.querySelector('#diff-btn');
                    
                    if (leetcodeLink && diffBtn) {
                        results.push({
                            "file_name": `NC150 - ${link.innerText.trim()}`,
                            "title": link.innerText.trim(),
                            "category": category,
                            "difficulty": diffBtn.innerText.trim(),
                            "leetcode_url": leetcodeLink.href,
                            "neetcode_url": "https://neetcode.io" + link.getAttribute('href'),
                            "base": "[[NeetCode 150.base]]",
                            "concepts": []
                        });
                    }
                });
            });
            return results;
        }''')

        await browser.close()
        return data

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    problems = loop.run_until_complete(extract_neetcode_150())
    
    output_file = "data/NC150.json"
    with open(output_file, "w") as f:
        json.dump(problems, f, indent=2)
    
    print(f"Successfully extracted {len(problems)} problems to {output_file}")
