import urllib.request
import re
from urllib.parse import urlparse, parse_qs, unquote

# Наш полный список скрытых сырых баз
complex_raw_urls = [
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/anaer/Sub/main/clash.yaml",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vless_configs.txt",
    "https://raw.githubusercontent.com/FreeFolksOn/abc-configs-free-vpn-proxy-list/main/README.md",
    "https://raw.githubusercontent.com/flaafix/AetrisVPN/refs/heads/main/AetrisVPN.txt",
    "https://raw.githubusercontent.com/bobrinaw/vlessforu/refs/heads/main/working_configs.txt"
          ]
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
                # МГНОВЕННО очищаем ссылку от %40 (@) и %2F (/) перед любым анализом
                clean_link = unquote(link.strip())
                
                parsed = urlparse(clean_link)
                if parsed.scheme == "vless":
                    params = parse_qs(parsed.query)
                    # Наш железный щит против кривого REALITY мусора
                    if "sid" in params and "pbk" not in params:
                        continue
                        
                clean_vless_links.append(clean_link)
            except:
                continue
    except Exception as e:
        print(f"❌ Ошибка сети на источнике -> {e}")

# ЗАПИСЬ ФАЙЛА (строго вне цикла и на самом левом краю экрана!)
with open("pure_raw_proxies.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(clean_vless_links))

print(f"📦 ДЕКОДЕР УСПЕШНО СФОРМИРОВАЛ: {len(clean_vless_links)} чистых ссылок без знаков % !")
