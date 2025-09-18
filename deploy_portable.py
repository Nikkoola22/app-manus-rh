#!/usr/bin/env python3
"""
Script de déploiement rapide pour l'application RH portable
Configure, teste et lance l'application en une seule commande
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class PortableDeployer:
    def __init__(self):
        self.app_dir = Path(__file__).parent.absolute()
        
    def run_setup(self):
        """Exécute la configuration"""
        print("🔧 Configuration de l'application...")
        try:
            result = subprocess.run([sys.executable, "setup_portable.py"], 
                                  cwd=self.app_dir, check=True)
            print("✅ Configuration terminée")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur de configuration: {e}")
            return False
    
    def run_tests(self):
        """Exécute les tests"""
        print("🧪 Tests de l'application...")
        try:
            result = subprocess.run([sys.executable, "test_portable.py"], 
                                  cwd=self.app_dir, check=True)
            print("✅ Tests réussis")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests échoués: {e}")
            return False
    
    def launch_application(self):
        """Lance l'application"""
        print("🚀 Lancement de l'application...")
        try:
            # Utiliser le launcher
            if os.name == 'nt':  # Windows
                subprocess.run([sys.executable, "launcher.py"], cwd=self.app_dir)
            else:  # Unix/Linux/macOS
                subprocess.run([sys.executable, "launcher.py"], cwd=self.app_dir)
            return True
        except Exception as e:
            print(f"❌ Erreur de lancement: {e}")
            return False
    
    def deploy(self, skip_tests=False, skip_setup=False):
        """Déploie l'application"""
        print("🚀 Déploiement de l'application RH portable")
        print("=" * 60)
        
        # Configuration
        if not skip_setup:
            if not self.run_setup():
                print("❌ Échec de la configuration")
                return False
        else:
            print("⏭️  Configuration ignorée")
        
        # Tests
        if not skip_tests:
            if not self.run_tests():
                print("⚠️  Tests échoués, mais continuation...")
        else:
            print("⏭️  Tests ignorés")
        
        # Lancement
        print("\n🎉 Application prête!")
        print("🌐 L'application va s'ouvrir dans votre navigateur...")
        print("📝 Pour arrêter l'application: Ctrl+C")
        print()
        
        return self.launch_application()

def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Déploiement de l'application RH portable")
    parser.add_argument("--skip-setup", action="store_true", 
                       help="Ignorer la configuration (si déjà faite)")
    parser.add_argument("--skip-tests", action="store_true", 
                       help="Ignorer les tests")
    parser.add_argument("--setup-only", action="store_true", 
                       help="Configuration uniquement (pas de lancement)")
    parser.add_argument("--test-only", action="store_true", 
                       help="Tests uniquement")
    
    args = parser.parse_args()
    
    deployer = PortableDeployer()
    
    if args.setup_only:
        success = deployer.run_setup()
    elif args.test_only:
        success = deployer.run_tests()
    else:
        success = deployer.deploy(
            skip_tests=args.skip_tests,
            skip_setup=args.skip_setup
        )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()


