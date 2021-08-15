import hashlib
import json
import os
import time

blockchain_dir = os.curdir + '/blockchain_temp/'
transactions = []

def setMercleRoot(trs):
	merkle_hashes = []	#хеши транзакций
	mercle_two = []		#хеши хешей
	mercle_root = None  #корень дерева Меркла
	n = 0;				#счетчик для цикла

	for t in trs: #хеши транзакций
		n = n + 1
		bytes = json.dumps(t).encode()
		merkle_hashes.append(hashlib.sha256(bytes).hexdigest())
		if n%2 == 0:	#первый уровень хешей хешей
			mercle_two.append(hashlib.sha256((f'{merkle_hashes[n-2]}{merkle_hashes[n-1]}').encode()).hexdigest())

	mercle_root = hashlib.sha256((f'{mercle_two[0]}{mercle_two[1]}').encode()).hexdigest()
	#print("Хеши транзакций: {0}\nХеши хешей: {1}\nКорень дерева Меркла: {2}".format(merkle_hashes,mercle_two,mercle_root))

	return mercle_root

def getTestTrs():
	#Cформируем список транзакций
	trs = []
	tr = {
		'name': 'Victor',
		'to_whom': 'Rulic',
		'amount': 11
	}
	trs.append(tr)
	tr = {
		'name': 'Pavel',
		'to_whom': 'Abdulla',
		'amount': 54
	}
	trs.append(tr)
	tr = {
		'name': 'Nickolay',
		'to_whom': 'Petr',
		'amount': 100
	}
	trs.append(tr)
	tr = {
		'name': 'Malic',
		'to_whom': 'Ara',
		'amount': 5
	}
	trs.append(tr)

	return trs


def inputTransaction(name, to_whom, amount):
	#Cформируем список транзакций

	tr = {
		'name': name,
		'to_whom': to_whom,
		'amount': amount
	}
	transactions.append(tr)
	if len(transactions) == 4:
		write_block(transactions)
		transactions.clear()


#Расчет дерева Меркла
def setGenesysBlock():

	#получаем транзакции
	trs = getTestTrs()

	#получаем корень дерева Меркла
	mercle_root = setMercleRoot(trs)
	
	#Заголовок блока
	header = {
		'number': 1,						#номер блока
		'timestamp': time.ctime(),			#время создания
		'mercle_root': mercle_root,			#корень дерева меркла для списка транзакций
		'hash_of_block': '0x0',				#хеш блока
		'prev_hash': '0x0',					#хеш предыдущего блока
		'nonce': 0							#доказательство работы
	}

	#Формируеем блок
	block = {
		'header': header,	#Заголовок блока	
		'trs': trs			#Список транзакций
	}

	#Поиск доказательства работы
	proof = 0
	while validHash(header) is False:
		proof += 1
		header['nonce'] = proof
		#print(header)

	#Формируем имя файла
	header['hash_of_block'] = getHash(header)
	name_of_file = blockchain_dir + f"{header['number']}" + '.json'  ###+ '_'+ f"{header['number']}" 
	print(name_of_file)

	#Создаем файл блока
	with open(name_of_file, 'w') as file:
		json.dump(block, file, indent=4, ensure_ascii=False)
 
