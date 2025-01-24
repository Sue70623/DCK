from flask import Flask, render_template, request
from flask_mail import Mail, Message
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import base64
from google.auth.transport.requests import Request
import logging
logging.basicConfig(level=logging.DEBUG)



app = Flask(__name__)

# # Configuration pour Flask-Mail (optionnel si tu utilises Gmail OAuth uniquement)
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'suzannefv7@gmail.com'  # Remplace par ton email
# app.config['MAIL_PASSWORD'] = 'xwko sgmh zwig qcwr'  # Mot de passe d'application généré
# app.config['MAIL_DEFAULT_SENDER'] = 'suzannefv7@gmail.com'

# mail = Mail(app)

# Configuration Gmail OAuth
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
import os

# Définir les chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, r"C:\Users\All is PolitiQ\Desktop\Mes sites\DCK\backend\client_secret_114651955200-vtihoq1pc9j9d37sfmubpsaddtg3.apps.googleusercontent.com.json")  # Ton fichier JSON
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

import os
print(os.path.exists("C:/Users/All is PolitiQ/Desktop/Mes sites/DCK/backend/client_secret_114651955200-vtihoq1pc9j9d37sfmubpsaddtg3.apps.googleusercontent.com.json"))



# Vérifier si le fichier client_secret existe
if not os.path.exists(CLIENT_SECRET_FILE):
    raise FileNotFoundError(f"Fichier introuvable : {CLIENT_SECRET_FILE}")
else:
    print(f"Fichier trouvé : {CLIENT_SECRET_FILE}")
def get_gmail_service():
    """Authentifie l'utilisateur et retourne un service Gmail."""
    creds = None
    print("Début de get_gmail_service")  # Log de début
    if os.path.exists(TOKEN_FILE):
        print("Fichier token.json trouvé")  # Log token.json trouvé
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        print("Token invalide ou inexistant, démarrage de l'authentification OAuth")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            print("Tentative d'autorisation OAuth avec Google...")
            print("Lancement de l'authentification console, attends l'URL d'autorisation...")
            #creds = flow.run_console(prompt='consent')
            creds = flow.run_local_server(port=5000, open_browser=False)
            print("L'autorisation OAuth a été réussie.")
            #print("URI utilisé pour l'autorisation : ", flow.redirect_uri)  # Ajout pour vérifier
            #creds = flow.run_local_server(port=5000)
            #print("URL générée, prêt pour l'authentification")
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            print("Token sauvegardé")
    print("Fin de get_gmail_service")
    return build('gmail', 'v1', credentials=creds)


# def get_gmail_service():
#     """Authentifie l'utilisateur et retourne un service Gmail."""
#     creds = None
#     if os.path.exists(TOKEN_FILE):
#         creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
#             creds = flow.run_local_server(port=5000)
#         with open(TOKEN_FILE, 'w') as token:
#             token.write(creds.to_json())
#     return build('gmail', 'v1', credentials=creds)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Récupération des données du formulaire de contact
        nom = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Contenu de l'email
        sujet_owner = "Nouvelle demande de contact"
        body_owner = f"""
        Nouvelle demande de contact reçue :
        - Nom : {nom}
        - Email : {email}
        - Message : {message}
        """

        try:
            service = get_gmail_service()
            message_owner = {
                'raw': base64.urlsafe_b64encode(
                    f"Subject: {sujet_owner}\n\n{body_owner}".encode('utf-8')
                ).decode('utf-8')
            }
            service.users().messages().send(userId='me', body=message_owner).execute()
            return "Message envoyé avec succès !"
        except Exception as e:
            return f"Une erreur s'est produite : {e}"

    return render_template('contact.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        # Récupération des données du formulaire de réservation
        prenom = request.form.get('first-name')
        nom = request.form.get('last-name')
        telephone = request.form.get('phone')
        email = request.form.get('email')
        date = request.form.get('date')
        service_type = request.form.get('service')

        # Contenu de l'email pour l'utilisateur
        sujet_user = "Confirmation de réservation"
        body_user = f"""
        Bonjour {prenom},

        Merci pour votre réservation !
        Voici les détails de votre réservation :
        - Date : {date}
        - Service : {service_type}

        Cordialement,
        Karim - Cours de Danse Classique
        """

        # Contenu de l'email pour le propriétaire
        sujet_owner = "Nouvelle réservation"
        body_owner = f"""
        Nouvelle réservation reçue :
        - Prénom : {prenom}
        - Nom : {nom}
        - Téléphone : {telephone}
        - Email : {email}
        - Date : {date}
        - Service : {service_type}
        """

        try:
            service = get_gmail_service()

            # Envoi à l'utilisateur
            message_user = {
                'raw': base64.urlsafe_b64encode(
                    f"Subject: {sujet_user}\n\n{body_user}".encode('utf-8')
                ).decode('utf-8')
            }
            service.users().messages().send(userId='me', body=message_user).execute()

            # Envoi au propriétaire
            message_owner = {
                'raw': base64.urlsafe_b64encode(
                    f"Subject: {sujet_owner}\n\n{body_owner}".encode('utf-8')
                ).decode('utf-8')
            }
            service.users().messages().send(userId='me', body=message_owner).execute()

            return "Réservation confirmée ! Un email a été envoyé."
        except Exception as e:
            return f"Une erreur s'est produite : {e}"

    return render_template('reservations.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
