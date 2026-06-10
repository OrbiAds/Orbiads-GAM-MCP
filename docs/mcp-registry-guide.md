# Soumettre OrbiAds au registre officiel MCP

**Registre** : https://registry.modelcontextprotocol.io  
**Manifest** : `orbiads/server.json` (racine du repo public `OrbiAds/Orbiads-GAM-MCP`)

---

## Méthode choisie : DNS (recommandée)

Le nom du serveur `com.orbiads/gam` est en reverse-DNS du domaine `orbiads.com`.  
L'auth DNS prouve la propriété du domaine → crédibilité maximale dans le registre.

**Alternative GitHub** : si tu préfères éviter la config DNS, utilise le nom
`io.github.OrbiAds/Orbiads-GAM-MCP` dans `server.json` et saute l'étape 2.

---

## Étape 1 — Installer mcp-publisher

```powershell
# Windows (PowerShell)
$arch = if ([System.Runtime.InteropServices.RuntimeInformation]::ProcessArchitecture -eq "Arm64") { "arm64" } else { "amd64" }
Invoke-WebRequest -Uri "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_windows_$arch.tar.gz" -OutFile "mcp-publisher.tar.gz"
tar xf mcp-publisher.tar.gz mcp-publisher.exe
Remove-Item mcp-publisher.tar.gz
# Déplacer mcp-publisher.exe dans un dossier du PATH (ex: C:\Windows\System32 ou ~/bin)
```

Vérification :
```powershell
mcp-publisher --help
```

---

## Étape 2 — Générer la clé Ed25519 + ajouter le TXT record DNS

> Requiert OpenSSL 3.0+ (pas la LibreSSL macOS par défaut).
> Sur Windows, OpenSSL est disponible via Git Bash ou `winget install ShiningLight.OpenSSL`.

```bash
# Générer la paire de clés
openssl genpkey -algorithm ed25519 -out mcp-registry-private.pem
openssl pkey -in mcp-registry-private.pem -pubout -out mcp-registry-public.pem

# Afficher la clé publique encodée en base64 (pour le TXT record)
openssl pkey -in mcp-registry-public.pem -pubin -outform DER | base64 -w 0
```

**Ajouter le TXT record DNS sur `orbiads.com` (apex du domaine, pas un sous-domaine) :**

| Type | Nom | Valeur |
|------|-----|--------|
| TXT  | `@` (apex) | `mcp-registry=<base64-de-la-cle-publique>` |

> Dans Firebase Hosting / Google Domains : Manage → DNS → Add Record → TXT → `@`

Attendre la propagation DNS (quelques minutes à 1h) puis vérifier :
```bash
nslookup -type=TXT orbiads.com
# ou
dig TXT orbiads.com +short
```

---

## Étape 3 — S'authentifier

```bash
mcp-publisher login dns --domain orbiads.com --key mcp-registry-private.pem
```

Résultat attendu : `✓ Authenticated as com.orbiads`

> La clé privée `mcp-registry-private.pem` ne doit JAMAIS être committée.
> Ajouter à `.gitignore` : `mcp-registry-private.pem`

---

## Étape 4 — Publier depuis le repo public

```bash
cd path/to/OrbiAds-GAM-MCP   # ou depuis gam-native/orbiads/
mcp-publisher publish
```

Le CLI lit `server.json` dans le répertoire courant et soumet au registre.

Vérification post-publication :
```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=com.orbiads/gam"
```

---

## Étape 5 — Mettre à jour après chaque release

À chaque bump de version dans `version.json`, mettre à jour `server.json` :
- Le champ `version` racine
- Le champ `version` dans `packages[0].version`

Puis republier :
```bash
mcp-publisher publish
```

> Le registre supporte le versioning semver — les anciennes versions restent accessibles.

---

## Contenu du server.json actuel

```json
{
  "name": "com.orbiads/gam",
  "title": "OrbiAds — Google Ad Manager",
  "description": "The most complete MCP server for Google Ad Manager: campaigns, line items, creatives, inventory, targeting, reporting, yield and ad-ops audits — 50 tools covering 290+ GAM operations.",
  "version": "1.9.0",
  "transport": "streamable-http",
  "url": "https://orbiads.com/mcp"
}
```

---

## Notes importantes

**`registryType: mcpb`** — OrbiAds est un serveur HTTP distant (SaaS), pas un paquet installable localement. `mcpb` (MCP Bridge) est le type registre prévu pour les serveurs hébergés. Si le CLI remonte une erreur de validation sur ce champ, essaie de le remplacer par `oci` ou contacte support@modelcontextprotocol.io pour confirmer le type correct pour les serveurs HTTP SaaS.

**Auth OAuth** — Le serveur implémente MCP OAuth 2.0 complet (RFC 9728). Les utilisateurs s'authentifient via `https://orbiads.com/mcp` → flow Google OAuth → session persistante. Aucune clé API à passer manuellement.

**Glama.ai** — OrbiAds est déjà indexé sur Glama. Le registre officiel MCP est distinct et plus impactant (source d'autodécouverte par défaut pour Claude Desktop/Code).
