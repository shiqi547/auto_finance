from web3 import Web3
from concurrent.futures import ThreadPoolExecutor
from django.http import HttpResponse
from django.shortcuts import render
import requests,re
from oauth2client.service_account import ServiceAccountCredentials
import gspread

scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive' 
    ]
#/root/myproject/caiwu.json
    # 从JSON密钥文件中加载认证信息
credentials = ServiceAccountCredentials.from_json_keyfile_name("替换掉", scopes)

# 使用先前下载的JSON密钥对gspread进行身份验证
file = gspread.authorize(credentials)

# 打开指定的Google Sheets表格
sheet = file.open("Google Sheets表格文件名")
worksheet1 = sheet.get_worksheet(0)
worksheet= sheet.get_worksheet(1)
# 获取部分
all_cells1 = worksheet1.get_all_values()
# 获取所有单元格的数据
all_cells = worksheet.get_all_values()
    # 将获取的数据转换为一个矩阵（二维列表）
matrix = [list(row) for row in all_cells1]
address1 = matrix[1][1]

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/d9b266f9315c4080baa53b12344a80a6'))
checksum_address1 = w3.to_checksum_address(address1)
balance_wei1 = w3.eth.get_balance(checksum_address1)
balance_eth1 = float(w3.from_wei(balance_wei1, 'ether'))

def get_token_decimals(w3, token_contract_address):
    decimals_method_id = w3.keccak(text="decimals()")[0:4].hex()
    result = w3.eth.call({'to': token_contract_address, 'data': decimals_method_id})
    return w3.to_int(hexstr=result.hex())

def get_token_balance(w3, token_contract_address, address):
    balance_of_method_id = w3.keccak(text="balanceOf(address)")[0:4].hex()
    checksum_address = w3.to_checksum_address(address)
    data = balance_of_method_id + '0' * 24 + checksum_address[2:]
    result = w3.eth.call({'to': token_contract_address, 'data': data})
    if result == bytes(32): # 检查是否全为零
        return 0
    return w3.to_int(hexstr=result.hex())

tokens = {
    'USDC': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'DAI': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
    'CFX':'0xA1f82E14bc09A1b42710dF1A8a999B62f294e592',
    'USDT': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    'MASK':'0x69af81e73A73B40adF4f3d4223Cd9b1ECE623074',
}

def everpay(id,hang):
    user_url = 'https://api.everpay.io/balances/{}'.format(id)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    response_list = requests.get(url=user_url, headers=headers).json()['balances']
    type_dict = {}  # 存放数据列表

    for response in response_list:
        name = response['tag']
        name = re.findall(r'-.*?-', name)[0].replace('-', '')
        number = response['amount']
        dic = response['decimals']
        b = len(number)
        d = b - dic
        index = 0
        data = []
        if d < 0:
            data.append('0.')
            xiangfan = 0 - d
            for i in range(xiangfan):
                data.append('0')

        for i in number:
            if index == d and d != 0:
                data.append('.')
            if d == 0:
                data.append('0.')
                d = -1
            index += 1
            data.append(i)
        data = ''.join(data)
        dict_data = {name: data}
        type_dict.update(dict_data)
    list2=[]
    usdc = type_dict["usdc"]
    if float(usdc) == 0:
        usdc = ''
    else: usdc = float(usdc)
    list2.append(usdc)
    ar = type_dict["ar"]
    if float(ar) == 0:
        ar = ''
    else: ar = float(ar)
    list2.append(ar)
    eth = type_dict["eth"]
    if float(eth) == 0:
        eth = ''
    else: eth = float(eth)
    list2.append(eth)
    usdt = type_dict["usdt"]
    if float(usdt) == 0:
        usdt = ''
    else: usdt = float(usdt)
    list2.append(usdt)
    cfx = type_dict["cfx"]
    if float(cfx) == 0:
        cfx = ''
    else: cfx = float(cfx)
    list2.append(cfx)
    glmr = type_dict["glmr"]
    if float(glmr) == 0:
        glmr = ''
    else: glmr = float(glmr)
    list2.append(glmr)
    acnh = type_dict["acnh"]
    if float(acnh) == 0:
        acnh = ''
    else: acnh = float(acnh)
    list2.append(acnh)
    ardrive = type_dict["ardrive"]
    if float(ardrive) == 0:
        ardrive = ''
    else: ardrive = float(ardrive)
    list2.append(ardrive)
    mask = type_dict["mask"]
    if float(mask) == 0:
        mask = ''
    else: mask = float(mask)
    list2.append(mask)
    bnb = type_dict["bnb"]
    if float(bnb) == 0:
        bnb = ''
    else: bnb = float(bnb)
    list2.append(bnb)
    cell_range = f'H{hang+1}:Q{hang+1}'
    worksheet.update(cell_range,[list2])


