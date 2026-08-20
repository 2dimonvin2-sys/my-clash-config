import urllib.request
import re
import os
from urllib.parse import urlparse, parse_qs, unquote

# Сюда закидываем вообще любые базы (включая новую с Base64 и vmess)
complex_raw_urls = [
    #"https://githubusercontent.com",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vless_configs.txt",
    "https://raw.githubusercontent.com/flaafix/AetrisVPN/refs/heads/main/AetrisVPN.txt",
    "https://raw.githubusercontent.com/bobrinaw/vlessforu/refs/heads/main/working_configs.txt",
    #"https://vlessfo.ru"
]

print("=== 🧪 ЗАПУСК АВТОНОМНОГО ДЕКОДЕРА БАЗ ===")
clean_vless_links = []

for url in complex_raw_urls:
    try:
        print(f"🔄 Сканирую источник: {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as res:
            content = res.read().decode("utf-8", errors="ignore")
        
        # Всеядный поиск: выковыриваем vless, ss, trojan
        found = re.findall(r'((?:vless|ss|trojan)://[^\s"\'<>`]+)', content)
        
        for link in found:
            try:
                # ИСПРАВЛЕНО: Принудительно декодируем %40 в @, %2F в / прямо на лету!
                clean_link = unquote(link.strip())
                
                parsed = urlparse(clean_link)
                if parsed.scheme == "vless":
                    params = parse_qs(parsed.query)
                    # Железный щит: выкидываем кривой REALITY мусор без ключа pbk
                    if "sid" in params and "pbk" not in params:
                        continue
                        
                clean_vless_links.append(clean_link)
            except:
                continue


# Сохраняем чистый список локально
with open("pure_raw_proxies.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(clean_vless_links))

print(f"📦 ДЕКОДЕР СФОРМИРОВАЛ: {len(clean_vless_links)} чистых ссылок.")
