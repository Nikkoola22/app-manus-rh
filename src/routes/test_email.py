from flask import Blueprint, request, jsonify, session
from src.services.email_service import send_test_email
from src.routes.auth import login_required

test_email_bp = Blueprint('test_email', __name__)

@test_email_bp.route('/test-email', methods=['POST'])
@login_required
def test_email():
    """Route de test pour l'envoi d'emails"""
    try:
        data = request.get_json()
        email = data.get('email', 'nikkoola@gmail.com')
        
        # Envoyer un email de test
        success = send_test_email(email)
        
        if success:
            return jsonify({
                'message': f'Email de test envoyé à {email}',
                'success': True
            }), 200
        else:
            return jsonify({
                'error': 'Erreur lors de l\'envoi de l\'email',
                'success': False
            }), 500
            
    except Exception as e:
        return jsonify({
            'error': f'Erreur: {str(e)}',
            'success': False
        }), 500

