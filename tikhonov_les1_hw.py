import json
import requests
import time


# Задачу разобьем на 2 этапа:
# 1) парсинг каталога товаров с целью взять код и название категории
# 2) парсинг списка товаров конкретной категории


def parse_funk(url, req_headers={}, req_params={}):
    while True:
        try:
            response = requests.get(url, params=req_params, headers=req_headers)
            if response.status_code != 200:
                raise Exception
            return response.json()
        except Exception:
            time.sleep(0.1)


if __name__ == '__main__':
    # Получим каталог товаров в виде json
    my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    catalog_url = 'https://5ka.ru/api/v2/categories/'

    catalog_info = parse_funk(catalog_url, my_headers)
    # Пройдем по каталогу, возьмем код и название категории и отпарсим соответствующие товары
    for itm in catalog_info:
        cat_code = itm['parent_group_code']
        cat_name = itm['parent_group_name']
        products_list = []

        products_url = 'https://5ka.ru/api/v2/special_offers/'
        my_params = {
            'categories': cat_code
        }

        while products_url:
            products_info = parse_funk(products_url, my_headers, my_params)
            for product_itm in products_info['results']:
                products_list.append(product_itm)

            products_url = products_info['next']

        # Сохраним результаты для очередной категории, если там присутствуют товары
        if len(products_list):
            data = {
                'name': cat_name,
                'code': cat_code,
                'products': products_list
            }
            with open(f'parse_results/category_{cat_code}.json', 'w', encoding='UTF-8') as file:
                json.dump(data, file, ensure_ascii=False)