def write_block(trs): #name, to_whom, amount
	
	#получаем хеш пред блока
	numbers = get_files_numbers()
	prev_number = numbers[-1]
	number = str(prev_number + 1)

	
	f = open(blockchain_dir + str(prev_number) + '.json', 'r')
	prev_hash = json.load(f)['hash_of_block']
	#print(prev_hash)
	#prev_hash = getHash(prev_file['header'])

	#получаем транзакции
	#trs = getTestTrs()

	#получаем корень дерева Меркла
	mercle_root = setMercleRoot(trs)

	#Заголовок блока
	header = {
		'version': 1,
		'timestamp': time.ctime(),			#время создания
		'mercle_root': mercle_root,			#корень дерева меркла для списка транзакций
		'prev_hash': prev_hash,					#хеш предыдущего блока
		'nonce': 0							#доказательство работы
	}

	#Формируеем блок
	block = {
		'hash_of_block': '',	#хеш блока
		'header': header,		#Заголовок блока	
		'transactions': trs				#Список транзакций
	}

	#Поиск доказательства работы
	proof = 0
	while validHash(header) is False:
		proof += 1
		header['nonce'] = proof
		#print(header)

	#Формируем имя файла
	block['hash_of_block'] = getHash(header)
	name_of_file = blockchain_dir + number + '.json' 
	#print(name_of_file)

	#Создаем файл блока
	with open(name_of_file, 'w') as file:
		json.dump(block, file, indent=4, ensure_ascii=False)

	
#Получение сортированного списка блоков
def get_files_numbers():
	files = os.listdir(blockchain_dir)
	return sorted([int(i.split('.')[0]) for i in files])

#Проверка доказательства работы, валидация блока
def getHash(value):
	return hashlib.sha256(f'{value}'.encode()).hexdigest()

def validHash(value):
	value['timestamp'] = time.ctime()
	hash = getHash(value)
	return hash[:4] == '0000'

#Проверка целостности блокчейна
def check_blockchain():
	#результаты проверки блокчейна
	results = []
	#получаем имена файлов в блокчейне
	numbers = get_files_numbers()

	#проверяем genesys блок
	with open(blockchain_dir + str(0) + '.json', 'r') as file:
		f = json.load(file)

		#если расчетный хеш транзакций совпадает с записанным в заголовке, то транзакции верны
		if setMercleRoot(f['transactions']) == f['header']['mercle_root']:
			root = 'Ok'
		else:
			root = 'Corrupted transactions'
		results.append({'Block': 0, 'trs_check': root})

		#если расчетный хеш совпадает с хешем блока
		if (getHash(f['header'])) == f['hash_of_block']:
			res = 'Ok'
		else:
			res = 'Corrupted Genesys block!'
		results[0]['hash_check'] = res

	#сверяем хеши предыдущего блока с записанным в заголовке, последный слок не проверяем
	for n in numbers[1:]:
		with open(blockchain_dir + str(n) + '.json', 'r') as file:
			f = json.load(file)

			#если расчетный хеш транзакций совпадает с записанным в заголовке, то транзакции верны
			if setMercleRoot(f['transactions']) == f['header']['mercle_root']:
				root = 'Ok'
			else:
				root = 'Corrupted transactions'
			results.append({'Block': n, 'trs_check': root})

			with open(blockchain_dir + str(n-1) + '.json', 'r') as prev_file:
				pf = json.load(prev_file)

				#если расчетный хеш совпадает с хешем предыдущего блока
				if (getHash(pf['header'])) == f['header']['prev_hash']:
					res = 'Ok'
				else:
					res = 'Corrupted!'
		results[n-1]['hash_check'] = res

		#сравниваем всё
		if results[n-1]['hash_check'] == results[n-1]['trs_check']:
			results[n-1]['summary_check'] = 'Ok'
		else:
			results[n-1]['summary_check'] = 'Corrupted!'

	#Для последнего блока
	with open(blockchain_dir + str(numbers[-1]) + '.json', 'r') as file:
		f = json.load(file)
		#если расчетный хеш совпадает с хешем предыдущего блока
		if (getHash(f['header'])) == f['hash_of_block']:
			res = 'Ok'
		else:
			res = 'Corrupted!'
	results[-1]['hash_check'] = res

	if results[-1]['hash_check'] == results[-1]['trs_check']:
		results[-1]['summary_check'] = 'Ok'
	else:
		results[-1]['summary_check'] = 'Corrupted!'



	print(results)
	return results

if __name__ == '__main__':
  	check_blockchain()
	#get_files()
# 	#write_block()
# 	#setGenesysBlock()
