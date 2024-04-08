#!/usr/bin/python3

from flask import Flask

# Créer une instance d'application Flask
app = Flask(__name__)

# Route pour afficher "Hello HBNB!"
@app.route('/', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB!'

# Méthode principale pour exécuter l'application Flask
if __name__ == '__main__':
    # Exécuter l'application sur 0.0.0.0, port 5000
    app.run(host='0.0.0.0', port=5000)
