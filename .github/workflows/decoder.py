import urllib.request
import re
import base64
from urllib.parse import urlparse, parse_qs, unquote

# Сюда мы можем закидывать ЛЮБЫЕ самые грязные сырые базы из интернета
complex_raw_urls = [
    "https://sub.vlessfo.ru/vlessforu/working_configs.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vless_configs.txt",
    "https://raw.githubusercontent.com/FreeFolksOn/abc-configs-free-vpn-proxy-list/main/README.md",
    #"https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vless_configs.txt"
]

print("=== 🧪 ЗАПУСК ИЗОЛИРОВАННОГО ДЕКОДЕРА БАЗ ===")
clean_vless_links = []

for url in complex_raw_urls:
    try:
        print(f"🔄 Сканирую источник: {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as res:
            content = res.read().decode("utf-8", errors="ignore")
        
        # Ищем абсолютно все типы ссылок на странице
        found = re.findall(r'((?:vless|ss|trojan)://[^\s"\'<>`]+)', content)
        
        for link in found:
            try:
                parsed = urlparse(link.strip())
                # Если это капризный VLESS, принудительно очищаем его от REALITY мусора
                if parsed.scheme == "vless":
                    params = parse_qs(parsed.query)
                    # Если в ссылке сидит short-id без нормального pbk — это виновник наших бед!
                    if "sid" in params and "pbk" not in params:
                        continue # Сразу выкидываем этот сервер в корзину, не пуская дальше!
                
                # Если ссылка прошла проверку, сохраняем её в наш чистый список
                clean_vless_links.append(link.strip())
            except:
                continue
    except Exception as e:
        print(f"❌ Пропуск источника из-за ошибки сети -> {e}")

# Записываем все идеально отфильтрованные сырые прокси в промежуточный файл
with open("pure_raw_proxies.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(clean_vless_links))

print(f"📦 ДЕКОДЕР ЗАВЕРШЕН: Успешно отфильтровано и подготовлено {len(clean_vless_links)} чистых ссылок!")
