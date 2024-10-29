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

project = gl.projects.get(NEW_PROJECT_ID)

def create_board(name):
    # Créer un nouveau tableau
    try:
        board = project.boards.create({'name': name})
        print(f"Board '{name}' created successfully.")
        return board
    except gitlab.exceptions.GitlabCreateError as e:
        print(f"Error creating board '{name}': {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def add_list_to_board(board, list_type, label_title=None):
    try:
        board_instance = project.boards.get(board.id)
        existing_lists = board_instance.lists.list()

        position = len(existing_lists)

        list_data = {
            'list_type': list_type,
            'position': position,
        }

        if label_title:
            # Récupérer l'ID du label basé sur le titre
            labels = project.labels.list()
            label_id = next((l.id for l in labels if l.name == label_title), None)
            if label_id:
                list_data['label_id'] = label_id
            else:
                print(f"Label '{label_title}' not found.")
                return

        # Ajouter la liste au tableau
        board_instance.lists.create(list_data)
        print(f"List '{list_type}' added to board '{board.name}'.")
    except gitlab.exceptions.GitlabCreateError as e:
        print(f"Error adding list to board '{board.name}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Lire le fichier NDJSON et créer les tableaux
with open('boards.ndjson', 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():  # Vérifiez que la ligne n'est pas vide
            try:
                board_data = json.loads(line)
                name = board_data.get('name')
                if name:
                    # Créer le tableau
                    board = create_board(name)
                    if board:
                        # Ajouter les listes au tableau
                        for list_data in board_data.get('lists', []):
                            list_type = list_data.get('list_type')
                            label_title = list_data.get('label', {}).get('title')
                            add_list_to_board(board, list_type, label_title)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")