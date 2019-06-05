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

sourcePath = "./DATA/"                   # 测试合约目录

maxInputGen = 2                          # 对每个函数生成的输入组数
maxMutaIter = 2                          # 变异次数


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


def all_file_name(file_dir):   
    l = []   
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            if os.path.splitext(file)[1] == '.sol':  # 后缀
                l.append(os.path.splitext(file)[0])  # 文件名
    return l


import execjs

def get_jsRequest(param):
    with open("./TypeRandom.js", "r") as f:   
        data_func = f.read()          # 读取js文件
    tk = execjs.compile(data_func)    # 编译执行js代码
    tk = tk.call('getTypeRandom', param)
    return tk


def main():
    fileList = all_file_name(sourcePath)
    # 遍历合约
    for co in range(len(fileList)):
        contractName = fileList[co]
        print("* contractName:", contractName, " *")
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
                print("** funcName:", funcName, " **")

                # inputdatalist = [['6', '2']]
                inputdatalist = []
                # 随即生成xx组input
                for idx in range(maxInputGen):
                    randomData = get_jsRequest(dataTypeList)
                    inputdatalist.append(randomData)

                # 遍历输入
                for cur in range(len(inputdatalist)):
                    inputdata = '' 
                    for i in range(len(inputdatalist[cur])):
                        if i != 0 :
                            inputdata += ', '
                        inputdata += inputdatalist[cur][i]
                    print("** inputParam:", inputdata, " **")
                    ori = ['R_ContractName', 'R_FunctionName', '(R_Signature)', 'R_Inter']
                    rep = [contractName, funcName, inputdata, '#']
                    # print(rep)
                    replaceTestFile(contractName, ori, rep, 1)

                    # 运行
                    os.system("cp " + sourcePath + contractName + ".sol ./contracts/")
                    os.system("npx solidity-coverage")

                    # 变异
                    for iter in range(maxMutaIter):
                        print("*** iter#", iter, " ***")
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
                        # print(deadCodeLine)

                        mutate.exec('./contracts/'+contractName+'.sol', deadCodeLine, 1)
                        # 保存种子
                        os.system('cp ./contracts/'+contractName+'.sol ./output/seed/'+
                                contractName+'_'+funcName+'_'+str(iter)+'.sol')

                        # 变异后运行
                        rep[3] = '#' + str(iter)
                        replaceTestFile(contractName, ori, rep, 2)
                        os.system("npx solidity-coverage 2")  # do not generate report
                    
                    # clean ./scripts/xxx.expect.out
                    f = open('./scripts/'+contractName+'.expect.out', "r+")
                    f.truncate()

                # break  # 只运行一个函数


if __name__ == '__main__':
    initEnvironment()
    main()
    # cleanUp()