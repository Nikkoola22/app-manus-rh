from flask import Blueprint, request, jsonify, session
from src.models.presence import Presence
from src.models.agent import Agent
from src.models.demande_conge import DemandeConge
from src.models.user import db
from src.routes.auth import login_required, role_required
from datetime import datetime, date, timedelta
import calendar

presence_bp = Blueprint('presence', __name__)

@presence_bp.route('/presence', methods=['GET'])
@login_required
def get_presences():
    """Récupère les présences selon les permissions et les filtres"""
    try:
        current_user = Agent.query.get(session['user_id'])
        
        # Paramètres de filtrage
        agent_id = request.args.get('agent_id')
        date_debut = request.args.get('date_debut')
        date_fin = request.args.get('date_fin')
        semaine = request.args.get('semaine')  # Format: YYYY-WW (ex: 2024-15)
        
        # Construire la requête de base
        query = Presence.query
        
        # Filtrage par agent
        if agent_id:
            query = query.filter_by(agent_id=agent_id)
        
        # Filtrage par dates
        if date_debut and date_fin:
            date_debut_obj = datetime.strptime(date_debut, '%Y-%m-%d').date()
            date_fin_obj = datetime.strptime(date_fin, '%Y-%m-%d').date()
            query = query.filter(Presence.date_presence >= date_debut_obj, Presence.date_presence <= date_fin_obj)
        
        # Filtrage par semaine
        if semaine:
            try:
                annee, semaine_num = semaine.split('-')
                annee, semaine_num = int(annee), int(semaine_num)
                
                # Calculer les dates de début et fin de la semaine
                # Lundi comme premier jour de la semaine
                date_debut_semaine = datetime.strptime(f'{annee}-W{semaine_num:02d}-1', '%Y-W%W-%w').date()
                date_fin_semaine = date_debut_semaine + timedelta(days=6)
                
                query = query.filter(Presence.date_presence >= date_debut_semaine, Presence.date_presence <= date_fin_semaine)
            except ValueError:
                return jsonify({'error': 'Format de semaine invalide. Utilisez YYYY-WW'}), 400
        
        # Permissions selon le rôle
        if current_user.role == 'Admin':
            # Admin peut voir toutes les présences
            pass
        elif current_user.role == 'Responsable':
            # Responsable peut voir les présences de son service
            agents_du_service = Agent.query.filter_by(service_id=current_user.service_id).all()
            agent_ids = [agent.id for agent in agents_du_service]
            query = query.filter(Presence.agent_id.in_(agent_ids))
        elif current_user.role == 'Agent':
            # Agent peut voir seulement ses propres présences
            query = query.filter_by(agent_id=current_user.id)
        else:
            return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        presences = query.order_by(Presence.date_presence.desc()).all()
        
        return jsonify([presence.to_dict() for presence in presences]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@presence_bp.route('/presence', methods=['POST'])
@login_required
@role_required(['Admin', 'Responsable'])
def create_presence():
    """Crée une nouvelle entrée de présence"""
    try:
        data = request.get_json()
        current_user = Agent.query.get(session['user_id'])
        
        # Validation des champs requis
        required_fields = ['agent_id', 'date_presence', 'creneau', 'statut']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Le champ {field} est requis'}), 400
        
        agent_id = data['agent_id']
        
        # Vérifier les permissions
        if current_user.role == 'Responsable':
            agent = Agent.query.get(agent_id)
            if not agent or agent.service_id != current_user.service_id:
                return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        # Vérifier que l'agent existe
        agent = Agent.query.get(agent_id)
        if not agent:
            return jsonify({'error': 'Agent non trouvé'}), 404
        
        # Parser la date
        date_presence = datetime.strptime(data['date_presence'], '%Y-%m-%d').date()
        
        # Vérifier s'il existe déjà une présence pour cette date, cet agent et ce créneau
        creneau = data['creneau']
        existing_presence = Presence.query.filter_by(
            agent_id=agent_id, 
            date_presence=date_presence,
            creneau=creneau
        ).first()
        
        if existing_presence:
            return jsonify({'error': 'Une présence existe déjà pour cet agent à cette date et ce créneau'}), 400
        
        # Calculer la durée si les heures sont fournies
        duree_heures = None
        if data.get('heure_debut') and data.get('heure_fin'):
            heure_debut = datetime.strptime(data['heure_debut'], '%H:%M').time()
            heure_fin = datetime.strptime(data['heure_fin'], '%H:%M').time()
            
            # Calculer la différence en heures
            debut_datetime = datetime.combine(date.today(), heure_debut)
            fin_datetime = datetime.combine(date.today(), heure_fin)
            duree_heures = (fin_datetime - debut_datetime).total_seconds() / 3600
            
            # Ajuster si la présence est sur plusieurs jours (cas rare)
            if duree_heures < 0:
                duree_heures += 24
        
        # Créer la présence
        presence = Presence(
            agent_id=agent_id,
            date_presence=date_presence,
            creneau=creneau,
            statut=data['statut'],
            motif=data.get('motif', ''),
            heure_debut=datetime.strptime(data['heure_debut'], '%H:%M').time() if data.get('heure_debut') else None,
            heure_fin=datetime.strptime(data['heure_fin'], '%H:%M').time() if data.get('heure_fin') else None,
            duree_heures=duree_heures,
            cree_par=current_user.id
        )
        
        db.session.add(presence)
        db.session.commit()
        
        return jsonify(presence.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': f'Format de date/heure invalide: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@presence_bp.route('/presence/<int:presence_id>', methods=['PUT'])
@login_required
@role_required(['Admin', 'Responsable'])
def update_presence(presence_id):
    """Met à jour une présence"""
    try:
        presence = Presence.query.get_or_404(presence_id)
        current_user = Agent.query.get(session['user_id'])
        
        # Vérifier les permissions
        if current_user.role == 'Responsable':
            if presence.agent.service_id != current_user.service_id:
                return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        data = request.get_json()
        
        # Mettre à jour les champs
        if 'statut' in data:
            presence.statut = data['statut']
        if 'creneau' in data:
            presence.creneau = data['creneau']
        if 'motif' in data:
            presence.motif = data['motif']
        if 'heure_debut' in data:
            presence.heure_debut = datetime.strptime(data['heure_debut'], '%H:%M').time() if data['heure_debut'] else None
        if 'heure_fin' in data:
            presence.heure_fin = datetime.strptime(data['heure_fin'], '%H:%M').time() if data['heure_fin'] else None
        
        # Recalculer la durée si nécessaire
        if presence.heure_debut and presence.heure_fin:
            debut_datetime = datetime.combine(date.today(), presence.heure_debut)
            fin_datetime = datetime.combine(date.today(), presence.heure_fin)
            presence.duree_heures = (fin_datetime - debut_datetime).total_seconds() / 3600
            
            if presence.duree_heures < 0:
                presence.duree_heures += 24
        else:
            presence.duree_heures = None
        
        db.session.commit()
        
        return jsonify(presence.to_dict()), 200
        
    except ValueError as e:
        return jsonify({'error': f'Format de date/heure invalide: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@presence_bp.route('/presence/<int:presence_id>', methods=['DELETE'])
@login_required
@role_required(['Admin', 'Responsable'])
def delete_presence(presence_id):
    """Supprime une présence"""
    try:
        presence = Presence.query.get_or_404(presence_id)
        current_user = Agent.query.get(session['user_id'])
        
        # Vérifier les permissions
        if current_user.role == 'Responsable':
            if presence.agent.service_id != current_user.service_id:
                return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        db.session.delete(presence)
        db.session.commit()
        
        return jsonify({'message': 'Présence supprimée avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@presence_bp.route('/presence/calendrier/semaine/<string:semaine>', methods=['GET'])
@login_required
@role_required(['Admin', 'Responsable'])
def get_calendrier_semaine(semaine):
    """Récupère le calendrier pour une semaine donnée"""
    try:
        current_user = Agent.query.get(session['user_id'])
        
        # Parser la semaine (format: YYYY-WW)
        try:
            annee, semaine_num = semaine.split('-')
            annee, semaine_num = int(annee), int(semaine_num)
        except ValueError:
            return jsonify({'error': 'Format de semaine invalide. Utilisez YYYY-WW'}), 400
        
        # Calculer les dates de la semaine (lundi à dimanche)
        date_debut_semaine = datetime.strptime(f'{annee}-W{semaine_num:02d}-1', '%Y-W%W-%w').date()
        date_fin_semaine = date_debut_semaine + timedelta(days=6)
        
        # Récupérer les agents selon les permissions
        if current_user.role == 'Admin':
            agents = Agent.query.filter_by(role='Agent').all()
        elif current_user.role == 'Responsable':
            agents = Agent.query.filter_by(service_id=current_user.service_id, role='Agent').all()
        else:
            return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        # Récupérer les présences pour cette semaine
        presences = Presence.query.filter(
            Presence.date_presence >= date_debut_semaine,
            Presence.date_presence <= date_fin_semaine
        ).all()
        
        # Récupérer les demandes de congés validées pour cette semaine
        demandes_validées = DemandeConge.query.filter(
            DemandeConge.statut == 'Approuvée',
            DemandeConge.date_debut <= date_fin_semaine,
            DemandeConge.date_fin >= date_debut_semaine
        ).all()
        
        # Organiser les données par agent et par jour
        calendrier_data = {
            'semaine': semaine,
            'date_debut': date_debut_semaine.isoformat(),
            'date_fin': date_fin_semaine.isoformat(),
            'agents': []
        }
        
        for agent in agents:
            agent_data = {
                'id': agent.id,
                'nom': f"{agent.prenom} {agent.nom}",
                'service': agent.service.nom_service if agent.service else 'Non assigné',
                'jours': {}
            }
            
            # Initialiser tous les jours de la semaine avec créneaux matin/après-midi
            for i in range(7):
                jour_date = date_debut_semaine + timedelta(days=i)
                agent_data['jours'][jour_date.isoformat()] = {
                    'date': jour_date.isoformat(),
                    'matin': {
                        'presence': None,
                        'statut': 'absent'
                    },
                    'apres_midi': {
                        'presence': None,
                        'statut': 'absent'
                    }
                }
            
            # Remplir avec les présences existantes
            for presence in presences:
                if presence.agent_id == agent.id:
                    jour_date = presence.date_presence.isoformat()
                    if jour_date in agent_data['jours']:
                        creneau = presence.creneau
                        if creneau in agent_data['jours'][jour_date]:
                            agent_data['jours'][jour_date][creneau] = {
                                'presence': presence.to_dict(),
                                'statut': presence.statut,
                                'type': 'presence'
                            }
            
            # Remplir avec les demandes de congés validées
            for demande in demandes_validées:
                if demande.agent_id == agent.id:
                    # Vérifier si la demande couvre des jours de cette semaine
                    date_demande_debut = max(demande.date_debut, date_debut_semaine)
                    date_demande_fin = min(demande.date_fin, date_fin_semaine)
                    
                    current_date = date_demande_debut
                    while current_date <= date_demande_fin:
                        jour_date = current_date.isoformat()
                        if jour_date in agent_data['jours']:
                            # Créer un objet présence virtuel pour la demande de congés
                            demande_presence = {
                                'id': f"demande_{demande.id}",
                                'agent_id': demande.agent_id,
                                'date_presence': jour_date,
                                'creneau': 'journee',
                                'statut': demande.type_absence.lower(),
                                'motif': demande.motif or f"Congés validés - {demande.type_absence}",
                                'heure_debut': None,
                                'heure_fin': None,
                                'duree_heures': demande.nb_heures,
                                'date_creation': demande.date_demande.isoformat(),
                                'cree_par': demande.agent_id,
                                'statut_color': 'blue' if demande.type_absence.lower() in ['conges', 'rtt'] else 'orange',
                                'statut_label': demande.type_absence,
                                'creneau_label': 'Journée',
                                'creneau_color': 'bg-gray-50 border-gray-200',
                                'duree_display': f"{demande.nb_heures}h",
                                'agent_nom': f"{demande.agent.prenom} {demande.agent.nom}" if demande.agent else None,
                                'createur_nom': f"{demande.agent.prenom} {demande.agent.nom}" if demande.agent else None,
                                'is_demande': True,
                                'demande_id': demande.id
                            }
                            
                            # Pour les demandes de congés, afficher sur les deux créneaux
                            if agent_data['jours'][jour_date]['matin']['statut'] == 'absent':
                                agent_data['jours'][jour_date]['matin'] = {
                                    'presence': demande_presence,
                                    'statut': demande.type_absence.lower(),
                                    'type': 'demande'
                                }
                            
                            if agent_data['jours'][jour_date]['apres_midi']['statut'] == 'absent':
                                agent_data['jours'][jour_date]['apres_midi'] = {
                                    'presence': demande_presence,
                                    'statut': demande.type_absence.lower(),
                                    'type': 'demande'
                                }
                        
                        current_date += timedelta(days=1)
            
            calendrier_data['agents'].append(agent_data)
        
        return jsonify(calendrier_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@presence_bp.route('/presence/statistiques/semaine/<string:semaine>', methods=['GET'])
@login_required
@role_required(['Admin', 'Responsable'])
def get_statistiques_semaine(semaine):
    """Récupère les statistiques de présence pour une semaine"""
    try:
        current_user = Agent.query.get(session['user_id'])
        
        # Parser la semaine
        try:
            annee, semaine_num = semaine.split('-')
            annee, semaine_num = int(annee), int(semaine_num)
        except ValueError:
            return jsonify({'error': 'Format de semaine invalide'}), 400
        
        date_debut_semaine = datetime.strptime(f'{annee}-W{semaine_num:02d}-1', '%Y-W%W-%w').date()
        date_fin_semaine = date_debut_semaine + timedelta(days=6)
        
        # Récupérer les agents selon les permissions
        if current_user.role == 'Admin':
            agents = Agent.query.filter_by(role='Agent').all()
        elif current_user.role == 'Responsable':
            agents = Agent.query.filter_by(service_id=current_user.service_id, role='Agent').all()
        else:
            return jsonify({'error': 'Permissions insuffisantes'}), 403
        
        # Récupérer les présences
        presences = Presence.query.filter(
            Presence.date_presence >= date_debut_semaine,
            Presence.date_presence <= date_fin_semaine
        ).all()
        
        # Récupérer les demandes de congés validées
        demandes_validées = DemandeConge.query.filter(
            DemandeConge.statut == 'Approuvée',
            DemandeConge.date_debut <= date_fin_semaine,
            DemandeConge.date_fin >= date_debut_semaine
        ).all()
        
        # Calculer les statistiques
        total_agents = len(agents)
        total_jours_possibles = total_agents * 7  # 7 jours par agent
        
        # Compter par statut (présences + demandes validées)
        statuts_count = {}
        
        # Compter les présences manuelles
        for presence in presences:
            statuts_count[presence.statut] = statuts_count.get(presence.statut, 0) + 1
        
        # Compter les demandes de congés validées
        for demande in demandes_validées:
            # Calculer les jours de la demande dans cette semaine
            date_demande_debut = max(demande.date_debut, date_debut_semaine)
            date_demande_fin = min(demande.date_fin, date_fin_semaine)
            
            current_date = date_demande_debut
            while current_date <= date_demande_fin:
                statut_demande = demande.type_absence.lower()
                statuts_count[statut_demande] = statuts_count.get(statut_demande, 0) + 1
                current_date += timedelta(days=1)
        
        # Calculer le pourcentage de présence
        presences_totales = sum(statuts_count.values())
        pourcentage_presence = (statuts_count.get('present', 0) / total_jours_possibles * 100) if total_jours_possibles > 0 else 0
        
        return jsonify({
            'semaine': semaine,
            'total_agents': total_agents,
            'total_jours_possibles': total_jours_possibles,
            'presences_totales': presences_totales,
            'pourcentage_presence': round(pourcentage_presence, 2),
            'statuts': statuts_count,
            'date_debut': date_debut_semaine.isoformat(),
            'date_fin': date_fin_semaine.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
