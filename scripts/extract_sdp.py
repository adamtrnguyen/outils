import requests
import re
import json

def extract_system_design_primer():
    url = "https://raw.githubusercontent.com/donnemartin/system-design-primer/master/README.md"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch README: {response.status_code}")
        return []

    content = response.text
    
    # 1. Extract the Table of Contents section
    # Usually between "## Index of system design topics" and the next "##"
    toc_start = content.find("* [Performance vs scalability]")
    if toc_start == -1:
        # Fallback to general list search if the specific text changed
        toc_start = content.find("* [")
        
    toc_end = content.find("## Study guide", toc_start)
    if toc_end == -1:
        toc_end = content.find("##", toc_start + 10)
        
    toc_text = content[toc_start:toc_end]
    
    results = []
    base_url = "https://github.com/donnemartin/system-design-primer/blob/master/README.md"
    
    current_category = "General"
    
    # Simple regex for markdown list items: * [Title](#anchor)
    # We also track indentation to determine if it's a sub-topic
    lines = toc_text.split('\n')
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith('* ['):
            continue
            
        match = re.search(r"\* \[(.*?)\]\((.*?)\)", line)
        if not match:
            continue
            
        title = match.group(1)
        anchor = match.group(2)
        
        # Determine if it's a top level category (no leading spaces)
        is_top_level = not line.startswith(' ') and not line.startswith('\t')
        
        if is_top_level:
            current_category = title
            # We skip adding the category as its own item if we want more granularity, 
            # but usually it's good to have it too.
            # Let's add it.
        
        full_url = anchor if anchor.startswith('http') else base_url + anchor
        
        results.append({
            "file_name": f"SDP - {title}",
            "title": title,
            "chapter": "System Design Concepts",
            "category": current_category,
            "url": full_url,
            "base": "[[System Design Primer.base]]",
            "concepts": []
        })

    # 2. Extract Question Tables
    # System Design Questions
    sd_pos = content.find("## System design interview questions with solutions")
    if sd_pos != -1:
        table_start = content.find("| Question | |", sd_pos)
        if table_start != -1:
            table_end = content.find("\n\n", table_start + 20)
            table_lines = content[table_start:table_end].strip().split('\n')
            for line in table_lines[2:]:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    q = parts[1]
                    if "Add a system design question" in q or "Contribute" in parts[2]: continue
                    link_match = re.search(r"\[Solution\]\((.*?)\)", parts[2])
                    link = link_match.group(1) if link_match else ""
                    sol_url = link if link.startswith('http') else "https://github.com/donnemartin/system-design-primer/blob/master/" + link
                    
                    results.append({
                        "file_name": f"SDP - Question - {q}",
                        "title": q,
                        "chapter": "Interview Questions",
                        "category": "System Design",
                        "url": sol_url,
                        "base": "[[System Design Primer.base]]",
                        "concepts": []
                    })

    # Object-Oriented Design Questions
    ood_pos = content.find("## Object-oriented design interview questions with solutions")
    if ood_pos != -1:
        table_start = content.find("| Question | |", ood_pos)
        if table_start != -1:
            table_end = content.find("\n\n", table_start + 20)
            table_lines = content[table_start:table_end].strip().split('\n')
            for line in table_lines[2:]:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:
                    q = parts[1]
                    if "Add an object-oriented design question" in q or "Contribute" in parts[2]: continue
                    link_match = re.search(r"\[Solution\]\((.*?)\)", parts[2])
                    link = link_match.group(1) if link_match else ""
                    sol_url = link if link.startswith('http') else "https://github.com/donnemartin/system-design-primer/blob/master/" + link
                    
                    results.append({
                        "file_name": f"SDP - OOD - {q}",
                        "title": q,
                        "chapter": "Interview Questions",
                        "category": "Object Oriented Design",
                        "url": sol_url,
                        "base": "[[System Design Primer.base]]",
                        "concepts": []
                    })

    return results

if __name__ == "__main__":
    problems = extract_system_design_primer()
    output_file = "data/SDP.json"
    with open(output_file, "w") as f:
        json.dump(problems, f, indent=2)
    print(f"Successfully extracted {len(problems)} problems to {output_file}")
