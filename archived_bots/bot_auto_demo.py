#!/usr/bin/env python3
"""
🤖 AURORA - Auto Demo (Sin Interacción)
Demostración automática del bot personal
"""

import psutil
import platform
import requests
import json
import time
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

def print_header(title):
    """Imprimir encabezado"""
    print(f"\n{Fore.CYAN}┌{'─'*68}┐")
    print(f"│ {title:<66} │")
    print(f"└{'─'*68}┘{Style.RESET_ALL}\n")

def print_bot_response(text):
    """Imprimir respuesta del bot"""
    print(f"{Fore.GREEN}🤖 Aurora: {text}{Style.RESET_ALL}")

def main():
    """Demo automática"""
    # Intentar primero servidor local
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        if result == 0:
            madre_url = "http://localhost:8000"
            print(f"{Fore.GREEN}✅ Conectado a servidor LOCAL{Style.RESET_ALL}")
        else:
            madre_url = "https://madre-autonoma-988104947874.us-central1.run.app"
            print(f"{Fore.YELLOW}⚠️  Usando servidor PRODUCCIÓN{Style.RESET_ALL}")
    except:
        madre_url = "https://madre-autonoma-988104947874.us-central1.run.app"
        print(f"{Fore.YELLOW}⚠️  Usando servidor PRODUCCIÓN{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  🤖 AURORA - Personal Bot Auto Demo")
    print(f"  Asistente Personal Inteligente + Madre Autónoma + NeuroSys AGI v6.0")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    time.sleep(1)
    
    # Demo 1: Comandos disponibles
    print_header("Demo 1/6: Comandos Disponibles")
    print(f"{Fore.YELLOW}👤 Usuario: 'Ayuda'{Style.RESET_ALL}")
    print_bot_response("Puedo ayudarte con:")
    print("   • 📊 Estado del sistema (CPU, RAM, Disco)")
    print("   • 🌐 Estado de Madre Autónoma")
    print("   • 🧠 Consultas a NeuroSys AGI")
    print("   • 🐦 Estadísticas de Phoenix")
    print("   • 🚀 Abrir aplicaciones")
    print("   • 🔍 Buscar en la web")
    print("   • 💻 Generar código")
    time.sleep(2)
    
    # Demo 2: Sistema
    print_header("Demo 2/6: Información del Sistema")
    print(f"{Fore.YELLOW}👤 Usuario: 'Estado del sistema'{Style.RESET_ALL}")
    
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    print_bot_response("El sistema está funcionando:")
    print(f"   • SO: {platform.system()} {platform.version()}")
    print(f"   • CPU: {cpu}%")
    print(f"   • Memoria: {memory.percent}% ({round(memory.used / (1024**3), 2)} GB / {round(memory.total / (1024**3), 2)} GB)")
    print(f"   • Disco: {disk.percent}% ({round(disk.used / (1024**3), 2)} GB / {round(disk.total / (1024**3), 2)} GB)")
    time.sleep(2)
    
    # Demo 3: Fecha y hora
    print_header("Demo 3/6: Hora y Fecha")
    print(f"{Fore.YELLOW}👤 Usuario: 'Qué hora es'{Style.RESET_ALL}")
    
    now = datetime.now()
    print_bot_response(f"Son las {now.strftime('%H:%M:%S')}")
    print_bot_response(f"Hoy es {now.strftime('%A, %d de %B de %Y')}")
    time.sleep(2)
    
    # Demo 4: Madre Autónoma
    print_header("Demo 4/6: Estado de Madre Autónoma")
    print(f"{Fore.YELLOW}👤 Usuario: 'Estado de Madre'{Style.RESET_ALL}")
    
    try:
        response = requests.get(f"{madre_url}/madre/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_bot_response("Madre Autónoma está OPERATIVA ✅")
            print(f"   • URL: {madre_url}")
            print(f"   • Status: {data.get('status', 'N/A')}")
        else:
            print_bot_response(f"Error al conectar: Status {response.status_code}")
    except Exception as e:
        print_bot_response(f"Madre Autónoma no disponible: {str(e)[:50]}")
    time.sleep(2)
    
    # Demo 5: Phoenix Stats
    print_header("Demo 5/6: Estadísticas de Phoenix")
    print(f"{Fore.YELLOW}👤 Usuario: 'Estadísticas de Phoenix'{Style.RESET_ALL}")
    
    try:
        response = requests.get(f"{madre_url}/madre/phoenix/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_bot_response("Sistema Phoenix operativo ✅")
            print(f"   {json.dumps(data, indent=3, ensure_ascii=False)[:200]}...")
        else:
            print_bot_response(f"Error: Status {response.status_code}")
    except Exception as e:
        print_bot_response(f"Error: {str(e)[:50]}")
    time.sleep(2)
    
    # Demo 6: AGI Query
    print_header("Demo 6/6: Consulta a NeuroSys AGI")
    print(f"{Fore.YELLOW}👤 Usuario: 'Si A > B y B > C, entonces A ? C'{Style.RESET_ALL}")
    
    try:
        response = requests.post(
            f"{madre_url}/madre/neurosys/agi/reason",
            json={
                "agent": "logical_reasoner",
                "query": "Si A es mayor que B, y B es mayor que C, entonces ¿qué relación hay entre A y C?",
                "context": "Razonamiento lógico"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_bot_response("Consulta procesada por AGI ✅")
            print(f"   • Agente: {data.get('agent', 'N/A')}")
            print(f"   • Razonamiento: {json.dumps(data.get('reasoning', {}), indent=3, ensure_ascii=False)[:300]}...")
        else:
            print_bot_response(f"Error en consulta AGI: Status {response.status_code}")
    except Exception as e:
        print_bot_response(f"Error: {str(e)[:50]}")
    
    # Final
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  ✅ Demo Completada")
    print(f"  💡 Para usar Aurora en modo interactivo: python personal_bot.py")
    print(f"  📖 Documentación: PERSONAL_BOT_README.md")
    print(f"{'='*70}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
