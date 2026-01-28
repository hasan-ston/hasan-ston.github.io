# Projects

Here are some things I've built:

<div class="projects-grid" markdown="1">

{% for project in load_projects() %}
{{ project_card(project) }}
{% endfor %}

</div>
