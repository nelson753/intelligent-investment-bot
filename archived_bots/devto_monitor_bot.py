"""
🤖 DEV.TO MONITOR BOT
Monitorea comentarios en tu artículo y responde automáticamente
"""

import requests
import time
from datetime import datetime
import json

# ============================================================================
# CONFIGURACIÓN - ¡COMPLETA ESTOS DATOS!
# ============================================================================

# Tu API Key de Dev.to (obtén en: https://dev.to/settings/extensions)
DEVTO_API_KEY = "fC86HSdfVgd87VCiYHEfhuRt"  # ✅ CONFIGURADO

# ID de tu artículo (lo encuentras en la URL)
# Ejemplo: https://dev.to/nelson753/i-built-an-ai-debugger-5abc
# El ID es el número al final o el slug completo
ARTICLE_SLUG = "i-built-an-ai-debugger-43-to-100-tests-in-3-minutes-h14"

# Tu username de Dev.to
USERNAME = "nelson753"

# ============================================================================
# RESPUESTAS AUTOMÁTICAS INTELIGENTES
# ============================================================================

RESPUESTAS = {
    # Si mencionan problemas/errores
    "no funciona|error|problem|issue|fail": """
Thanks for trying it! 🙏

Here are the most common fixes:

**1. Python Version**
```bash
python --version  # Needs 3.7+
```

**2. Check File Path**
```bash
# Use absolute path
python auto_debugger_pro.py /full/path/to/project
```

**3. UTF-8 Encoding**
Make sure your test files use UTF-8 encoding.

**4. Test Framework**
Currently supports pytest. Run:
```bash
pip install pytest
```

Still having issues? Share the error message and I'll help! 💪
""",
    
    # Si preguntan por precio/licencia
    "price|cost|expensive|cheap|worth|license": """
Great question! 💰

**What you get for $49:**
- ✅ Full commercial license (unlimited projects)
- ✅ 300+ lines of production code
- ✅ Email support (24h response)
- ✅ Free v1.x updates forever
- ✅ 14-day money-back guarantee

**ROI:** If it saves you 1 hour of debugging = $49+ value

**vs Alternatives:**
- Manual debugging: Free but 10+ hours/week
- DeepCode/Snyk: $29/month subscription
- CodeRabbit: $12/month subscription
- Auto-Debugger Pro: $49 one-time ✅

Buy here: https://ko-fi.com/s/85f18c167d
""",
    
    # Si preguntan cómo funciona
    "how does it work|how it works|explain|algorithm": """
Great question! Here's the technical breakdown: 🔧

**1. Test Execution**
Runs `pytest` and captures all output/errors

**2. Pattern Detection**
Scans for 6 bug patterns:
- HTTP/API errors (status codes, endpoints)
- Boolean False issues (activation flags)
- Validation errors (Pydantic schemas)
- Import errors (missing packages)
- Encoding issues (UTF-8)
- Timeout problems (network calls)

**3. Smart Fixes**
Applies 4 fix types:
- **Blockchain:** Fixes chicken-egg initialization
- **Metacognition:** Adds missing flags
- **Dependencies:** Auto-installs packages
- **Schema:** Repairs validation logic

**4. Iteration**
Repeats 1-10 times until all tests pass

**5. Reporting**
Shows before/after, time saved, fixes applied

GitHub: https://github.com/nelson753/auto-debugger-pro
""",
    
    # Si preguntan por frameworks soportados
    "fastapi|flask|django|pytorch|framework|support": """
Good question! Here's what's supported: 🎯

**Web Frameworks:**
- ✅ FastAPI (HTTP errors, validation, endpoints)
- ✅ Flask (routes, templates, blueprints)
- ✅ Django (models, views, tests)

**ML Frameworks:**
- ✅ PyTorch (tensor errors, CUDA issues)
- ✅ TensorFlow (basic support)
- ✅ Pydantic (schema validation)

**Test Frameworks:**
- ✅ Pytest (primary support)
- ⚠️ Unittest (partial support)

**Coming in v1.1:**
- Selenium/web scraping
- Custom fix patterns
- Multi-language (JavaScript, Java)

What framework are you using? 🤔
""",
    
    # Si muestran interés/curiosidad
    "interesting|cool|nice|awesome|great": """
Thanks! Glad you like it! 🙌

**Try it yourself:**
1. Get it: https://ko-fi.com/s/85f18c167d
2. Run: `python auto_debugger_pro.py your_project`
3. Watch it fix bugs automatically

**Real results:**
- NeuroSys: 43% → 100% (5 hours saved)
- AGI Phoenix: 0 → 100% (2 hours saved)
- LegalAssistant: 0 → 100% (3 hours saved)

Questions? Ask away! 💬
""",
    
    # Si preguntan por GitHub/código
    "github|code|source|open source|repo": """
Good question! 📦

**GitHub:** https://github.com/nelson753/auto-debugger-pro
- Full README with examples
- Real-world results table
- Technical documentation

**Is it open source?**
No, it's a **commercial product** ($49) with:
- ✅ Full commercial license
- ✅ Modify source code
- ✅ Unlimited projects
- ❌ No redistribution (single developer)

**Why not open source?**
Took 100+ hours to build + test on 7 real projects. The $49 helps fund:
- Email support
- v1.1 features (Git auto-commit, Slack notifications)
- New framework support

Questions? Happy to help! 🚀
""",
    
    # Si mencionan alternativas/competidores
    "alternative|instead|better|comparison|vs": """
Fair question! Here's how it compares: ⚖️

**Auto-Debugger Pro ($49 one-time):**
- ✅ Fixes bugs automatically (not just detection)
- ✅ Works offline (no API calls)
- ✅ Unlimited usage
- ✅ Python-specific (deep integration)

**DeepCode/Snyk ($29/month):**
- ❌ Only detects issues (doesn't fix)
- ❌ Requires internet
- ❌ Subscription model
- ✅ Multi-language

**CodeRabbit ($12/month):**
- ❌ GitHub PR reviews only
- ❌ Doesn't run tests
- ❌ Subscription
- ✅ Good for teams

**GitHub Copilot ($10/month):**
- ❌ Suggests fixes (manual application)
- ❌ Doesn't run tests
- ❌ Subscription
- ✅ Multi-language

**Auto-Debugger Pro is best for:**
- Solo Python devs
- One-time payment preference
- Automatic fixes (not just suggestions)

Questions? Ask! 💬
""",
}

