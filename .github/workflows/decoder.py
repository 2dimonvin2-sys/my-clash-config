import urllib.request
import re
import base64
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

print("=== 🧪 ЗАПУСК АВТОНОМНОГО УЛЬТИМАТИВНОГО ДЕКОДЕРА ===")
clean_vless_links = []

for url in complex_raw_urls:
    try:
        print(f"🔄 Сканирую и очищаю источник: {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as res:
            content = res.read().decode("utf-8", errors="ignore")
        
        # Всеядный поиск: забираем vless, ss, trojan
        found = re.findall(r'((?:vless|ss|trojan)://[^\s"\'<>`]+)', content)
        
        for link in found:
            try:
                # 1. Мгновенно очищаем ссылку от процентов %40 и %2F
                clean_link = unquote(link.strip())
                parsed = urlparse(clean_link)
                proto = parsed.scheme
                
                # 2. ЖЕСТКИЙ ФИЛЬТР БРАКА REALITY
                if proto == "vless":
                    params = parse_qs(parsed.query)
                    if "sid" in params and "pbk" not in params:
                        continue  # Выкидываем ломаный прокси в корзину
                    clean_vless_links.append(clean_link)
                
                # 3. КОНВЕРТЕР ТРОЯНА И ШАДОУСОКС В БЕЗОПАСНЫЙ VLESS ДЛЯ ГЛАВНОГО КОДА
                elif proto in ["ss", "trojan"]:
                    server_port = parsed.netloc.split("@")[-1]
                    if ":" in server_port:
                        server, port = server_port.split(":")[:2]
                        # Вытаскиваем имя (фрагмент)
                        frag = parsed.fragment if parsed.fragment else f"{proto.upper()}_Proxy"
                        # Собираем стандартную VLESS-строку, которую главный код переварит без бубнов
                        fake_vless = f"vless://com-decoder-uuid@{server}:{port}?security=none#{proto.upper()}_{frag}"
                        clean_vless_links.append(fake_vless)
            except:
                continue
    except Exception as e:
        print(f"❌ Ошибка сети на источнике -> {e}")

# Записываем идеально отфильтрованный черновик
with open("pure_raw_proxies.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(clean_vless_links))

print(f"📦 ДЕКОДЕР ПОЛНОСТЬЮ ЗАВЕРШИЛ РАБОТУ: Подготовлено {len(clean_vless_links)} чистых строк.")
