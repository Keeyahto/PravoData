"""
В классе Configs указываются все основные настройки для скачивания документов.
"""
import pathlib
import json
from pathlib import Path
import urllib.parse



class StartLinkCreator:
    def __init__(self, **kwargs):
        self.base_url = 'http://pravo.gov.ru/proxy/ips/'
        self.region_code = self.get_region_code(kwargs.get('region')) #Возвращает список регионов для подключения БПА, кодировать через /, bpas
        self.org_code = '' #self.get_organization_code(kwargs.get('organization')) #Список организаций, кодировать через ;, v6, v6type=1
        self.from_date = kwargs.get('from_date') or '26.10.1917'
        self.to_date = kwargs.get('to_date') or '24.05.2023'
        self.name = kwargs.get('name') or '' #a1
        self.text = kwargs.get('text') or ''


    def get_start_link(self):
        base_params = {'bpas': '', 'v3': '', 'v3type': '1', 'v3value': '', 'a6': '', 'a6type': '1', 'a6value': '',
                       'a15': '', 'a15type': '1', 'a15value': '', 'a7type': '3', 'a7from': '', 'a7to': '', 'a7date': '',
                       'a8': '', 'a8type': '1', 'a1': '', 'a0': '', 'a16': '', 'a16type': '1', 'a16value': '', 'a17': '',
                       'a17type': '1', 'a17value': '', 'a4': '', 'a4type': '1', 'a4value': '', 'a23': '', 'a23type': '1',
                       'a23value': '', 'textpres': '', 'sort': '7', 'x': '48', 'y': '8', 'lstsize': '200', 'start': '0'}

        # base_params = {'bpas':'', 'a3type': '1', 'a6type': '1', 'a15type': '1', 'a7type': '4', 'a7from': '', 'a7to': '', 'a8type': '1', 'a0': '', 'a16type': '1', 'a17type': '1', 'a4type': '1', 'a23type': '1', 'sort': '7','lstsize': '200', 'start': '0' }


        user_params = {'a7type': '4', 'bpas': '/'.join(self.region_code).encode('cp1251'), "a6": ';'.join(self.org_code).encode('cp1251') or '',
                       'a6value': ';'.join(self.org_code).encode('cp1251'), 'a7from': self.from_date,
                       'a7to': self.to_date, 'a0': self.text, 'a1': self.name,
                       }
        base_params.update(user_params)
        encoded_params = urllib.parse.urlencode(base_params, encoding='cp1251')
        url = self.base_url + '?searchlist=&' + encoded_params
        return url



    def get_region_code(self, region):
        '''находит айди региона. напр - Брянская область == 'r013200' '''
        with open(Path(__file__).parent / 'regions_n_their_numbers.json', encoding='utf-8') as f:
                codes = json.load(f)
                if region is None:
                    regions = []
                    for reg_code in codes.values():
                        regions.append(reg_code)
                    return regions
                elif isinstance(region, str) and len(region.split(',')) > 1:
                    regions = []
                    for reg in region.split(','):
                        try:
                            regions.append(codes[reg])
                        except KeyError:
                            raise KeyError(
                                f'''{reg} направильно указан регион. допустимые значения {list(codes.keys())}''')
                    return regions
                else:
                    try:
                        return [codes[region]]
                    except KeyError:
                        raise KeyError(
                            f'''{region} направильно указан регион. допустимые значения {list(codes.keys())}''')

    def get_organization_code(self, org):
        '''находит айди региона. напр - Брянская область == 'r013200' '''
        with open(Path(__file__).parent / 'gov_bodies_n_their_codes.json', encoding='utf-8') as f:
                codes = json.load(f)
                if org is None:
                    orgs = []
                    for org_code in codes.values():
                        orgs.append(org_code)
                    return orgs
                elif isinstance(org, str) and len(org.split(',')) > 1:
                    orgs = []
                    for organization in org.split(','):
                        try:
                            orgs.append(codes[organization])
                        except KeyError:
                            raise KeyError(
                                f'''{org} направильно указан регион. допустимые значения {list(codes.keys())}''')
                    return organization
                else:
                    try:
                        return [codes[org]]
                    except KeyError:
                        raise KeyError(
                            f'''{org} направильно указан регион. допустимые значения {list(codes.keys())}''')




t = StartLinkCreator()
print(t.get_start_link())