def viewblock(url,hang):
    headers = {}
    cookies = {}
    url = 'https://viewblock.io/arweave/address/{}'.format(url)
    #url = "https://viewblock.io/arweave/address/qmg-WUYiCHqhnx_kv4zx2zedssosU1is9Td2UWGfI5g"
    response = requests.get(url, headers=headers, cookies=cookies)
    balancear = re.findall('Balance</b><div class="sc-bczRLJ iIGKPS"><span>(.*?) ', response.text)[0]
    worksheet.update_cell(hang+1,9,balancear)


def etherscan(id,hang):
    checksum_address = w3.to_checksum_address(id)
    balance_wei = w3.eth.get_balance(checksum_address)
    balance_eth = float(w3.from_wei(balance_wei, 'ether'))
    balances=set()
    balances = {'ETH': balance_eth}
    def get_balance(token_name, contract_address):
        decimals = get_token_decimals(w3, contract_address)
        balance_wei = get_token_balance(w3, contract_address, id)
        balance = balance_wei / (10 ** decimals)
        balances[token_name] = balance  
    # 使用线程池并行处理
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_balance, token_name, contract_address) for token_name, contract_address in tokens.items()]


    # 确保所有的操作都完成
    for future in futures:
        future.result()
    
    if float(balances['ETH']) == 0.0:
        balances['ETH'] = ''
    if float(balances['USDT']) == 0.0:
        balances['USDT'] = ''
    if float(balances['USDC']) == 0.0:
        balances['USDC'] = ''
    if float(balances['CFX']) == 0.0:
        balances['CFX'] = ''
    if float(balances['MASK']) == 0.0:
        balances['MASK'] = ''
    worksheet.update_cell(hang+1, 10, balances['ETH'])
    worksheet.update_cell(hang+1, 11, balances['USDT'])
    worksheet.update_cell(hang+1, 12, balances['CFX'])
    worksheet.update_cell(hang+1, 8, balances['USDC'])
    worksheet.update_cell(hang+1, 16, balances['MASK'])
    
def backvalue(type_dict):
    c = []
    usdc = type_dict['usdc']
    if usdc == '0':
        usdc = ''
    c.append(usdc)
    ar = type_dict['ar']
    if ar == '0':
        ar = ''
    c.append(ar)
    eth = type_dict['eth']
    if eth == '0':
        eth = ''
    c.append(eth)
    usdt = type_dict['usdt']
    if usdt == '0':
        usdt = ''
    c.append(usdt)
    cfx = type_dict['cfx']
    if cfx == '0':
        cfx = ''
    c.append(cfx)
    glmr = type_dict['glmr']
    if glmr == '0':
        glmr = ''
    c.append(glmr)
    acnh = type_dict['acnh']
    if acnh == '0':
        acnh = ''
    c.append(acnh)
    ardrive = type_dict['ardrive']
    if ardrive == '0':
        ardrive = ''
    c.append(ardrive)
    mask = type_dict['mask']
    if mask == '0':
        mask = ''
    c.append(mask)
    bnb = type_dict['bnb']
    if bnb == '0':
        bnb = ''
    c.append(bnb)
    return c

