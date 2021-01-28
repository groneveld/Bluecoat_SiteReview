import requests
import json
from PIL import Image
import pytesseract
import simplejson
import calendar
import time
import os
import base64


class SiteReview:
    headers = {
        'authority': 'sitereview.bluecoat.com',
        'accept': 'application/json, text/plain, */*',
        'x-xsrf-token': 'ce6e0505-ed4b-43ef-9624-9a5ad3b70f27',
        'accept-language': 'ru',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://sitereview.bluecoat.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://sitereview.bluecoat.com/',
        'cookie': 'JSESSIONID=FD00E4699288139952D7B9CF25DC6F61; XSRF-TOKEN=ce6e0505-ed4b-43ef-9624-9a5ad3b70f27',
    }

    _headers = {
        'authority': 'sitereview.bluecoat.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'image',
        'referer': 'https://sitereview.bluecoat.com/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'JSESSIONID=FD00E4699288139952D7B9CF25DC6F61; XSRF-TOKEN=ce6e0505-ed4b-43ef-9624-9a5ad3b70f27; __utma=265713933.443691065.1605382266.1605382266.1605382266.1; __utmc=265713933; __utmz=265713933.1605382266.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    }

    def get_captcha_base64(self):
        epoch_timestamp = str(calendar.timegm(time.gmtime()) * 1000)
        captcha_url = 'https://sitereview.bluecoat.com/resource/captcha.jpg?%s' % (epoch_timestamp)
        local_filename = 'captcha.jpg'
        r = requests.get(captcha_url, headers=self._headers, stream=True)

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Мария\AppData\Local\Tesseract-OCR\tesseract.exe'
        captcha = pytesseract.image_to_string(Image.open('captcha.jpg'))
        captcha = "".join(captcha.split())
        os.remove('captcha.jpg')

        captcha_utf = captcha.encode("UTF-8")
        base64_captcha = base64.b64encode(captcha_utf)
        return base64_captcha.decode("utf-8")

    def get_data(self, url: str):
        return json.dumps(
            {"url": url, "captcha": "", "key": "f69e0635f42170328ee88fac4276ffb17a587931f2cd31ad0bdd2759005e0cc2",
             "phrase": "U2NyaXB0aW5nIGFnYWluc3QgU2l0ZSBSZXZpZXcgaXMgYWdhaW5zdCB0aGUgU2l0ZSBSZXZpZXcgVGVybXMgb2YgU2VydmljZQ==",
             "source": ""})

    def captcha_recognize(self):
        captcha = self.get_captcha_base64()
        response = requests.get(f'https://sitereview.bluecoat.com/resource/captcha-request/{captcha}',
                                headers=self._headers)

    def get_category(self, url: str, is_again=False) -> str:
        data = self.get_data(url)
        response = requests.post('https://sitereview.bluecoat.com/resource/lookup', headers=self.headers, data=data)
        if response.status_code == 200:
            return json.loads(response.text)['categorization']
        elif not is_again:
            self.captcha_recognize()
            return self.get_category(url, True)
        else:
            start = time.time()
            time.sleep(5)
            self.captcha_recognize()
            return self.get_category(url, True)
