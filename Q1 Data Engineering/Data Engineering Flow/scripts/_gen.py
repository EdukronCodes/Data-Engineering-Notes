# Generator - writes provision scripts, seed scripts, ADF JSON, README section
from pathlib import Path
import json

ROOT = Path(r"c:\Users\Admin\Downloads\Healthcare-APP-main\Data Engineering Flow")

def w(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8", newline="\n")
    print("wrote", rel)

# .env.example
w("infra/.env.example", """# Copy to infra/.env.local and fill after provision (do not commit secrets)
AZURE_SUBSCRIPTION_ID=
AZURE_RESOURCE_GROUP=rg-retailde-dev
AZURE_LOCATION=eastus
NAMING_PREFIX=retailde
SQL_ADMIN_PASSWORD=
POSTGRES_ADMIN_PASSWORD=
""")

print("done part1")
