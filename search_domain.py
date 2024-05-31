import requests
import json
import urllib3
import ssl

from random import randint

# Hàm thực hiện tìm kiếm domain của công ty
def search_domain(cop: str):
    req = requests.get("https://crt.sh/", params={"O": cop, "output": "json"}, timeout=120)
    if req == []:
        req = resend_request(5, cop)
    results = set()
    try:
        for c in req.json():
            results.add(c["common_name"])
    except json.decoder.JSONDecodeError:
        pass
    return results

# Hàm thực hiện gửi lại request nếu gặp lỗi mạng
def resend_request(total: int, cop: int):
    statusCode = [400, 401, 402, 403, 429, 500, 502, 503, 504]
    for _ in range(total):
        try: 
            response = requests.get("https://crt.sh/", params={"O": cop, "output": "json"}, timeout=120)
            if response.status_code in statusCode:
                continue
            return response
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout, requests.exceptions.SSLError, urllib3.exceptions.SSLError, urllib3.exceptions.MaxRetryError, ssl.SSLEOFError) as error:
            pass
    return None

if __name__ == "__main__":
    cop = input("Nhập tên công ty: ")

    result = search_domain(cop)
    top_level_domain_lst = []
    domain_list = []
    with open("tld.txt", "r") as tld:
        domains = tld.readlines()
        for i in domains:
            top_level_domain_lst.append(i.rstrip("\n"))
        tld.close()
    for CN in result:
        CN = CN.split(".")
        if len(CN) == 1:
            continue
        if CN[-1] in top_level_domain_lst:
            if CN[-2] in top_level_domain_lst:
                domain_list.append("{}.{}.{}".format(CN[-3], CN[-2], CN[-1]))
            else:
                domain_list.append("{}.{}".format(CN[-2], CN[-1]))
    
    for domain in domain_list:
        print(domain)
