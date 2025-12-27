# Render project YAMLs to HTML pages and an index
import os
import yaml
from jinja2 import Environment, FileSystemLoader
import markdown as md
from typing import List, Any
import re

PROJECTS_DIR = '.'
OUTPUT_DIR = '..'
PROJECT_TEMPLATE = 'project_template.html'
INDEX_TEMPLATE = 'projects_index_template.html'

def load_projects() -> List[Any]:
    projects: List[Any] = []
    for fname in os.listdir(PROJECTS_DIR):
        if fname.endswith('.yml') and fname != "template.yml":
            with open(os.path.join(PROJECTS_DIR, fname), 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                # Render markdown fields to HTML
                for field in ['summary_md', 'details_md']:
                    if field in data:
                        html = md.markdown(data[field])
                        # Wrap h3 with box class div
                        pattern = re.compile(
                            r'(<h3.*?>.*?</h3>)(.*?)(?=(<h[123][^>]*?>|<hr\b|$))',
                            re.DOTALL | re.IGNORECASE
                        )
                        html = re.sub(pattern, r'<div class="box">\1\2</div>', html)
                        data[field.replace('_md', '_html')] = html
                    else:
                        data[field.replace('_md', '_html')] = ''
                # Fallbacks
                data['summary'] = data.get('summary_md', '').split('\n')[0]
                # Output page name
                data['page'] = f"project_{data['id']}.html"
                projects.append(data)
    return projects

def render():
    env = Environment(loader=FileSystemLoader(PROJECTS_DIR))
    project_template = env.get_template(PROJECT_TEMPLATE)
    index_template = env.get_template(INDEX_TEMPLATE)
    projects = load_projects()
    # Render each project page
    for project in projects:
        html = project_template.render(project=project)
        with open(os.path.join(OUTPUT_DIR, project['page']), 'w', encoding='utf-8') as f:
            f.write(html)
    # Render index
    index_html = index_template.render(projects=projects)
    with open(os.path.join(OUTPUT_DIR, 'projects.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"Rendered {len(projects)} projects and index.")

if __name__ == '__main__':
    render()
