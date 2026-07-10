# file: render_links.py
# purpose: Render links from markdown to HTML using Jinja2

from jinja2 import Environment, FileSystemLoader
from typing import List, Dict, Tuple, Any
import re


with open('links.md', 'r', encoding='utf-8') as f:
    markdown = f.readlines()



def parse_markdown(md: List[str]) -> Tuple[str, str, List[Dict[str, Any]]]:
    lines = md #.strip().splitlines()
    title = ""
    description = ""
    categories: List[Dict[str, Any]] = []
    current_category: Dict[str, Any] | None = None
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for i, line in enumerate(lines):
        line = line.rstrip()
        if i == 0 and line.startswith('#'):
            title = line.lstrip('#').strip()
            continue
        if not line.strip():
            continue
        if not title:
            continue
        if not categories and not line.startswith('-'):
            description += line.strip() + ' '
            continue
        if line.startswith('- '):
            cat_name = line[2:].strip()
            current_category = {'name': cat_name, 'links': []}
            categories.append(current_category)
        elif line.lstrip().startswith('- '):
            if not current_category:
                continue

            content = line.lstrip()[2:].strip()
            matches = list(link_pattern.finditer(content))
            if not matches:
                continue

            segments: List[Dict[str, str]] = []
            last_index = 0
            for match in matches:
                prefix = content[last_index:match.start()]
                if prefix:
                    segments.append({'type': 'text', 'value': prefix})
                segments.append({'type': 'link', 'text': match.group(1), 'url': match.group(2)})
                last_index = match.end()

            suffix = content[last_index:]
            if suffix:
                segments.append({'type': 'text', 'value': suffix})

            current_category['links'].append({'segments': segments})
    description = description.strip()
    return title, description, categories

title, description, categories = parse_markdown(markdown)

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('link_template.html')

html = template.render(
    page_title="Interesting Links",
    title=title,
    description=description,
    categories=categories
)

with open('../links.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Rendered to links.html")
