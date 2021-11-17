import sys
import time
import pprint

from web3 import *
from solc import compile_source
import os

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def connectWeb3():
    # print(os.environ['HOME']+'/HW3/test-eth1/geth.ipc')
    return Web3(IPCProvider(os.environ['HOME']+'/HW3/test-eth1/geth.ipc', timeout=100000))


def deployEmptyContract(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface3 = compiled_sol.popitem()
    curBlock = w3.eth.getBlock('latest')
    tx_hash = w3.eth.contract(
            abi=contract_interface3['abi'],
            bytecode=contract_interface3['bin']).constructor().transact({'txType':"0x0", 'from':account, 'gas':1000000})
    return tx_hash

def deployContracts(source_path,w3, account):
    tx_hash3 = deployEmptyContract(source_path, w3, account)

    
    receipt3 = w3.eth.getTransactionReceipt(tx_hash3)

    while ((receipt3 is None)) :
        time.sleep(1)
        receipt3 = w3.eth.getTransactionReceipt(tx_hash3)

    w3.miner.stop()

    
    if receipt3 is not None:
        f=open("contractAddressList","w")
        print("empty:{0}".format(receipt3['contractAddress']), file=f)
        f.close() 


def deploy():
    source_path = os.environ['HOME']+'/HW3/Dapp.sol'


    w3 = connectWeb3()
    # print("1")
    w3.miner.start(1)
    # print("2")
    time.sleep(4)
    deployContracts(source_path,w3, w3.eth.accounts[0])