# Credit app

Приложение для кредитования на блокчейне, имеет следующий функционал:
* Ввод данных транзакции (фреймворк Flask)
* Организация хранения блоков в json файлах
* Расчет дерева Меркла списка транзакций в блоке
* Расчет хеша заголовка блока и заголовка предыдущего блока
* Реализация proof-of-work концепции (сложность, расчет nonce)
* Реализован функционал валидации блока и всей цепи:
    - Пересчет корня дерева меркла каждого блока и сравнение с
    корнем в заголовке блока
    - Пересчет хеша заголовка каждого предыдущего  блока и сравнение
    со значением в заголовке блока

## Usage

```cmd
git clone https://github.com/tprvx/first_blockchain_py.git
cd Credit_app 
python main.py
Running on http://127.0.0.1:5000 
```

Блок имеет структуру:
```json
{
    "hash_of_block": "00007bfc8ff14ba98f2a278d06b7670aeb24d5ea6816d60d626fcd79eba8b194",
    "header": {
        "number": "2",
        "version": "1",
        "timestamp": "Fri Nov 12 22:40:43 2021",
        "mercle_root": "408820a77c16d51da50154145997c7f91cc56832fefd8ae606e2111670665258",
        "prev_hash": "000037328739df61d8c88d78fedf041c9c0dc2106ff7746912f6300ec38e5d70",
        "nonce": "3516"
    },
    "transactions": [
        {
            "name": "Alexander",
            "to_whom": "Andrey",
            "amount": "100"
        },
        {
            "name": "Petr",
            "to_whom": "Nikolay",
            "amount": "40"
        },
        {
            "name": "Nikolay",
            "to_whom": "Ali",
            "amount": "5000"
        },
        {
            "name": "Anna",
            "to_whom": "Pavel",
            "amount": "432"
        }
    ]
}
```