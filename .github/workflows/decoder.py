import urllib.request
import re
import base64
from urllib.parse import urlparse, parse_qs, unquote

# Наш полный список скрытых сырых баз
complex_raw_urls = [
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/anaer/Sub/main/clash.yaml",
    "https://raw.githubusercontent.com/Au1rxx/free-vpn-subscriptions/main/output/clash.yaml"
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vless_configs.txt",
    "https://raw.githubusercontent.com/FreeFolksOn/abc-configs-free-vpn-proxy-list/main/README.md",
    "https://raw.githubusercontent.com/flaafix/AetrisVPN/refs/heads/main/AetrisVPN.txt",
    "https://raw.githubusercontent.com/bobrinaw/vlessforu/refs/heads/main/working_configs.txt"
]

print("=== 🧪 ЗАПУСК УЛЬТИМАТИВНОГО ДЕКОДЕРА БАЗ ===")
clean_vless_links = []

for url in complex_raw_urls:
    try:
        print(f"🔄 Сканирую источник: {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as res:
            content = res.read().decode("utf-8", errors="ignore")
        
        if "proxies:" in content or "- name:" in content:
            lines = content.split("\n")
            current_proxy = []
            for line in lines:
                if line.strip().startswith("- name:"):
                    if current_proxy:
                        proxy_str = "\n".join(current_proxy)
                        if "type: vless" not in proxy_str and "type: trojan" not in proxy_str:
                            encoded_block = base64.b64encode(proxy_str.encode("utf-8")).decode("utf-8")
                            clean_vless_links.append(f"yaml-direct://{encoded_block}#RAW_YAML")
                    current_proxy = [line]
                elif current_proxy:
                    current_proxy.append(line)
        else:
            found = re.findall(r'((?:vless|ss|trojan)://[^\s"\'<>`]+)', content)
            for link in found:
                try:
                    clean_link = unquote(link.strip())
                    parsed = urlparse(clean_link)
                    proto = parsed.scheme
                    
                    if proto == "vless":
                        params = parse_qs(parsed.query)
                        if "sid" in params and "pbk" not in params:
                            continue
                        clean_vless_links.append(clean_link)
                    elif proto in ["ss", "trojan"]:
                        server_port = parsed.netloc.split("@")[-1]
                        if ":" in server_port:
                            server, port = server_port.split(":")[:2]
                            frag = parsed.fragment if parsed.fragment else f"{proto.upper()}_Proxy"
                            clean_vless_links.append(f"vless://com-decoder-uuid@{server}:{port}?security=none#{proto.upper()}_{frag}")
                except: continue
    except Exception as e:
        print(f"❌ Ошибка сети на источнике -> {e}")

with open("pure_raw_proxies.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(clean_vless_links))

print(f"📦 ДЕКОДЕР СФОРМИРОВАЛ: {len(clean_vless_links)} чистых строк.")

print(f"📦 ДЕКОДЕР ПОЛНОСТЬЮ ЗАВЕРШИЛ РАБОТУ: Подготовлено {len(clean_vless_links)} чистых строк.")
