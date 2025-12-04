#!/usr/bin/env python3
"""
🤖 DEMO DEL PERSONAL BOT - Aurora
Demostración de las capacidades del asistente personal
"""

import psutil
import platform
import requests
import json
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

class BotDemo:
    def __init__(self):
        self.madre_url = "https://madre-autonoma-988104947874.us-central1.run.app"
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"  🤖 AURORA - Personal Bot Demo")
        print(f"  Asistente Personal Inteligente + Madre Autónoma + NeuroSys AGI v6.0")
        print(f"{'='*70}{Style.RESET_ALL}\n")
    
    def demo_system_info(self):
        """Demo: Información del sistema"""
        print(f"{Fore.YELLOW}📊 Comando: 'Estado del sistema'{Style.RESET_ALL}")
        
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        print(f"{Fore.GREEN}🤖 Aurora:{Style.RESET_ALL}")
        print(f"   • Sistema Operativo: {platform.system()} {platform.version()}")
        print(f"   • CPU: {cpu}%")
        print(f"   • Memoria: {memory.percent}% ({round(memory.used / (1024**3), 2)} GB / {round(memory.total / (1024**3), 2)} GB)")
        print(f"   • Disco: {disk.percent}% ({round(disk.used / (1024**3), 2)} GB / {round(disk.total / (1024**3), 2)} GB)")
        print(f"   • Hostname: {platform.node()}\n")
    
    def demo_madre_status(self):
        """Demo: Estado de Madre Autónoma"""
        print(f"{Fore.YELLOW}🌐 Comando: 'Estado de Madre Autónoma'{Style.RESET_ALL}")
        
        try:
            response = requests.get(f"{self.madre_url}/madre/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"{Fore.GREEN}🤖 Aurora:{Style.RESET_ALL}")
                print(f"   ✅ Madre Autónoma está OPERATIVA")
                print(f"   • URL: {self.madre_url}")
                print(f"   • Status: {data.get('status', 'N/A')}")
                print(f"   • Timestamp: {data.get('timestamp', 'N/A')}\n")
            else:
                print(f"{Fore.RED}   ❌ Error: Status {response.status_code}{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.RED}   ❌ Madre Autónoma no disponible: {e}{Style.RESET_ALL}\n")
    
    def demo_agi_query(self):
        """Demo: Consulta a NeuroSys AGI"""
        print(f"{Fore.YELLOW}🧠 Comando: 'Consulta AGI - Razonamiento lógico'{Style.RESET_ALL}")
        
        try:
            response = requests.post(
                f"{self.madre_url}/madre/neurosys/agi/reason",
                json={
                    "agent": "logical_reasoner",
                    "query": "Si A es mayor que B, y B es mayor que C, entonces ¿qué relación hay entre A y C?",
                    "context": "Razonamiento lógico básico"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"{Fore.GREEN}🤖 Aurora:{Style.RESET_ALL}")
                print(f"   ✅ Consulta procesada por AGI")
                print(f"   • Agente: {data.get('agent', 'N/A')}")
                print(f"   • Respuesta: {json.dumps(data.get('reasoning', {}), indent=6, ensure_ascii=False)}\n")
            else:
                print(f"{Fore.RED}   ❌ Error en consulta AGI: Status {response.status_code}{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.RED}   ❌ Error: {e}{Style.RESET_ALL}\n")
    
    def demo_phoenix_stats(self):
        """Demo: Estadísticas de Phoenix"""
        print(f"{Fore.YELLOW}🐦 Comando: 'Estadísticas de Phoenix'{Style.RESET_ALL}")
        
        try:
            response = requests.get(f"{self.madre_url}/madre/phoenix/stats", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"{Fore.GREEN}🤖 Aurora:{Style.RESET_ALL}")
                print(f"   ✅ Sistema Phoenix operativo")
                print(f"   • Estadísticas: {json.dumps(data, indent=6, ensure_ascii=False)}\n")
            else:
                print(f"{Fore.RED}   ❌ Error: Status {response.status_code}{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.RED}   ❌ Error: {e}{Style.RESET_ALL}\n")
    
    def demo_datetime(self):
        """Demo: Hora y fecha"""
        print(f"{Fore.YELLOW}🕐 Comando: 'Qué hora es'{Style.RESET_ALL}")
        now = datetime.now()
        print(f"{Fore.GREEN}🤖 Aurora:{Style.RESET_ALL}")
        print(f"   Son las {now.strftime('%H:%M:%S')}")
        print(f"   Hoy es {now.strftime('%A, %d de %B de %Y')}\n")
    
    def demo_available_commands(self):
        """Demo: Comandos disponibles"""
        print(f"{Fore.YELLOW}❓ Comando: 'Ayuda'{Style.RESET_ALL}")
        print(f"{Fore.GREEN}🤖 Aurora:{Style.RESET_ALL}")
        print(f"   Puedo ayudarte con:")
        print(f"   • 📊 Estado del sistema (CPU, RAM, Disco)")
        print(f"   • 🌐 Estado de Madre Autónoma")
        print(f"   • 🧠 Consultas a NeuroSys AGI")
        print(f"   • 🐦 Estadísticas de Phoenix")
        print(f"   • 🚀 Abrir aplicaciones")
        print(f"   • 🔍 Buscar en la web")
        print(f"   • 💻 Generar código")
        print(f"   • 🕐 Hora y fecha actual")
        print(f"   • ❓ Y mucho más...\n")
    
    def run_full_demo(self):
        """Ejecutar demostración completa"""
        demos = [
            ("Comandos Disponibles", self.demo_available_commands),
            ("Información del Sistema", self.demo_system_info),
            ("Hora y Fecha", self.demo_datetime),
            ("Estado de Madre Autónoma", self.demo_madre_status),
            ("Estadísticas Phoenix", self.demo_phoenix_stats),
            ("Consulta AGI", self.demo_agi_query),
        ]
        
        for i, (name, demo_func) in enumerate(demos, 1):
            print(f"{Fore.CYAN}┌{'─'*68}┐")
            print(f"│ Demo {i}/{len(demos)}: {name:<55} │")
            print(f"└{'─'*68}┘{Style.RESET_ALL}")
            
            try:
                demo_func()
            except Exception as e:
                print(f"{Fore.RED}Error en demo: {e}{Style.RESET_ALL}\n")
            
            if i < len(demos):
                input(f"{Fore.BLUE}Presiona Enter para continuar...{Style.RESET_ALL}")
                print()
        
        print(f"{Fore.CYAN}{'='*70}")
        print(f"  ✅ Demo completada")
        print(f"  💡 Para usar Aurora en modo interactivo: python personal_bot.py")
        print(f"{'='*70}{Style.RESET_ALL}\n")


def main():
    """Función principal"""
    demo = BotDemo()
    
    print(f"{Fore.YELLOW}🎯 Esta es una demostración de las capacidades de Aurora{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   El bot personal inteligente integrado con Madre Autónoma{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}¿Ejecutar demo completa? (s/n): {Style.RESET_ALL}").strip().lower()
    
    if choice == 's' or choice == 'si' or choice == 'sí' or choice == '':
        demo.run_full_demo()
    else:
        print(f"\n{Fore.GREEN}Selecciona una demo individual:{Style.RESET_ALL}")
        print("  1. Comandos disponibles")
        print("  2. Información del sistema")
        print("  3. Hora y fecha")
        print("  4. Estado de Madre Autónoma")
        print("  5. Estadísticas Phoenix")
        print("  6. Consulta AGI")
        
        selection = input(f"\n{Fore.CYAN}Opción (1-6): {Style.RESET_ALL}").strip()
        
        demos_map = {
            '1': demo.demo_available_commands,
            '2': demo.demo_system_info,
            '3': demo.demo_datetime,
            '4': demo.demo_madre_status,
            '5': demo.demo_phoenix_stats,
            '6': demo.demo_agi_query,
        }
        
        demo_func = demos_map.get(selection)
        if demo_func:
            print()
            demo_func()
        else:
            print(f"{Fore.RED}Opción no válida{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
