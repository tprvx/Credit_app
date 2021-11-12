# Blockchain on python

Приложение кредитования на блокчейне, имеет следующий функционал:
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