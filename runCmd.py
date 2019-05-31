# -*- coding: UTF-8 -*-
import subprocess
import argparse
import random
import time
import os,shutil
import ctypes,sys
import heapq
import json
import re
import mutate

sourcePath = "/home/rm/Desktop/"


def initEnvironment():
    # create needed folders
    os.system("mkdir scripts/")
    os.system("mkdir output/")
    os.system("mkdir output/seed/")

    # create file
    if os.path.exists('./output/bugReport'):
        os.remove('./output/bugReport')
    os.system("touch ./output/bugReport")  # bug report file

def cleanUp():
    os.system("rm -rf ./scripts")
    os.system("rm -rf ./output")
    os.system("rm -rf ./contracts/*")
    os.system("rm -rf ./test/*")

    os.system("rm -rf ./coverage")
    if os.path.exists("./coverage.json"):
        os.remove("./coverage.json")
    pass


def replaceTestFile(contractname, ori, rep, choice=1):
    filename = contractname + ".Test.js"
    # 如果存在，删除
    if os.path.exists('./test/'+filename):
        os.remove("./test/"+filename)

    if choice == 1:
        subprocess.call("cp ./exampleJS/TestFirst.js ./test/" + filename, shell=True)
    else:
        subprocess.call("cp ./exampleJS/TestSecond.js ./test/" + filename, shell=True)

    # replace key words
    f = open('./test/'+filename,'r')  # read
    alllines = f.readlines()
    f.close()
    f = open('./test/'+filename,'w+')  # write
    for line in alllines:
        a = line
        for i in range(len(ori)):
            a = re.sub(ori[i], rep[i], a)
        f.writelines(a)
    f.close()


def main():
    contractName = "NewContract"
    os.system("cp " + sourcePath + contractName + ".sol ./contracts/")

    # 生成函数签名
    dirPATH = "./scripts/"
    subprocess.call("solc ./contracts/" + contractName + ".sol --hashes -o " + dirPATH, shell=True)

    if os.path.exists('./scripts/'+contractName+'.signatures'):
        sigfile = open('./scripts/'+contractName+'.signatures', "r")
        line = sigfile.read().splitlines()
        # 遍历函数
        for signature in line:
            pos1 = signature.find('(')
            pos2 = signature.find(')')

            # sig = "0x" + signature[:8]
            funcName = signature[10:pos1]
            dataTypeList = signature[pos1+1:pos2].split(',')

            # 生成输入
            # inputdatalist = genInputData(...)

            # 遍历输入
            inputdatalist = [['6', '2']]
            for cur in range(len(inputdatalist)):
                inputdata = ''
                for i in range(len(inputdatalist[cur])):
                    if i != 0 :
                        inputdata += ', '
                    inputdata += inputdatalist[cur][i]
                ori = ['R_ContractName', 'R_FunctionName', '(R_Signature)', 'R_Inter']
                rep = [contractName, funcName, inputdata, '#']
                # print(rep)
                replaceTestFile(contractName, ori, rep, 1)

                # 运行
                os.system("cp " + sourcePath + contractName + ".sol ./contracts/")
                os.system("npx solidity-coverage")

                # 变异次数
                maxMutaIter = 1
                for iter in range(maxMutaIter):
                    # print(funcName, iter)
                    # 复制原始合约
                    os.system("cp " + sourcePath + contractName + ".sol ./contracts/")
                    
                    # line number of dead code
                    deadCodeLine = []
                    load_f = open("./coverage.json",'r')
                    json_dict = json.load(load_f)
                    for lineNo, val in json_dict['contracts/'+contractName+'.sol']['l'].items():
                        if val == 0:
                            deadCodeLine.append(lineNo)
                    load_f.close()
                    print(deadCodeLine)

                    mutate.exec('./contracts/'+contractName+'.sol', deadCodeLine, 1)
                    # 保存种子
                    os.system('cp ./contracts/'+contractName+'.sol ./output/seed/'+
                              contractName+'_'+funcName+'_'+str(iter)+'.sol')

                    # 变异后运行
                    rep[3] = '#' + str(iter)
                    replaceTestFile(contractName, ori, rep, 2)
                    os.system("npx solidity-coverage 2")  # do not generate report

            # break  # 只运行一个函数

    cleanUp()


if __name__ == '__main__':
    initEnvironment()
    main()
    # cleanUp()