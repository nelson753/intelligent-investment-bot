#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 CONTENT ARBITRAGE BOT v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bot Autónomo de Arbitraje de Contenido

ESTRATEGIA:
1. Encuentra repos GitHub infravalorados (buen código, 0 marketing)
2. Analiza potencial de ganancia (ROI calculator)
3. Transforma con AI (docs, videos, marketing)
4. Publica en Ko-fi/Gumroad a 10x precio

OBJETIVO: Generar ingresos pasivos automáticamente
"""

import requests
import json
import os
import time
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# GitHub Personal Access Token (opcional, aumenta rate limit)
# Obtén uno en: https://github.com/settings/tokens
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)

# Criterios de búsqueda
SEARCH_CRITERIA = {
    "min_stars": 10,           # Mínimo de estrellas (tiene tracción)
    "max_stars": 100,          # Máximo de estrellas (no muy popular)
    "min_forks": 2,            # Al menos algunos forks
    "languages": ["Python", "JavaScript", "TypeScript", "Go", "Rust"],
    "licenses": ["MIT", "Apache-2.0", "BSD"],  # Licencias comerciales OK
    "topics": ["api", "cli", "tool", "automation", "scraper", "bot"],
    "exclude_archived": True,
    "exclude_fork": True,
    "updated_last_months": 6   # Activo recientemente
}

# Precio estimado por tipo de proyecto
PRICING_STRATEGY = {
    "api": {"base": 79, "premium": 199},
    "cli": {"base": 49, "premium": 129},
    "tool": {"base": 59, "premium": 149},
    "automation": {"base": 89, "premium": 229},
    "scraper": {"base": 69, "premium": 179},
    "bot": {"base": 99, "premium": 249},
    "default": {"base": 49, "premium": 99}
}

# Directorio para guardar oportunidades
OPPORTUNITIES_DIR = "arbitrage_opportunities"

# Affiliate Programs (Zero-Friction Income Model)
AFFILIATE_PROGRAMS = {
    "railway": {
        "name": "Railway",
        "commission": "$5-10 per signup",
        "link_template": "https://railway.app?referralCode=YOUR_CODE",
        "use_cases": ["deployment", "hosting", "backend", "api", "database"]
    },
    "vercel": {
        "name": "Vercel",
        "commission": "$10-20 per paid conversion",
        "link_template": "https://vercel.com/?via=YOUR_CODE",
        "use_cases": ["frontend", "nextjs", "react", "deployment", "serverless"]
    },
    "sentry": {
        "name": "Sentry",
        "commission": "20% lifetime",
        "link_template": "https://sentry.io/signup/?ref=YOUR_CODE",
        "use_cases": ["error-tracking", "monitoring", "debugging", "production"]
    },
    "digitalocean": {
        "name": "DigitalOcean",
        "commission": "$25 per signup",
        "link_template": "https://m.do.co/c/YOUR_CODE",
        "use_cases": ["vps", "hosting", "cloud", "infrastructure"]
    },
    "stripe": {
        "name": "Stripe",
        "commission": "$0-$10k per integration",
        "link_template": "https://stripe.com/?partner=YOUR_CODE",
        "use_cases": ["payments", "ecommerce", "billing", "subscriptions"]
    }
}

# RL Agent Configuration
RL_CONFIG = {
    "learning_rate": 0.1,
    "discount_factor": 0.9,
    "epsilon": 0.2,  # Exploration rate
    "min_samples_for_learning": 10,  # Mínimo de datos antes de aprender
    "reward_signals": {
        "sale": 100,           # Venta realizada
        "no_sale": -10,        # No hubo venta
        "high_traffic": 20,    # Mucho tráfico pero no venta (interés)
        "low_traffic": -5,     # Poco tráfico (mal keyword/pricing)
    }
}

# ============================================================================
# GITHUB SCANNER
# ============================================================================

class GitHubScanner:
    """Escanea GitHub buscando repos infravalorados"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def search_repos(self, query: str, per_page: int = 30) -> List[Dict]:
        """Busca repositorios en GitHub"""
        url = "https://api.github.com/search/repositories"
        params = {
            "q": query,
            "sort": "updated",
            "order": "desc",
            "per_page": per_page
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])
        except Exception as e:
            print(f"❌ Error buscando repos: {e}")
            return []
    
    def get_repo_details(self, owner: str, repo: str) -> Optional[Dict]:
        """Obtiene detalles completos de un repositorio"""
        url = f"https://api.github.com/repos/{owner}/{repo}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error obteniendo detalles de {owner}/{repo}: {e}")
            return None
    
    def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """Obtiene el README del repositorio"""
        url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Decodificar contenido base64
            import base64
            content = base64.b64decode(data["content"]).decode("utf-8")
            return content
        except Exception as e:
            return None
    
    def build_search_queries(self) -> List[str]:
        """Construye queries de búsqueda basadas en criterios"""
        queries = []
        
        for lang in SEARCH_CRITERIA["languages"]:
            for topic in SEARCH_CRITERIA["topics"]:
                query_parts = [
                    f"language:{lang}",
                    f"topic:{topic}",
                    f"stars:{SEARCH_CRITERIA['min_stars']}..{SEARCH_CRITERIA['max_stars']}",
                    f"forks:>={SEARCH_CRITERIA['min_forks']}"
                ]
                
                if SEARCH_CRITERIA["exclude_archived"]:
                    query_parts.append("archived:false")
                
                if SEARCH_CRITERIA["exclude_fork"]:
                    query_parts.append("fork:false")
                
                # Licencias
                license_query = " OR ".join([f"license:{lic}" for lic in SEARCH_CRITERIA["licenses"]])
                query_parts.append(f"({license_query})")
                
                queries.append(" ".join(query_parts))
        
        return queries

