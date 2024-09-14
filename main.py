from extract_politicians_info_nrw import extract_mdl_info

if __name__ == "__main__":
    mdl_info_list = extract_mdl_info()
    for mdl_info in mdl_info_list:
        print(mdl_info)
        print(len(mdl_info_list))

import requests

response= requests.get('https://chatgpt.com/c/66e4cdea-3084-8006-9b19-34d36069327b')
#print(response.text)