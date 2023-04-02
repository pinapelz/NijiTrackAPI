import urllib.request

def get_url(url):
    with urllib.request.urlopen(url) as f:
        return f.read()

print(get_url("https://nijitrackerapi-pinapelz.pythonanywhere.com/subs/UCIM92Ok_spNKLVB5TsgwseQ"))