# ============================================================================
# OPPORTUNITY ANALYZER
# ============================================================================

class OpportunityAnalyzer:
    """Analiza potencial de ganancia de un repo"""
    
    def analyze_repo(self, repo: Dict, readme: Optional[str]) -> Dict:
        """Analiza un repositorio y calcula ROI potencial"""
        
        analysis = {
            "repo_name": repo["full_name"],
            "url": repo["html_url"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "topics": repo.get("topics", []),
            "license": repo.get("license", {}).get("spdx_id", "Unknown"),
            "description": repo.get("description", ""),
            "last_update": repo["updated_at"],
            "has_readme": readme is not None,
            "readme_length": len(readme) if readme else 0,
            
            # Scoring
            "quality_score": 0,
            "opportunity_score": 0,
            "estimated_work_hours": 0,
            "estimated_price": 0,
            "estimated_revenue": 0,
            "roi_percentage": 0,
            
            # Improvement plan
            "improvements_needed": [],
            "value_adds": []
        }
        
        # Calcular quality score (0-100)
        quality_score = 0
        
        # Stars/forks ratio
        if repo["forks_count"] > 0:
            ratio = repo["stargazers_count"] / repo["forks_count"]
            quality_score += min(ratio * 2, 20)  # Max 20 puntos
        
        # README quality
        if readme:
            if len(readme) > 500:
                quality_score += 15
            if "##" in readme:  # Tiene secciones
                quality_score += 10
            if "```" in readme:  # Tiene ejemplos de código
                quality_score += 10
        
        # Topics (indica buena categorización)
        quality_score += min(len(repo.get("topics", [])) * 5, 20)
        
        # License comercial
        if repo.get("license", {}).get("spdx_id") in ["MIT", "Apache-2.0", "BSD-3-Clause"]:
            quality_score += 15
        
        # Descripción clara
        if repo.get("description") and len(repo["description"]) > 30:
            quality_score += 10
        
        analysis["quality_score"] = min(quality_score, 100)
        
        # Calcular opportunity score (potencial de mejora)
        opportunity_score = 0
        improvements = []
        
        # README pobre pero código bueno
        if readme and len(readme) < 1000 and repo["stargazers_count"] > 20:
            opportunity_score += 30
            improvements.append("Mejorar README (agregar instalación, ejemplos, casos de uso)")
        
        # Sin video/screenshots
        if readme and "![" not in readme and ".gif" not in readme.lower():
            opportunity_score += 20
            improvements.append("Agregar screenshots/GIFs demostrando funcionalidad")
        
        # Sin docs completas
        if readme and "documentation" not in readme.lower() and "docs" not in readme.lower():
            opportunity_score += 25
            improvements.append("Crear documentación completa (API reference, guías)")
        
        # Poca visibilidad pero buen código
        if repo["stargazers_count"] < 50 and quality_score > 50:
            opportunity_score += 30
            improvements.append("Marketing y SEO (mejor descripción, keywords, tags)")
        
        # Sin ejemplos de uso
        if readme and "example" not in readme.lower() and "usage" not in readme.lower():
            opportunity_score += 15
            improvements.append("Agregar ejemplos de uso y casos reales")
        
        analysis["opportunity_score"] = min(opportunity_score, 100)
        analysis["improvements_needed"] = improvements
        
        # Determinar tipo de proyecto
        project_type = "default"
        for topic in repo.get("topics", []):
            if topic in PRICING_STRATEGY:
                project_type = topic
                break
        
        pricing = PRICING_STRATEGY.get(project_type, PRICING_STRATEGY["default"])
        
        # Estimar horas de trabajo
        work_hours = len(improvements) * 2  # 2 horas por mejora
        analysis["estimated_work_hours"] = work_hours
        
        # Estimar precio de venta (base + premium si es muy bueno)
        if quality_score > 70:
            analysis["estimated_price"] = pricing["premium"]
        else:
            analysis["estimated_price"] = pricing["base"]
        
        # Estimar revenue (conservador: 3-5 ventas primer mes)
        estimated_sales = 3 if quality_score < 60 else 5
        analysis["estimated_revenue"] = analysis["estimated_price"] * estimated_sales
        
        # Calcular ROI (asumiendo $0 costo de adquisición - repo gratis)
        # Costo = trabajo (work_hours * $20/hora asumido)
        labor_cost = work_hours * 20
        analysis["roi_percentage"] = ((analysis["estimated_revenue"] - labor_cost) / labor_cost * 100) if labor_cost > 0 else 0
        
        # Value adds específicos
        value_adds = []
        if repo["language"] == "Python":
            value_adds.extend([
                "Agregar type hints completos",
                "Crear package para PyPI",
                "Docker container ready-to-use"
            ])
        elif repo["language"] in ["JavaScript", "TypeScript"]:
            value_adds.extend([
                "Crear NPM package",
                "Agregar TypeScript definitions",
                "Webpack/Vite build optimizado"
            ])
        
        value_adds.extend([
            "Video tutorial de 5 minutos",
            "Guía de deployment (Heroku/Railway/Vercel)",
            "Traducciones (ES, FR, DE, PT, JP)"
        ])
        
        analysis["value_adds"] = value_adds
        
        return analysis

# ============================================================================
# REPORT GENERATOR
# ============================================================================

class ReportGenerator:
    """Genera reportes de oportunidades encontradas"""
    
    @staticmethod
    def generate_markdown_report(opportunities: List[Dict], filename: str = None):
        """Genera reporte en Markdown"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"arbitrage_report_{timestamp}.md"
        
        # Ordenar por ROI
        opportunities.sort(key=lambda x: x["roi_percentage"], reverse=True)
        
        report = f"""# 🤖 Content Arbitrage Report
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Opportunities Found:** {len(opportunities)}

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Opportunities | {len(opportunities)} |
| Avg Quality Score | {sum(o['quality_score'] for o in opportunities) / len(opportunities):.1f} |
| Avg Opportunity Score | {sum(o['opportunity_score'] for o in opportunities) / len(opportunities):.1f} |
| Total Est. Revenue | ${sum(o['estimated_revenue'] for o in opportunities):,} |
| Avg ROI | {sum(o['roi_percentage'] for o in opportunities) / len(opportunities):.1f}% |

---

## 🎯 Top Opportunities

"""
        
        # Top 10 oportunidades
        for i, opp in enumerate(opportunities[:10], 1):
            report += f"""
### {i}. [{opp['repo_name']}]({opp['url']})

**Language:** {opp['language']} | **Stars:** ⭐ {opp['stars']} | **Forks:** 🔱 {opp['forks']}

**Scores:**
- Quality: {opp['quality_score']}/100
- Opportunity: {opp['opportunity_score']}/100

**Financials:**
- Estimated Price: ${opp['estimated_price']}
- Estimated Revenue (3-5 sales): ${opp['estimated_revenue']}
- Work Hours: {opp['estimated_work_hours']}h
- **ROI: {opp['roi_percentage']:.0f}%**

**Improvements Needed:**
"""
            for imp in opp['improvements_needed']:
                report += f"- {imp}\n"
            
            report += "\n**Value Adds:**\n"
            for add in opp['value_adds'][:3]:  # Top 3
                report += f"- {add}\n"
            
            report += "\n---\n"
        
        # Guardar reporte
        os.makedirs(OPPORTUNITIES_DIR, exist_ok=True)
        filepath = os.path.join(OPPORTUNITIES_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📄 Reporte guardado: {filepath}")
        return filepath
    
    @staticmethod
    def generate_json_export(opportunities: List[Dict], filename: str = None):
        """Exporta oportunidades a JSON"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"opportunities_{timestamp}.json"
        
        os.makedirs(OPPORTUNITIES_DIR, exist_ok=True)
        filepath = os.path.join(OPPORTUNITIES_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(opportunities, f, indent=2, ensure_ascii=False)
        
        print(f"💾 JSON guardado: {filepath}")
        return filepath

# ============================================================================
# MAIN BOT
# ============================================================================

class ContentArbitrageBot:
    """Bot principal de arbitraje de contenido"""
    
    def __init__(self, github_token: Optional[str] = None):
        self.scanner = GitHubScanner(github_token)
        self.analyzer = OpportunityAnalyzer()
        self.reporter = ReportGenerator()
    
    def run_scan(self, max_repos: int = 50):
        """Ejecuta escaneo completo"""
        
        print("🤖 CONTENT ARBITRAGE BOT - INICIANDO")
        print("=" * 70)
        print(f"⏰ Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Max repos: {max_repos}")
        print("=" * 70)
        
        # Generar queries
        queries = self.scanner.build_search_queries()
        print(f"\n🔍 Queries generadas: {len(queries)}")
        
        all_repos = []
        opportunities = []
        
        # Ejecutar búsquedas
        for i, query in enumerate(queries[:10], 1):  # Límite de 10 queries
            print(f"\n📡 Query {i}/10: {query[:80]}...")
            
            repos = self.scanner.search_repos(query, per_page=10)
            print(f"   Encontrados: {len(repos)} repos")
            
            all_repos.extend(repos)
            time.sleep(2)  # Rate limiting
            
            if len(all_repos) >= max_repos:
                break
        
        # Remover duplicados
        unique_repos = {repo["full_name"]: repo for repo in all_repos}
        print(f"\n✅ Total repos únicos: {len(unique_repos)}")
        
        # Analizar cada repo
        print(f"\n🔬 Analizando oportunidades...")
        
        for i, (name, repo) in enumerate(list(unique_repos.items())[:max_repos], 1):
            print(f"\n[{i}/{min(len(unique_repos), max_repos)}] {name}")
            
            # Obtener README
            owner, repo_name = name.split("/")
            readme = self.scanner.get_readme(owner, repo_name)
            
            # Analizar
            analysis = self.analyzer.analyze_repo(repo, readme)
            
            # Filtrar por scores mínimos
            if analysis["quality_score"] >= 40 and analysis["opportunity_score"] >= 30:
                opportunities.append(analysis)
                print(f"   ✅ Quality: {analysis['quality_score']}/100 | Opportunity: {analysis['opportunity_score']}/100 | ROI: {analysis['roi_percentage']:.0f}%")
            else:
                print(f"   ⏭️ Descartado (Q:{analysis['quality_score']} O:{analysis['opportunity_score']})")
            
            time.sleep(1)  # Rate limiting
        
        # Generar reportes
        print(f"\n📊 RESULTADOS FINALES")
        print("=" * 70)
        print(f"✅ Oportunidades viables: {len(opportunities)}")
        
        if opportunities:
            avg_roi = sum(o["roi_percentage"] for o in opportunities) / len(opportunities)
            total_revenue = sum(o["estimated_revenue"] for o in opportunities)
            
            print(f"💰 Revenue potencial: ${total_revenue:,}")
            print(f"📈 ROI promedio: {avg_roi:.0f}%")
            
            # Top 3
            top3 = sorted(opportunities, key=lambda x: x["roi_percentage"], reverse=True)[:3]
            print(f"\n🏆 TOP 3 OPORTUNIDADES:")
            for i, opp in enumerate(top3, 1):
                print(f"   {i}. {opp['repo_name']} - ROI {opp['roi_percentage']:.0f}% (${opp['estimated_revenue']})")
            
            # Generar reportes
            self.reporter.generate_markdown_report(opportunities)
            self.reporter.generate_json_export(opportunities)
        else:
            print("⚠️ No se encontraron oportunidades viables")
        
        print("\n✅ Escaneo completado")
        return opportunities

# ============================================================================
# CLI
# ============================================================================

def main():
    """Función principal"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║            🤖 CONTENT ARBITRAGE BOT v1.0                             ║
║                                                                       ║
║  Encuentra repos GitHub infravalorados y calcula ROI potencial       ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar bot
    bot = ContentArbitrageBot(github_token=GITHUB_TOKEN)
    
    # Ejecutar escaneo
    opportunities = bot.run_scan(max_repos=30)
    
    if opportunities:
        print(f"\n💡 Revisa los reportes en: {OPPORTUNITIES_DIR}/")
        print(f"📋 Próximo paso: Selecciona la mejor oportunidad y empieza la transformación")

if __name__ == "__main__":
    main()
