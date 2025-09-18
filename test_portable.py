#!/usr/bin/env python3
"""
Script de test pour vérifier le bon fonctionnement de l'application portable
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

class PortableTester:
    def __init__(self):
        self.app_dir = Path(__file__).parent.absolute()
        self.python_cmd = self._get_python_command()
        
    def _get_python_command(self):
        """Détermine la commande Python à utiliser"""
        if os.name == 'nt':  # Windows
            return str(self.app_dir / "venv" / "Scripts" / "python.exe")
        else:  # Unix/Linux/macOS
            return str(self.app_dir / "venv" / "bin" / "python")
    
    def test_python_environment(self):
        """Teste l'environnement Python"""
        print("🐍 Test de l'environnement Python...")
        
        try:
            result = subprocess.run([self.python_cmd, "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Python: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"❌ Erreur Python: {e}")
            return False
    
    def test_dependencies(self):
        """Teste les dépendances Python"""
        print("📦 Test des dépendances Python...")
        
        try:
            result = subprocess.run([self.python_cmd, "-c", 
                                   "import flask, flask_sqlalchemy, flask_cors; print('✅ Dépendances OK')"], 
                                  capture_output=True, text=True, check=True)
            print(result.stdout.strip())
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Dépendances manquantes: {e}")
            return False
    
    def test_database(self):
        """Teste la base de données"""
        print("🗄️ Test de la base de données...")
        
        db_path = self.app_dir / "database" / "app.db"
        if db_path.exists():
            print("✅ Base de données trouvée")
            return True
        else:
            print("❌ Base de données non trouvée")
            return False
    
    def test_flask_startup(self):
        """Teste le démarrage de Flask"""
        print("🐍 Test du démarrage Flask...")
        
        try:
            # Démarrer Flask en arrière-plan
            process = subprocess.Popen([self.python_cmd, "main.py"], 
                                     cwd=self.app_dir,
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            # Attendre que Flask démarre
            for i in range(10):
                try:
                    response = requests.get('http://localhost:5001/api/auth/check-session', timeout=2)
                    if response.status_code == 200:
                        print("✅ Flask démarre correctement")
                        process.terminate()
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"   Attente... ({i+1}/10)")
            
            print("❌ Flask ne démarre pas")
            process.terminate()
            return False
            
        except Exception as e:
            print(f"❌ Erreur Flask: {e}")
            return False
    
    def test_node_environment(self):
        """Teste l'environnement Node.js"""
        print("📦 Test de l'environnement Node.js...")
        
        try:
            result = subprocess.run(["node", "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Node.js: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"❌ Erreur Node.js: {e}")
            return False
    
    def test_vite_dependencies(self):
        """Teste les dépendances Vite"""
        print("⚡ Test des dépendances Vite...")
        
        node_modules = self.app_dir / "node_modules"
        if node_modules.exists():
            print("✅ Dépendances Node.js installées")
            return True
        else:
            print("❌ Dépendances Node.js manquantes")
            return False
    
    def test_vite_startup(self):
        """Teste le démarrage de Vite"""
        print("⚡ Test du démarrage Vite...")
        
        try:
            # Démarrer Vite en arrière-plan
            process = subprocess.Popen(["node", "run", "dev"], 
                                     cwd=self.app_dir,
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            # Attendre que Vite démarre
            for i in range(15):
                try:
                    response = requests.get('http://localhost:5173/', timeout=2)
                    if response.status_code == 200:
                        print("✅ Vite démarre correctement")
                        process.terminate()
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"   Attente... ({i+1}/15)")
            
            print("❌ Vite ne démarre pas")
            process.terminate()
            return False
            
        except Exception as e:
            print(f"❌ Erreur Vite: {e}")
            return False
    
    def test_api_endpoints(self):
        """Teste les endpoints de l'API"""
        print("🔌 Test des endpoints API...")
        
        try:
            # Démarrer Flask
            flask_process = subprocess.Popen([self.python_cmd, "main.py"], 
                                           cwd=self.app_dir,
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.PIPE)
            
            # Attendre que Flask démarre
            time.sleep(3)
            
            # Tester les endpoints
            endpoints = [
                ('/api/auth/check-session', 'GET'),
                ('/api/agents', 'GET'),
                ('/api/services', 'GET')
            ]
            
            all_ok = True
            for endpoint, method in endpoints:
                try:
                    if method == 'GET':
                        response = requests.get(f'http://localhost:5001{endpoint}', timeout=5)
                        if response.status_code in [200, 401, 403]:  # 401/403 sont OK pour les endpoints protégés
                            print(f"✅ {endpoint}: OK")
                        else:
                            print(f"⚠️  {endpoint}: Status {response.status_code}")
                            all_ok = False
                except Exception as e:
                    print(f"❌ {endpoint}: {e}")
                    all_ok = False
            
            flask_process.terminate()
            return all_ok
            
        except Exception as e:
            print(f"❌ Erreur test API: {e}")
            return False
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🧪 Tests de l'application portable")
        print("=" * 50)
        
        tests = [
            ("Environnement Python", self.test_python_environment),
            ("Dépendances Python", self.test_dependencies),
            ("Base de données", self.test_database),
            ("Démarrage Flask", self.test_flask_startup),
            ("Environnement Node.js", self.test_node_environment),
            ("Dépendances Vite", self.test_vite_dependencies),
            ("Démarrage Vite", self.test_vite_startup),
            ("Endpoints API", self.test_api_endpoints)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🔍 {test_name}...")
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ Erreur lors du test: {e}")
                results.append((test_name, False))
        
        # Résumé
        print("\n" + "=" * 50)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
            if result:
                passed += 1
        
        print(f"\n📈 Résultat: {passed}/{total} tests réussis")
        
        if passed == total:
            print("🎉 Tous les tests sont passés! L'application est prête.")
        else:
            print("⚠️  Certains tests ont échoué. Vérifiez la configuration.")
        
        return passed == total

if __name__ == "__main__":
    tester = PortableTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

