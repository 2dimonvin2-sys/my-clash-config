import urllib.request
import re
import base64
import os
from urllib.parse import urlparse, parse_qs, unquote

# Наш стандартный список внешних баз
complex_raw_urls = [
    #"https://githubusercontent.com",
    "https://raw.githubusercontent.com/anaer/Sub/main/clash.yaml",
    "https://raw.githubusercontent.com/flaafix/AetrisVPN/refs/heads/main/AetrisVPN.txt",
    "https://raw.githubusercontent.com/bobrinaw/vlessforu/refs/heads/main/working_configs.txt",
    "https://raw.githubusercontent.com/Au1rxx/free-vpn-subscriptions/main/output/clash.yaml"
]

print("=== 🧪 ЗАПУСК ДЕКОДЕРА С СИСТЕМОЙ РУЧНОГО ИМПОРТА v2rayN ===")
clean_vless_links = []

# ШАГ 1: Проверяем ручную папку. Если там лежит файл v2rayN, расшифровываем его первым!
manual_dir = ".github/workflows/manual_proxies"
if os.path.exists(manual_dir):
    for filename in sorted(os.listdir(manual_dir)):
        file_path = os.path.join(manual_dir, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                for line in lines:
                    if not line.strip(): continue
                    clean_link = unquote(line.strip())
                    
                    # Если строка зашифрована приложением v2rayN
                    if clean_link.startswith("v2rayn://vless/"):
                        try:
                            b64_part = clean_link.split("v2rayn://vless/")[-1].split("?")[0]
                            padded_b64 = b64_part + "=" * ((4 - len(b64_part) % 4) % 4)
                            decoded = base64.b64decode(padded_b64).decode("utf-8", errors="ignore")
                            # Если внутри обычная vless строка, забираем её
                            if decoded.startswith("vless://"):
                                clean_vless_links.append(decoded.strip())
                        except: continue
                    elif clean_link.startswith("vless://"):
                        clean_vless_links.append(clean_link)
            except: continue

# ШАГ 2: Добираем остатки из интернета
for url in complex_raw_urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as res:
            content = res.read().decode("utf-8", errors="ignore")
        found = re.findall(r'((?:vless|ss|trojan)://[^\s"\'<>`]+)', content)
        for link in found:
            try:
                clean_link = unquote(link.strip())
                parsed = urlparse(clean_link)
                if parsed.scheme == "vless":
                    params = parse_qs(parsed.query)
                    if "sid" in params and "pbk" not in params: continue
                clean_vless_links.append(clean_link)
            except: continue
    except: continue

with open("pure_raw_proxies.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(clean_vless_links))
print(f"📦 ДЕКОДЕР ЗАВЕРШЕН: Подготовлено {len(clean_vless_links)} чистых строк.")
