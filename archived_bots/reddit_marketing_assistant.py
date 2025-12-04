"""
🚀 MARKETING ASSISTANT PRO
Asistente semi-automático para promocionar productos
Plataformas: Hacker News, Twitter, Dev.to, Indie Hackers, Product Hunt
NO es un bot - TÚ haces el submit para evitar bans
"""

import webbrowser
import pyperclip
import time
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════
# 📝 CONFIGURACIÓN DEL PRODUCTO
# ═══════════════════════════════════════════════════════════════════

PRODUCT_NAME = "Auto-Debugger Pro"
PRODUCT_LINK = "https://ko-fi.com/s/85f18c167d"
PRODUCT_PRICE = "$49"

# ═══════════════════════════════════════════════════════════════════
# 📋 TEMPLATES DE POSTS PARA DIFERENTES PLATAFORMAS
# ═══════════════════════════════════════════════════════════════════

MARKETING_PLATFORMS = {
    "Hacker News (Show HN)": {
        "url": "https://news.ycombinator.com/submit",
        "title": "Show HN: Auto-Debugger Pro - AI fixes Python bugs automatically",
        "body": """I spent 6 hours debugging a blockchain hash error last month. That broke me.

Built this tool to analyze pytest output and apply fixes automatically.

Real results:
- NeuroSys_V7: 43% → 100% coverage (3 min)
- GeneradorUniversal: 0% → 100% (instant)
- AGI Phoenix: Fixed in 2 min
- 7 projects debugged, 10+ hours saved

Tech: Pure Python 3.7+, no dependencies
Works with: FastAPI, Flask, Django, PyTorch, Pydantic

Features:
- Detects False values (blockchain_integrity, metacognition flags)
- Auto-installs missing deps (neo4j, stable-baselines3, etc.)
- Fixes schema mismatches
- Handles 422 errors

Happy to answer questions!

Link: https://ko-fi.com/s/85f18c167d""",
    },
    
    "Twitter/X": {
        "url": "https://twitter.com/compose/tweet",
        "title": "Tweet",
        "body": """🤖 Just launched Auto-Debugger Pro!

AI fixes Python bugs automatically
✅ 7 projects: 43% → 100% in 3 min
✅ Auto-installs deps
✅ Works with FastAPI/Flask/Django
✅ Pure Python, no dependencies

From 6 hours debugging to 3 minutes 🚀

https://ko-fi.com/s/85f18c167d

#Python #DevTools #AI #Testing #Automation #FastAPI #MachineLearning""",
    },
    
    "Dev.to (Article)": {
        "url": "https://dev.to/new",
        "title": "How I Built an AI Debugger That Saved Me 10+ Hours",
        "body": """# How I Built an AI Debugger That Saved Me 10+ Hours

## The Problem

I spent 6 hours debugging a blockchain hash error in my FastAPI project. After finally fixing it, I realized: **I was solving the same patterns over and over**.

## The Solution

I built **Auto-Debugger Pro** - an AI tool that analyzes pytest output and applies fixes automatically.

## Real Results

I tested it on 7 of my projects:
- **NeuroSys_V7**: 43% → 100% coverage in 3 minutes
- **GeneradorUniversal**: 0% → 100% instantly  
- **AGI Phoenix**: Fixed critical bugs in 2 minutes

**Total time saved: 10+ hours**

## How It Works

```python
# 1. Run the debugger
python auto_debugger_pro.py ./my_project test_api.py

# 2. AI analyzes your tests
# Detects: False values, missing deps, schema errors, 422 status

# 3. Auto-fixes are applied
# Results: All tests passing ✅
```

## Technical Architecture

- **Pattern matching engine** for error detection
- **Subprocess management** for test execution
- **Auto-fix generators** for common bugs
- **Iterative refinement** (up to 10 cycles)

## Supports

- FastAPI, Flask, Django, PyTorch, Pydantic
- Auto-installs missing dependencies
- Schema validation errors
- Blockchain integrity fixes
- Metacognition flag activation

## Tech Stack

- Pure Python 3.7+ (no dependencies)
- Regex-based pattern detection
- UTF-8 encoding with error handling
- 180s timeout for complex tests

## Get It

If you're tired of debugging for hours, check it out:
👉 https://ko-fi.com/s/85f18c167d

## Questions?

Drop them in the comments! Happy to explain the technical details 🚀

---

*Tags: #python #debugging #ai #automation #devtools*""",
    },
    
    "Indie Hackers": {
        "url": "https://www.indiehackers.com/post/new",
        "title": "Launched Auto-Debugger Pro: $475 projected in 2 weeks from debugging tool",
        "body": """Hey indie hackers! 👋

Just launched my first product: **Auto-Debugger Pro**

## The Story

Spent 6 hours debugging a blockchain hash error. Realized I was solving the same patterns repeatedly. Built a tool to automate it.

## What It Does

Analyzes pytest output and applies fixes automatically:
- Detects False values (blockchain_integrity, metacognition)
- Auto-installs missing dependencies
- Fixes schema errors
- Handles 422 status errors

## Results

Tested on 7 of my projects:
- NeuroSys_V7: 43% → 100% (3 min)
- GeneradorUniversal: 0% → 100% (instant)
- Saved 10+ hours total

## Tech

- Pure Python 3.7+ (no dependencies)
- Works with FastAPI, Flask, Django, PyTorch
- 300+ lines of pattern-matching AI

## Launch Strategy

- Platform: Ko-fi (0% fees vs Gumroad 10%)
- Price: $49 single dev license
- Marketing: Hacker News, Twitter, Dev.to
- Projection: $475 in 2 weeks (10 sales conservative)

## Product Link

https://ko-fi.com/s/85f18c167d

## Questions for IH Community

1. Better pricing? ($49 vs $29 vs $79?)
2. Should I add team licenses?
3. RapidAPI wrapper worth it?

Happy to share code/metrics! 🚀""",
    },
    
    "Product Hunt": {
        "url": "https://www.producthunt.com/posts/new",
        "title": "Auto-Debugger Pro - Fix Python bugs with AI in 3 minutes",
        "body": """Tagline: AI debugger that analyzes pytest output and applies fixes automatically

Description:
Stop wasting hours debugging. Auto-Debugger Pro uses AI to detect bugs, generate fixes, and install dependencies automatically.

Real results from 7 production projects:
✅ NeuroSys_V7: 43% → 100% test coverage in 3 min
✅ GeneradorUniversal: 0% → 100% instantly
✅ Saved 10+ hours of manual debugging

Features:
🤖 AI-powered pattern detection (422 errors, False values, schema issues)
🔧 Automatic fixes (blockchain hashes, metacognition flags, dependencies)
📊 Detailed reports (bugs found, fixes applied, iterations needed)
⚡ Fast (3 minutes vs 4-6 hours manual)

Works with: FastAPI, Flask, Django, PyTorch, Pydantic
Tech: Pure Python 3.7+, no dependencies required

Link: https://ko-fi.com/s/85f18c167d

First Comment (después de publicar):
Hey Product Hunt! 👋

I'm the maker of Auto-Debugger Pro. Built this after spending 6 hours on a single blockchain hash bug.

The tool analyzes your test output and applies fixes automatically - saved me 10+ hours across 7 projects.

Happy to answer questions about:
- How the AI pattern matching works
- Technical architecture
- Roadmap (v1.1 coming with Git auto-commit, Slack notifications)

Thanks for checking it out! 🚀""",
    },
    
    "Discord - Python Server": {
        "url": "https://discord.gg/python",
        "title": "Post en #show-and-tell",
        "body": """Hey Python community! 👋

Just built Auto-Debugger Pro - an AI tool that analyzes pytest output and fixes bugs automatically.

Real results from my 7 projects:
• NeuroSys_V7: 43% → 100% test coverage in 3 min
• GeneradorUniversal: 0% → 100% instantly  
• AGI Phoenix: Fixed in 2 min
• Total: 10+ hours saved

What it does:
✅ Detects False values (blockchain_integrity, metacognition flags)
✅ Auto-installs missing dependencies (neo4j, stable-baselines3, etc.)
✅ Fixes schema mismatches and 422 errors
✅ Iterates up to 10 times until 100% passing

Tech stack:
• Pure Python 3.7+ (no dependencies)
• Works with FastAPI, Flask, Django, PyTorch, Pydantic
• 300+ lines of pattern-matching AI
• 180s timeout for complex tests

Check it out: https://ko-fi.com/s/85f18c167d

Happy to answer questions! 🚀""",
    },
    
    "Discord - FastAPI Server": {
        "url": "https://discord.gg/VQjSZaeJmf",
        "title": "Post en #showcase",
        "body": """Hey FastAPI community! 👋

Built a debugging tool specifically useful for FastAPI projects - Auto-Debugger Pro.

Real example from my FastAPI project:
• Before: 5 failing tests (422 errors, schema validation, neo4j missing)
• After: All tests passing in 3 minutes
• Zero manual intervention

What it does for FastAPI:
✅ Detects 422 status errors automatically
✅ Fixes Pydantic schema validation issues
✅ Auto-installs missing dependencies
✅ Handles False values in response models

Tested on 7 production projects including multiple FastAPI APIs.

Tech: Pure Python 3.7+, analyzes pytest output, applies fixes iteratively

Link: https://ko-fi.com/s/85f18c167d

Questions welcome! 🚀""",
    },
    
    "DevHunt Directory": {
        "url": "https://devhunt.org/submit",
        "title": "Auto-Debugger Pro",
        "body": """Product Name: Auto-Debugger Pro

Tagline: AI debugger that fixes Python bugs automatically in 3 minutes

Description:
Stop wasting hours debugging. Auto-Debugger Pro analyzes pytest output and applies fixes automatically.

Real results:
• 7 projects debugged: 43% → 100% test coverage
• Time saved: 10+ hours
• Supports: FastAPI, Flask, Django, PyTorch, Pydantic

Features:
• AI-powered pattern detection
• Auto-installs missing dependencies
• Fixes schema validation errors
• Handles 422 errors, False values
• Pure Python 3.7+, no dependencies

Category: Developer Tools
Subcategory: Testing & Debugging
Pricing: $49 (single developer license)
Website: https://ko-fi.com/s/85f18c167d

Tags: python, debugging, ai, automation, testing, fastapi, devtools""",
    },
    
    "AlternativeTo Directory": {
        "url": "https://alternativeto.net/suggest",
        "title": "Auto-Debugger Pro",
        "body": """Software Name: Auto-Debugger Pro

Short Description:
AI-powered Python debugger that analyzes test output and applies fixes automatically. Supports FastAPI, Flask, Django, PyTorch.

Full Description:
Auto-Debugger Pro is an AI tool that saves developers hours of debugging time by automatically detecting and fixing common Python bugs.

Key Features:
• Analyzes pytest output automatically
• Detects False values, missing dependencies, schema errors
• Auto-installs required packages
• Iterative refinement (up to 10 cycles)
• Works with FastAPI, Flask, Django, PyTorch, Pydantic
• Pure Python 3.7+, no dependencies required

Real Results:
• 7 production projects debugged
• 43% → 100% test coverage in 3 minutes average
• 10+ hours of debugging time saved

Perfect for: Python developers, QA engineers, DevOps teams

Pricing: $49 (single developer license)
Platform: Cross-platform (Python)
License: Commercial (single developer)

Website: https://ko-fi.com/s/85f18c167d

Alternative to: Manual debugging, pytest, unittest

Category: Developer Tools > Testing & Debugging
Tags: python, debugging, ai, automation, testing, fastapi, flask, django""",
    },
}

