#!/usr/bin/env python3
"""
Script de test pour vérifier le calcul automatique des RTT
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.agent import Agent

def test_rtt_calculation():
    """Test du calcul automatique des RTT"""
    print("🧮 Test du calcul automatique des RTT")
    print("=" * 50)
    
    # Créer des agents de test avec différentes quotités
    test_cases = [
        {"quotite": 38, "expected_rtt": 18, "description": "38h/semaine"},
        {"quotite": 36, "expected_rtt": 6, "description": "36h/semaine"},
        {"quotite": 35, "expected_rtt": 0, "description": "35h/semaine"},
        {"quotite": 32, "expected_rtt": 0, "description": "32h/semaine"},
        {"quotite": 40, "expected_rtt": 18, "description": "40h/semaine"},
    ]
    
    for case in test_cases:
        # Créer un agent temporaire pour le test
        agent = Agent()
        agent.quotite_travail = case["quotite"]
        
        calculated_rtt = agent.calculate_rtt_from_quotite()
        expected_rtt = case["expected_rtt"]
        
        status = "✅" if calculated_rtt == expected_rtt else "❌"
        
        print(f"{status} {case['description']}: {calculated_rtt}RTT (attendu: {expected_rtt}RTT)")
        
        if calculated_rtt != expected_rtt:
            print(f"   ⚠️  Erreur: calculé {calculated_rtt}, attendu {expected_rtt}")
    
    print("\n📊 Règles de calcul des RTT:")
    print("   • 38h et plus → 18 RTT")
    print("   • 36h-37h → 6 RTT")
    print("   • 35h et moins → 0 RTT")
    
    print("\n🎯 Test de l'API:")
    print("   Les RTT sont maintenant calculés automatiquement dans l'API")
    print("   selon la quotité de travail de l'agent")

if __name__ == "__main__":
    test_rtt_calculation()




