from flask import current_app
from flask_mail import Mail, Message
from datetime import datetime
import os

# Charger les variables d'environnement
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuration du service email
mail = Mail()

def init_email(app):
    """Initialise le service email avec l'application Flask"""
    # Configuration SMTP (peut être modifiée selon vos besoins)
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@entreprise.com')
    
    mail.init_app(app)

def send_demande_conge_email(agent, responsable, demande):
    """Envoie un email au responsable quand un agent fait une demande de congé"""
    try:
        subject = f"📅 Nouvelle demande de congé - {agent.prenom} {agent.nom}"
        
        # Template HTML pour l'email
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: white; padding: 20px; border-radius: 8px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .status {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
                .status-pending {{ background: #fff3cd; color: #856404; border: 1px solid #ffeaa7; }}
                .btn {{ display: inline-block; padding: 12px 25px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px 5px; }}
                .btn:hover {{ background: #0056b3; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📅 Nouvelle Demande de Congé</h1>
                    <p>Une nouvelle demande de congé nécessite votre validation</p>
                </div>
                
                <div class="content">
                    <div class="info-box">
                        <h3>👤 Informations de l'Agent</h3>
                        <p><strong>Nom :</strong> {agent.prenom} {agent.nom}</p>
                        <p><strong>Email :</strong> {agent.email}</p>
                        <p><strong>Service :</strong> {agent.service.nom_service if agent.service else 'Non assigné'}</p>
                    </div>
                    
                    <div class="info-box">
                        <h3>📋 Détails de la Demande</h3>
                        <p><strong>Type d'absence :</strong> {demande.type_absence}</p>
                        <p><strong>Période :</strong> {demande.date_debut} au {demande.date_fin}</p>
                        <p><strong>Durée :</strong> {demande.nb_heures} heures</p>
                        <p><strong>Date de demande :</strong> {demande.date_demande.strftime('%d/%m/%Y à %H:%M')}</p>
                        <p><strong>Statut :</strong> <span class="status status-pending">En attente</span></p>
                        {f'<p><strong>Motif :</strong> {demande.motif}</p>' if demande.motif else ''}
                    </div>
                    
                    <div class="info-box">
                        <h3>⚡ Actions Requises</h3>
                        <p>Veuillez vous connecter à l'application RH pour valider ou refuser cette demande :</p>
                        <a href="http://localhost:5173" class="btn">Accéder à l'application</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Cet email a été envoyé automatiquement par le système RH</p>
                    <p>Merci de ne pas répondre à cet email</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Version texte simple
        text_body = f"""
        Nouvelle demande de congé - {agent.prenom} {agent.nom}
        
        Informations de l'agent :
        - Nom : {agent.prenom} {agent.nom}
        - Email : {agent.email}
        - Service : {agent.service.nom_service if agent.service else 'Non assigné'}
        
        Détails de la demande :
        - Type d'absence : {demande.type_absence}
        - Période : {demande.date_debut} au {demande.date_fin}
        - Durée : {demande.nb_heures} heures
        - Date de demande : {demande.date_demande.strftime('%d/%m/%Y à %H:%M')}
        - Statut : En attente
        {f'- Motif : {demande.motif}' if demande.motif else ''}
        
        Veuillez vous connecter à l'application RH pour valider ou refuser cette demande :
        http://localhost:5173
        """
        
        msg = Message(
            subject=subject,
            recipients=[responsable.email],
            html=html_body,
            body=text_body
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'envoi de l'email de demande : {str(e)}")
        return False

def send_validation_email(agent, responsable, demande, decision):
    """Envoie un email à l'agent quand sa demande est validée ou refusée"""
    try:
        status_text = "validée" if decision == "Approuvée" else "refusée"
        status_emoji = "✅" if decision == "Approuvée" else "❌"
        status_color = "#28a745" if decision == "Approuvée" else "#dc3545"
        
        subject = f"{status_emoji} Demande de congé {status_text} - {demande.type_absence}"
        
        # Template HTML pour l'email
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, {status_color} 0%, {status_color}dd 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: white; padding: 20px; border-radius: 8px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .status {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
                .status-approved {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
                .status-rejected {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
                .btn {{ display: inline-block; padding: 12px 25px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px 5px; }}
                .btn:hover {{ background: #0056b3; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{status_emoji} Demande de Congé {status_text.upper()}</h1>
                    <p>Votre demande de congé a été {status_text} par {responsable.prenom} {responsable.nom}</p>
                </div>
                
                <div class="content">
                    <div class="info-box">
                        <h3>📋 Détails de la Demande</h3>
                        <p><strong>Type d'absence :</strong> {demande.type_absence}</p>
                        <p><strong>Période :</strong> {demande.date_debut} au {demande.date_fin}</p>
                        <p><strong>Durée :</strong> {demande.nb_heures} heures</p>
                        <p><strong>Date de demande :</strong> {demande.date_demande.strftime('%d/%m/%Y à %H:%M')}</p>
                        <p><strong>Statut :</strong> <span class="status status-{'approved' if decision == 'Approuvée' else 'rejected'}">{decision}</span></p>
                        {f'<p><strong>Motif :</strong> {demande.motif}</p>' if demande.motif else ''}
                    </div>
                    
                    <div class="info-box">
                        <h3>👤 Validé par</h3>
                        <p><strong>Nom :</strong> {responsable.prenom} {responsable.nom}</p>
                        <p><strong>Rôle :</strong> {responsable.role}</p>
                        <p><strong>Date de validation :</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
                        {f'<p><strong>Commentaires :</strong> {demande.commentaires}</p>' if demande.commentaires else ''}
                    </div>
                    
                    {f'''
                    <div class="info-box">
                        <h3>💰 Impact sur vos soldes</h3>
                        <p>Cette demande a été déduite de votre solde de {demande.type_absence.lower()}.</p>
                        <p>Vous pouvez consulter vos soldes actuels dans votre espace personnel.</p>
                    </div>
                    ''' if decision == "Approuvée" else ''}
                    
                    <div class="info-box">
                        <h3>🔗 Actions</h3>
                        <p>Vous pouvez consulter le détail de cette demande et vos soldes dans votre espace personnel :</p>
                        <a href="http://localhost:5173" class="btn">Accéder à mon espace</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Cet email a été envoyé automatiquement par le système RH</p>
                    <p>Merci de ne pas répondre à cet email</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Version texte simple
        text_body = f"""
        Demande de congé {status_text.upper()} - {demande.type_absence}
        
        Votre demande de congé a été {status_text} par {responsable.prenom} {responsable.nom}
        
        Détails de la demande :
        - Type d'absence : {demande.type_absence}
        - Période : {demande.date_debut} au {demande.date_fin}
        - Durée : {demande.nb_heures} heures
        - Date de demande : {demande.date_demande.strftime('%d/%m/%Y à %H:%M')}
        - Statut : {decision}
        {f'- Motif : {demande.motif}' if demande.motif else ''}
        
        Validé par :
        - Nom : {responsable.prenom} {responsable.nom}
        - Rôle : {responsable.role}
        - Date de validation : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
        {f'- Commentaires : {demande.commentaires}' if demande.commentaires else ''}
        
        Vous pouvez consulter le détail de cette demande dans votre espace personnel :
        http://localhost:5173
        """
        
        msg = Message(
            subject=subject,
            recipients=[agent.email],
            html=html_body,
            body=text_body
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'envoi de l'email de validation : {str(e)}")
        return False

def send_test_email(recipient_email):
    """Envoie un email de test pour vérifier la configuration"""
    try:
        subject = "🧪 Test de Configuration Email - Système RH"
        
        html_body = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }
                .content { background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }
                .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; border: 1px solid #c3e6cb; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧪 Test de Configuration Email</h1>
                    <p>Le système de notifications email est opérationnel</p>
                </div>
                <div class="content">
                    <div class="success">
                        <h3>✅ Configuration Réussie</h3>
                        <p>Le service email du système RH fonctionne correctement.</p>
                        <p>Vous recevrez désormais des notifications automatiques pour :</p>
                        <ul>
                            <li>Nouvelles demandes de congés</li>
                            <li>Validation/refus de vos demandes</li>
                            <li>Autres notifications importantes</li>
                        </ul>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = """
        Test de Configuration Email - Système RH
        
        Le système de notifications email est opérationnel.
        
        Vous recevrez désormais des notifications automatiques pour :
        - Nouvelles demandes de congés
        - Validation/refus de vos demandes
        - Autres notifications importantes
        """
        
        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            html=html_body,
            body=text_body
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'envoi de l'email de test : {str(e)}")
        return False

def send_test_email(email):
    """Envoie un email de test simple"""
    try:
        subject = "🧪 Test Email - Application RH"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: white; padding: 20px; border-radius: 8px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧪 Test Email</h1>
                    <p>Configuration email de l'application RH</p>
                </div>
                <div class="content">
                    <div class="info-box">
                        <h2>✅ Email de test réussi !</h2>
                        <p>L'envoi d'emails est correctement configuré dans l'application RH.</p>
                        <p><strong>Date:</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
                        <p><strong>Destinataire:</strong> {email}</p>
                    </div>
                    <p>Si vous recevez cet email, cela signifie que :</p>
                    <ul>
                        <li>✅ La configuration SMTP est correcte</li>
                        <li>✅ Les emails de validation de congés fonctionneront</li>
                        <li>✅ Les notifications seront envoyées</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>Application de Gestion RH - Test Email</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = Message(
            subject,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[email]
        )
        msg.html = html_body
        mail.send(msg)
        
        current_app.logger.info(f"Email de test envoyé à {email}")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Erreur lors de l'envoi de l'email de test : {str(e)}")
        return False

