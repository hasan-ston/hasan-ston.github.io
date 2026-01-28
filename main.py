"""
MkDocs Macros plugin hook for loading project data
"""
import json
import os

def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    """

    @env.macro
    def load_projects():
        """Load projects from JSON file"""
        json_path = os.path.join(env.project_dir, 'docs', 'projects.json')
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data['projects']

    @env.macro
    def project_card(project):
        """Generate HTML for a project card"""
        card_html = f"""
<div class="project-card" markdown="1">

### {project['icon']} {project['name']}

**{project['tech']}** | {project['date']}

{project['description']}

"""

        # Add links
        links = []
        if project.get('live'):
            links.append(f"[Live Demo]({project['live']})")
        if project.get('demo_video'):
            links.append(f"[Demo Video]({project['demo_video']})")
        if project.get('github'):
            links.append(f"[GitHub]({project['github']})")

        if links:
            card_html += " | ".join(links) + "\n\n"

        # Add read more link
        if project.get('writeup'):
            card_html += f"[Read more →]({project['writeup']}){{ .md-button }}\n\n"

        card_html += "</div>\n"

        return card_html
