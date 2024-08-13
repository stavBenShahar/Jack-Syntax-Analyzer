import os
import sys

from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer

USAGE_ERR_MSG = "USAGE: please use: JackAnalyzer <input path>"


def createTokenFile(jackFileName: str) -> str:
    xmlConversions = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
    tokenFileName = jackFileName.replace('.jack', 'T.xml')
    tokenFile = open(tokenFileName, 'w')  # Closes in line 50
    jackFile = open(jackFileName, 'r')  # Closes in line 25
    tokenizer = JackTokenizer(jackFile)
    tokenFile.write('<tokens>\n')

    while tokenizer.hasMoreTokens():
        tokenizer.advance()
        if tokenizer.tokenType() == 'KEYWORD':
            tokenFile.write('<keyword> {} </keyword>\n'.format(
                tokenizer.keyWord().lower()))
        elif tokenizer.tokenType() == 'SYMBOL':
            symbol = tokenizer.symbol()
            if symbol in xmlConversions:
                symbol = xmlConversions[symbol]
            tokenFile.write('<symbol> {} </symbol>\n'.format(symbol))
        elif tokenizer.tokenType() == 'IDENTIFIER':
            tokenFile.write('<identifier> {} </identifier>\n'.format(
                tokenizer.identifier()))
        elif tokenizer.tokenType() == 'INT_CONST':
            tokenFile.write('<integerConstant> {} </integerConstant>\n'.format(
                tokenizer.intVal()))
        elif tokenizer.tokenType() == 'STRING_CONST':
            tokenFile.write('<stringConstant> {} </stringConstant>\n'.format(
                tokenizer.stringVal()))

    tokenFile.write('</tokens>\n')
    tokenFile.close()
    return tokenFileName


def analyzeFile(inputFileName: str, outputFileName: str) -> None:
    tokenFileName = createTokenFile(inputFileName)
    tokenFile = open(tokenFileName, 'r')
    outputFile = open(outputFileName, 'w')
    engine = CompilationEngine(tokenFile, outputFile)
    engine.compileClass()
    outputFile.close()
    tokenFile.close()


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        sys.exit(USAGE_ERR_MSG)
    argumentPath = os.path.abspath(sys.argv[1])
    if os.path.isdir(argumentPath):
        filesToAssemble = [
            os.path.join(argumentPath, filename)
            for filename in os.listdir(argumentPath)]
    else:
        filesToAssemble = [argumentPath]
    for inputPath in filesToAssemble:
        filename, extension = os.path.splitext(inputPath)
        if extension.lower() != ".jack":
            continue
        outputPath = filename + ".xml"
        analyzeFile(inputPath, outputPath)
