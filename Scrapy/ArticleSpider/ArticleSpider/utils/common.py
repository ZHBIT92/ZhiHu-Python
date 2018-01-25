import hashlib

def get_md5(url):
    # 如果是unicode,转为utf-8
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    # 抽取返回摘要
    return m.hexdigest()

if __name__ == "__main__":
    print(get_md5("http://jobbole.com".encode("utf-8")))