# ============================================================================
# FUNCIONES DEL BOT
# ============================================================================

def get_article_id():
    """Obtiene el ID numérico del artículo desde el slug"""
    url = f"https://dev.to/api/articles/{USERNAME}/{ARTICLE_SLUG}"
    headers = {"api-key": DEVTO_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("id")
    except Exception as e:
        print(f"❌ Error obteniendo artículo: {e}")
        return None

def get_article_comments():
    """Obtiene todos los comentarios del artículo"""
    article_id = get_article_id()
    if not article_id:
        return []
    
    url = f"https://dev.to/api/comments?a_id={article_id}"
    headers = {"api-key": DEVTO_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error obteniendo comentarios: {e}")
        return []

def encontrar_respuesta(comment_text):
    """Encuentra la mejor respuesta basada en palabras clave"""
    comment_lower = comment_text.lower()
    
    for keywords, response in RESPUESTAS.items():
        # Divide keywords por |
        keyword_list = keywords.split("|")
        if any(keyword in comment_lower for keyword in keyword_list):
            return response
    
    # Respuesta genérica si no hay match
    return """
Thanks for your comment! 🙏

I'm here to help! Could you share more details about:
- What you're trying to do?
- Any error messages?
- Your Python version?

Also check out:
- GitHub: https://github.com/nelson753/auto-debugger-pro
- Get it: https://ko-fi.com/s/85f18c167d

Happy to assist! 💪
"""

def responder_comentario(comment_id, response_text):
    """Responde a un comentario"""
    url = f"https://dev.to/api/comments"
    headers = {
        "api-key": DEVTO_API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "comment": {
            "body_markdown": response_text,
            "commentable_id": comment_id,
            "commentable_type": "Comment"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Error respondiendo: {e}")
        return False

def cargar_respondidos():
    """Carga IDs de comentarios ya respondidos"""
    try:
        with open("respondidos.json", "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def guardar_respondido(comment_id):
    """Guarda ID de comentario respondido"""
    respondidos = cargar_respondidos()
    respondidos.add(comment_id)
    with open("respondidos.json", "w") as f:
        json.dump(list(respondidos), f)

def monitor_loop():
    """Loop principal del bot"""
    print("🤖 DEV.TO MONITOR BOT - INICIADO")
    print("=" * 60)
    print(f"📝 Artículo: {ARTICLE_SLUG}")
    print(f"👤 Usuario: {USERNAME}")
    print(f"⏰ Iniciado: {datetime.now()}")
    print("=" * 60)
    
    if DEVTO_API_KEY == "TU_API_KEY_AQUI":
        print("\n⚠️ ERROR: Necesitas configurar tu API Key")
        print("👉 Ve a: https://dev.to/settings/extensions")
        print("👉 Genera un API Key")
        print("👉 Cópialo en la línea 16 de este archivo")
        return
    
    respondidos = cargar_respondidos()
    
    while True:
        try:
            print(f"\n🔍 Verificando comentarios... ({datetime.now().strftime('%H:%M:%S')})")
            
            comments = get_article_comments()
            nuevos = 0
            
            for comment in comments:
                comment_id = comment.get("id_code")
                author = comment.get("user", {}).get("username")
                body = comment.get("body_markdown", "")
                
                # No responderse a sí mismo
                if author == USERNAME:
                    continue
                
                # Ya respondido?
                if comment_id in respondidos:
                    continue
                
                print(f"\n💬 Nuevo comentario de @{author}")
                print(f"📄 Contenido: {body[:100]}...")
                
                # Encontrar mejor respuesta
                respuesta = encontrar_respuesta(body)
                
                # Espera 5-10 segundos (parecer humano)
                wait_time = 7
                print(f"⏳ Esperando {wait_time}s antes de responder...")
                time.sleep(wait_time)
                
                # Responder
                if responder_comentario(comment_id, respuesta):
                    print(f"✅ Respondido exitosamente")
                    guardar_respondido(comment_id)
                    nuevos += 1
                else:
                    print(f"❌ Error al responder")
            
            if nuevos == 0:
                print("   No hay comentarios nuevos")
            else:
                print(f"\n🎉 {nuevos} comentario(s) respondido(s)")
            
            # Espera 5 minutos antes de volver a verificar
            print(f"\n😴 Durmiendo 5 minutos...")
            time.sleep(300)  # 5 minutos
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Bot detenido por usuario")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            print("⏳ Reintentando en 1 minuto...")
            time.sleep(60)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    monitor_loop()
