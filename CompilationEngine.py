import re


class CompilationEngine:

    def __init__(self, tokenFile, outputFile):

        self.curToken = None
        self.tokenFile = tokenFile
        self.outputFile = outputFile
        self.indentCount = 0
        self.written = True
        self.tokenFile.readline()

    def compileClass(self) -> None:
        self.writeOpenTag('class')
        # 'class' className {
        self.writeCurTokenNTimes(3)

        while self.isClassVarDec():
            self.compileClassVarDec()
            self.saveTokenIfWritten()

        while self.isSubroutineDec():
            self.compileSubroutine()
            self.saveTokenIfWritten()

        self.writeCurToken()
        self.writeCloseTag('class')

    def compileClassVarDec(self) -> None:
        self.writeOpenTag('classVarDec')
        # ('static' | 'field') type varName
        self.writeCurTokenNTimes(3)
        self.compileMultiple(',', 'identifier')
        self.writeCurToken()
        self.writeCloseTag('classVarDec')

    def compileSubroutine(self) -> None:
        self.writeOpenTag('subroutineDec')
        # (constructor/function/method) (void/type) routineName (
        self.writeCurTokenNTimes(4)
        self.compileParameterList()
        self.writeCurToken()
        self.writeOpenTag('subroutineBody')
        self.writeCurToken()
        self.saveTokenIfWritten()
        while 'var' in self.curToken:
            self.compileVarDec()
            self.saveTokenIfWritten()
        self.compileStatements()
        self.writeCurToken()
        self.writeCloseTag('subroutineBody')
        self.writeCloseTag('subroutineDec')

    def compileParameterList(self) -> None:
        self.writeOpenTag('parameterList')
        self.saveTokenIfWritten()
        if ' ) ' not in self.curToken:
            # type varName
            self.writeCurTokenNTimes(2)
            self.saveTokenIfWritten()
        while ' ) ' not in self.curToken:
            # ,type varName
            self.writeCurTokenNTimes(3)
            self.saveTokenIfWritten()
        self.writeCloseTag('parameterList')

    def compileVarDec(self) -> None:
        self.writeOpenTag('varDec')
        # var type varName
        self.writeCurTokenNTimes(3)
        self.compileMultiple(',', 'identifier')
        self.writeCurToken()
        self.writeCloseTag('varDec')

    def compileStatements(self) -> None:
        self.writeOpenTag('statements')

        while self.isStatement():
            if 'let' in self.curToken:
                self.compileLet()
            elif ' if ' in self.curToken:
                self.compileIf()
            elif 'while' in self.curToken:
                self.compileWhile()
            elif 'do' in self.curToken:
                self.compileDo()
            elif 'return' in self.curToken:
                self.compileReturn()
            self.saveTokenIfWritten()

        self.writeCloseTag('statements')

    def compileDo(self) -> None:
        self.writeOpenTag('doStatement')
        # do (subRoutineName|className|varName)
        self.writeCurTokenNTimes(2)
        self.saveTokenIfWritten()
        if '.' in self.curToken:
            # .subRoutineName
            self.writeCurTokenNTimes(2)
        self.writeCurToken()
        self.compileExpressionList()
        # );
        self.writeCurTokenNTimes(2)
        self.writeCloseTag('doStatement')

    def compileLet(self) -> None:
        self.writeOpenTag('letStatement')
        # let varName
        self.writeCurTokenNTimes(2)
        self.saveTokenIfWritten()

        if ' [ ' in self.curToken:
            self.writeCurToken()
            self.compileExpression()
            self.writeCurToken()
        self.writeCurToken()
        self.compileExpression()
        self.writeCurToken()
        self.writeCloseTag('letStatement')

    def compileWhile(self) -> None:
        self.writeOpenTag('whileStatement')
        # while (
        self.writeCurTokenNTimes(2)
        self.compileExpression()
        # ) {
        self.writeCurTokenNTimes(2)
        self.compileStatements()
        self.writeCurToken()
        self.writeCloseTag('whileStatement')

    def compileReturn(self) -> None:
        self.writeOpenTag('returnStatement')
        self.writeCurToken()
        self.saveTokenIfWritten()
        if ';' not in self.curToken:
            self.compileExpression()
        self.writeCurToken()
        self.writeCloseTag('returnStatement')

    def compileIf(self) -> None:
        self.writeOpenTag('ifStatement')
        # if (
        self.writeCurTokenNTimes(2)
        self.compileExpression()
        # ) {
        self.writeCurTokenNTimes(2)
        self.compileStatements()
        self.writeCurToken()
        self.saveTokenIfWritten()

        if 'else' in self.curToken:
            # else {
            self.writeCurTokenNTimes(2)
            self.compileStatements()
            self.writeCurToken()

        self.writeCloseTag('ifStatement')

    def compileExpression(self) -> None:
        self.writeOpenTag('expression')
        self.compileTerm()

        while self.isOp():
            self.writeCurToken()
            self.compileTerm()

        self.writeCloseTag('expression')

    def compileTerm(self) -> None:
        self.writeOpenTag('term')

        self.saveTokenIfWritten()

        if self.isUnaryOpTerm():
            self.writeCurToken()
            self.compileTerm()
        elif ' ( ' in self.curToken:
            self.writeCurToken()
            self.compileExpression()
            self.writeCurToken()
        else:
            self.writeCurToken()

            self.saveTokenIfWritten()

            if ' [ ' in self.curToken:
                self.writeCurToken()
                self.compileExpression()
                self.writeCurToken()
            elif ' . ' in self.curToken:
                # .subRoutineName (
                self.writeCurTokenNTimes(3)
                self.compileExpressionList()
                self.writeCurToken()
            elif ' ( ' in self.curToken:
                self.writeCurToken()
                self.compileExpressionList()
                self.writeCurToken()

        self.writeCloseTag('term')

    def compileExpressionList(self) -> None:
        self.writeOpenTag('expressionList')

        self.saveTokenIfWritten()

        if ' ) ' not in self.curToken:
            self.compileExpression()
            self.saveTokenIfWritten()

        while ' ) ' not in self.curToken:
            self.writeCurToken()
            self.compileExpression()
            self.saveTokenIfWritten()

        self.writeCloseTag('expressionList')

    def compileMultiple(self, firstIdentifier: str, secondIdentifier: str) -> None:
        self.saveTokenIfWritten()

        while firstIdentifier in self.curToken or secondIdentifier in self.curToken:
            self.writeCurToken()
            self.saveTokenIfWritten()

    def isClassVarDec(self) -> bool:
        self.saveTokenIfWritten()

        return 'static' in self.curToken or 'field' in self.curToken

    def isSubroutineDec(self) -> bool:
        self.saveTokenIfWritten()

        return 'constructor' in self.curToken or 'function' in self.curToken or \
               'method' in self.curToken

    def isStatement(self) -> bool:
        self.saveTokenIfWritten()

        return 'let' in self.curToken or 'if' in self.curToken or 'while' in self.curToken \
               or 'do' in self.curToken or 'return' in self.curToken

    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                      Operators                      #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def isOp(self) -> bool:
        self.saveTokenIfWritten()
        return not re.search(r'> (\+|-|\*|/|&amp;|\||&lt;|&gt;|=) <', self.curToken) is None

    def isUnaryOpTerm(self) -> bool:
        self.saveTokenIfWritten()
        return not re.search(r'> (-|~|#|\^) <', self.curToken) is None

    # Write methods:
    def writeOpenTag(self, tag: str) -> None:
        self.outputFile.write('{}<{}>\n'.format(self.curIndent(), tag))
        self.increaseIndent()

    def writeCloseTag(self, tag: str) -> None:
        self.decreaseIndent()
        self.outputFile.write('{}</{}>\n'.format(self.curIndent(), tag))

    def writeCurToken(self):
        if self.written:
            self.curToken = self.tokenFile.readline()
        else:
            self.written = True

        output_line = '{}{}'.format(self.curIndent(), self.curToken)
        self.outputFile.write(output_line)

    def writeCurTokenNTimes(self, num: int) -> None:
        for _ in range(num):
            self.writeCurToken()

    def saveTokenIfWritten(self):
        if self.written:
            self.curToken = self.tokenFile.readline()
            self.written = False

    # Indent methods:
    def increaseIndent(self) -> None:
        self.indentCount += 1

    def decreaseIndent(self) -> None:
        self.indentCount -= 1

    def curIndent(self) -> str:
        return '  ' * self.indentCount