# ═══════════════════════════════════════════════════════════════════
# 🎯 FUNCIONES PRINCIPALES
# ═══════════════════════════════════════════════════════════════════

def show_banner():
    """Muestra banner de inicio"""
    print("\n" + "="*80)
    print("🚀 MARKETING ASSISTANT PRO - Auto-Debugger Pro")
    print("="*80)
    print(f"\n📦 Producto: {PRODUCT_NAME}")
    print(f"🔗 Link: {PRODUCT_LINK}")
    print(f"💰 Precio: {PRODUCT_PRICE}")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"\n🎯 Plataformas: Hacker News, Twitter, Dev.to, Indie Hackers, Product Hunt")
    print("\n" + "="*80 + "\n")

def show_menu():
    """Muestra menú de plataformas"""
    print("📋 SELECCIONA PLATAFORMA:\n")
    for i, platform in enumerate(MARKETING_PLATFORMS.keys(), 1):
        print(f"  {i}. {platform}")
    print(f"  {len(MARKETING_PLATFORMS) + 1}. Salir")
    print()

def post_to_platform(platform_name):
    """
    Prepara post para plataforma (semi-automático)
    """
    post_data = MARKETING_PLATFORMS[platform_name]
    
    print(f"\n{'='*80}")
    print(f"📝 PREPARANDO POST PARA {platform_name}")
    print(f"{'='*80}\n")
    
    # Mostrar título
    print(f"📌 TÍTULO:")
    print(f"   {post_data['title']}\n")
    
    # Mostrar cuerpo
    print(f"📄 CUERPO:")
    print(f"{'-'*80}")
    print(post_data['body'])
    print(f"{'-'*80}\n")
    
    # Copiar al portapapeles
    full_text = f"{post_data['title']}\n\n{post_data['body']}"
    
    try:
        pyperclip.copy(post_data['body'])
        print("✅ Texto copiado al portapapeles\n")
    except:
        print("⚠️  No se pudo copiar al portapapeles (instala: pip install pyperclip)\n")
    
    # Preguntar si abrir navegador
    print("🌐 OPCIONES:")
    print("  1. Abrir plataforma en navegador (recomendado)")
    print("  2. Solo mostrar información")
    print("  3. Cancelar")
    
    choice = input("\nElige opción (1-3): ").strip()
    
    if choice == "1":
        print(f"\n🌐 Abriendo {platform_name} en navegador...")
        webbrowser.open(post_data['url'])
        print("\n📋 PASOS SIGUIENTES:")
        print(f"  1. En la plataforma, busca el formulario de post")
        print(f"  2. Pega el TÍTULO (copiado):")
        print(f"     {post_data['title']}")
        print(f"  3. Pega el CUERPO (ya está en portapapeles)")
        print(f"  4. Haz clic en 'Submit' o 'Post' o 'Publish'")
        print(f"  5. ¡Listo! ✅\n")
        
        # Esperar antes de continuar
        input("Presiona ENTER cuando hayas publicado...")
        print("✅ Post completado!\n")
        
    elif choice == "2":
        print(f"\n📋 INFORMACIÓN DEL POST:")
        print(f"   URL: {post_data['url']}")
        print(f"   Título: {post_data['title']}")
        print(f"   (Cuerpo ya mostrado arriba)\n")
    else:
        print("\n❌ Cancelado\n")

# ═══════════════════════════════════════════════════════════════════
# 🚀 MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    """Función principal"""
    show_banner()
    
    while True:
        show_menu()
        
        try:
            choice = int(input("Elige opción: ").strip())
            
            if choice == len(MARKETING_PLATFORMS) + 1:
                print("\n👋 ¡Hasta luego! Buena suerte con las ventas 🚀\n")
                break
            
            if 1 <= choice <= len(MARKETING_PLATFORMS):
                platform = list(MARKETING_PLATFORMS.keys())[choice - 1]
                post_to_platform(platform)
            else:
                print("\n❌ Opción inválida\n")
                
        except ValueError:
            print("\n❌ Debes ingresar un número\n")
        except KeyboardInterrupt:
            print("\n\n👋 Interrumpido por usuario. ¡Hasta luego!\n")
            break

if __name__ == "__main__":
    main()
