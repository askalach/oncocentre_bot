import requests

import settings
from io import BytesIO
from bs4 import BeautifulSoup


class DataLoader:
    def __init__(self, url: str):
        self.base_url = url
        self.treats_url = self.base_url + '/ru/my/treats/'

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'my.oncocentre.ru',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Accept-Language': 'ru',
            'Referer': 'http://oncocentre.ru/profile-helper/',
            'Connection': 'keep-alive'
        }
        self.cookies = {
            'healthid_lang': settings.HEALTHID_LANG,
            'lhc_per': settings.LHC_PER,
            '_ym_visorc': settings._YM_VISORC,
            '_ga': settings._GA,
            '_gid': settings._GID,
            '_ym_isad': settings._YM_ISAD,
            '_ym_d': settings._YM_D,
            '_ym_uid': settings._YM_UID,
            'healthid': settings.HEALTHID
        }


    def get_meta(self, raw_html_data) -> dict:
        resault = {}

        resault['name'] = raw_html_data.find('strong', class_='text-overflow-ellipsis font-size-14').text
        raw_teg_a = raw_html_data.find('a', class_='font-size-14 font-red treat-click')
        resault['protocolid'] = raw_teg_a['data-protocolid']
        resault['treat_code'] = raw_teg_a['data-treat-code']
        resault['treat_company_id'] = raw_teg_a['data-treat-company-id']
        resault['treat_hash'] = raw_teg_a['data-treat-hash']
        resault['treat_place'] = raw_teg_a['data-treat-place']
        resault['href'] = raw_teg_a['href']
        resault['author'] = raw_html_data.find_all('div', class_='col-md-4 d-none d-sm-block')[0].text.strip()
        resault['date'] = raw_html_data.find_all('div', class_='col-md-4 d-none d-sm-block')[1].contents[0].strip()
        
        # for k, v in resault.items():
        #     print(f'{k}: {v}')

        return resault


    def save_to_file(self, link: str, name: str):
        with open('data/' + name + '.pdf', 'wb') as file:
            file.write(requests.get(self.base_url+link, headers=self.headers, cookies=self.cookies).content)
            print(name + '.pdf - ok!')
        return file


    def get_byte_object(self, link: str, name: str):
        buf = BytesIO(requests.get(self.base_url+link, headers=self.headers, cookies=self.cookies).content)
        buf.name = name + '.pdf'
        return buf

    def get_data(self):
        # fetching the url, raising error if operation fails
        
        resault = []
        
        try:
            response = requests.get(url=self.treats_url, headers=self.headers, cookies=self.cookies)
            print(response.status_code)
        except requests.exceptions.RequestException as e:
            print(e)
            exit()       
        
        soup = BeautifulSoup(response.text, 'lxml')

        items = soup.find_all('div', class_='row margin-bottom-15')

        for item in items:
            resault.append(self.get_meta(item))

        # notification = soup.find('form', id='SystemNotification')
        # if notification:
        #     print(notification.prettify())

        return resault


def main():
    dl = DataLoader(settings.URL)
    for count, item in enumerate(dl.get_data()):
        print(count, item)


if __name__ == '__main__':
    main()