def runm():
    # everpay
    user_url = 'https://api.everpay.io/balances/{}'.format(address1)
    headers = {}
    response_list = requests.get(url=user_url, headers=headers).json()['balances']
    type_dict = {}  # 存放数据列表
    for response in response_list:
        name = response['tag']
        name = re.findall(r'-.*?-', name)[0].replace('-', '')
        number = response['amount']
        dic = response['decimals']
        b = len(number)
        d = b - dic
        index = 0
        data = []
        if d < 0:
            data.append('0.')
            xiangfan = 0 - d
            for i in range(xiangfan):
                data.append('0')

        for i in number:
            if index == d:
                data.append('.')
            index += 1
            data.append(i)
        data = ''.join(data)
        dict_data = {name: data}
        type_dict.update(dict_data)
    dataeverpay = type_dict
    
    # everpay
    everpay = backvalue(dataeverpay)
    # 选择"data"工作表
    static_assets_worksheet = sheet.get_worksheet(0)
    value1=[float(value) for value in everpay]
    value1= [value if float(value) != 0 else '' for value in value1]
    value = [value1]
    # 将"data"工作表的数据复制
    static_assets_worksheet.update('E3:N3', value)

    # viewblock
    headers = {}
    cookies = {}
    url = 'https://viewblock.io/arweave/address//{}'.format(address1)
    response = requests.get(url, headers=headers, cookies=cookies)
    balance = re.findall('Balance</b><div class="sc-bczRLJ iIGKPS"><span>(.*?) ', response.text)[0]
    if balance == "0":
        balance = ''
    worksheet1.update_cell(5, 6, balance)

    # Etherscan
    # api_key = "Your_Etherscan_API_Key"
    balances = {'ETH': balance_eth1}

    # 使用线程池并行处理
    def get_balance(token_name, contract_address):
        decimals = get_token_decimals(w3, contract_address)
        balance_wei = get_token_balance(w3, contract_address, address1)
        balance = balance_wei / (10 ** decimals)
        balances[token_name] = balance
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_balance, token_name, contract_address) for token_name, contract_address in tokens.items()]
    
    # 确保所有的操作都完成
    for future in futures:
        future.result()
    if float(balances['ETH']) == 0.0:
        balances['ETH'] = ''
    if float(balances['USDT']) == 0.0:
        balances['USDT'] = ''
    if float(balances['USDC']) == 0.0:
        balances['USDC'] = ''
    if float(balances['CFX']) == 0.0:
        balances['CFX'] = ''
    if float(balances['MASK']) == 0.0:
        balances['MASK'] = ''
    
    worksheet1.update_cell(7, 7, balances['ETH'])
    worksheet1.update_cell(7, 8, balances['USDT'])
    worksheet1.update_cell(7, 9, balances['CFX'])
    worksheet1.update_cell(7, 5, balances['USDC'])
    worksheet1.update_cell(7, 13, balances['MASK'])
    
    everpay = 'https://scan.everpay.io/account/{}'.format(address1)
    Etherscan='https://etherscan.io/address/{}'.format(address1)
    Viewblock='https://viewblock.io/arweave/address/{}'.format(address1)
    worksheet1.update_cell(4, 2, everpay)
    worksheet1.update_cell(6, 2, Viewblock)
    worksheet1.update_cell(8, 2, Etherscan)

def run_code(request):
    if address1 !=' ':
        runm()
    for i in range(61):   #如有增加资产，可更改数字
        if len(all_cells[i][0])>10:
            nine=all_cells[i][0][8]
            parts = all_cells[i][0].split("/")
            address = parts[-1]
            if nine == "s":
                everpay(address,i)
            if nine == 'e':
                etherscan(address,i)
            if nine == 'v':
                viewblock(address,i)
    return HttpResponse("已加载，请返回excel,祝您生活愉快")