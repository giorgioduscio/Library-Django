import urllib.request
import urllib.error
import os

# docker compose exec django-demo python users/test_security_log.py

url = "http://localhost:8000/"
req = urllib.request.Request(url)
req.add_header("Host", "invalidhost.com")

print("Sending request with invalid Host header to trigger django.security warning...")
try:
    # We must disable redirect or handle the error
    with urllib.request.urlopen(req) as response:
        print(f"Response code: {response.getcode()}")
except urllib.error.HTTPError as e:
    print(f"Request failed as expected. Status code: {e.code}")
    print("-" * 50)
    print("Verifica del file logs/security.log in corso...")
    
    # Trova il percorso del log rispetto alla posizione dello script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    log_path = os.path.join(project_root, "logs", "security.log")
    
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            log_content = f.read()
        if "invalidhost.com" in log_content:
            print("✅ SUCCESSO: La violazione di sicurezza (Host non valido) è stata registrata correttamente nel log.")
        else:
            print("❌ ERRORE: Il file di log esiste, ma non contiene la segnalazione della violazione per 'invalidhost.com'.")
    else:
        print(f"❌ ERRORE: Il file {log_path} non è stato creato!")
except Exception as e:
    print(f"❌ ERRORE: Connessione fallita ({e}).")
    print("Assicurati che il server Django sia attivo nel container (es. 'docker compose up')")
