import gitlab
import json
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GITLAB_API_URL = ''
PRIVATE_TOKEN = ''
NEW_PROJECT_ID =

gl = gitlab.Gitlab(GITLAB_API_URL, private_token=PRIVATE_TOKEN)
# gl = gitlab.Gitlab(GITLAB_API_URL, private_token=PRIVATE_TOKEN, ssl_verify=False)

gl.auth()

user = gl.user
print(f"Authenticated as: {user.username}")

""" projects = gl.projects.list(get_all=True)

print("List of projects:")
for project in projects:
    print(f"ID: {project.id}, Name: {project.name}") """

project = gl.projects.get(NEW_PROJECT_ID)

def create_label(name, color, description=None, priority=None):
    # Vérifier si le label existe déjà
    existing_labels = project.labels.list()
    for label in existing_labels:
        if label.name == name:
            print(f"Label '{name}' already exists.")
            return

    # Créer un nouveau label
    try:
        label = project.labels.create({
            'name': name,
            'color': color,
            'description': description if description else "",
            'priority': priority if priority is not None else ""
        })
        print(f"Label '{name}' created successfully.")
    except gitlab.exceptions.GitlabCreateError as e:
        print(f"Error creating label '{name}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Lire le fichier NDJSON et importer les labels
with open('labels.ndjson', 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():  # Vérifiez que la ligne n'est pas vide
            try:
                label = json.loads(line)
                name = label.get('title')
                color = label.get('color')
                description = label.get('description', '')
                priority = label.get('priorities', [])[0]['priority'] if label.get('priorities') else None

                if name and color:
                    create_label(name, color, description, priority)
                else:
                    print(f"Skipping label due to missing title or color: {label}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
