import os
import csv


class PriceMachine:

    def __init__(self):
        self.data = []
        self.find_result = []
        self.result = ''
        self.name_count = 0

    def load_prices(self, file_path=''):
        if not file_path:
            file_path = os.path.dirname(os.path.abspath(__file__))

        for root, dirs, files in os.walk(file_path):
            for file in files:
                if 'price' in file.lower():
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        headers = next(reader)
                        product_col, price_col, weight_col = self._search_product_price_weight(headers)

                        if product_col is not None and price_col is not None and weight_col is not None:
                            for row in reader:
                                product = row[product_col]
                                price = row[price_col]
                                weight = row[weight_col]
                                self.data.append((product, price, weight, file))
                                self.name_count = self.name_count + 1

        return f'Найдено {self.name_count} продуктов.'

    def _search_product_price_weight(self, headers):
        product_col = None
        price_col = None
        weight_col = None

        for i, header in enumerate(headers):
            header = header.lower()
            if 'товар' in header or 'название' in header or 'наименование' in header or 'продукт' in header:
                product_col = i
            elif 'розница' in header or 'цена' in header:
                price_col = i
            elif 'вес' in header or 'масса' in header or 'фасовка' in header:
                weight_col = i

        return product_col, price_col, weight_col

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for i, (product, price, weight, file) in enumerate(self.find_result, start=1):
            result += f'''
                        <tr>
                            <td>{i}</td>
                            <td>{product}</td>
                            <td>{price}</td>
                            <td>{weight}</td>
                            <td>{file}</td>
                            <td>{round(float(price) / float(weight), 2)}</td>
                        </tr>
                    '''

        result += '''
                    </table>
                </body>
                </html>
                '''

        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)

        return 'Результат поиска экспортирован в HTML.'

    def find_text(self, text):
        text = text.lower()
        for product in self.data:
            if text in product[0].lower():
                self.find_result.append(product)
                print(product)


pm = PriceMachine()
print(pm.load_prices())

def search_interface():
    while True:
        text = input('Введите фрагмент названия продукта или "exit", чтобы выйти: ')
        pm.find_text(text)

        if text.lower() == 'exit':
            print('Программа завершила работу.')
            break

search_interface()
print(pm.export_to_html())
