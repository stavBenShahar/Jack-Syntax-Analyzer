import re
import itertools


class JackTokenizer:
    LEXICAL_ELEMENTS_MATCHES = ['KEYWORD', 'SYMBOL', 'INT_CONST',
                                'STRING_CONST', 'IDENTIFIER']

    KEYWORD = ('(class|constructor|function|method|field|static|var|int|'
               'char|boolean|void|true|false|null|this|let|do|if|else|while|return)')
    SYMBOL = '([{}()[\].,;+\-*/&|<>=~^#])'
    INT_CONST = '(\d+)'
    STRING_CONST = '\"([^\n]*)\"'
    IDENTIFIER = '([A-Za-z_]\w*)'
    LEXICAL_ELEMENTS = '{}|{}|{}|{}|{}'.format(KEYWORD, SYMBOL, INT_CONST,
                                               STRING_CONST, IDENTIFIER)

    LEXICAL_ELEMENTS_REGEX = re.compile(LEXICAL_ELEMENTS)

    INLINE_COMMENT_REGEX = re.compile('//.*\n')
    MULTILINE_COMMENT_REGEX = re.compile('/\*.*?\*/', flags=re.S)

    def __init__(self, inputFile):
        self.input = inputFile.read()
        self.tokens = self._tokenize()
        self.nextToken = ''
        self.advance()
        inputFile.close()

    def _removeComments(self):
        withoutMultiline = re.sub(self.MULTILINE_COMMENT_REGEX, ' ',
                                  self.input)
        withoutInline = re.sub(self.INLINE_COMMENT_REGEX, '\n',
                               withoutMultiline)
        return withoutInline

    def keyWord(self):
        return self.curToken[0].upper()

    def symbol(self):
        return self.curToken[0]

    def identifier(self):
        return self.curToken[0]

    def intVal(self):
        return self.curToken[0]

    def stringVal(self):
        return self.curToken[0]

    def tokenType(self):
        return self.curToken[1]

    def _geElementMatches(self):
        return lambda elementMatches:\
            self.LEXICAL_ELEMENTS_MATCHES[
                next(i for i, element in enumerate(elementMatches) if element)]

    def _getMatchTypes(self, matches):
        return map(self._geElementMatches(), matches)

    def _tokenize(self):
        inputWithoutComments = self._removeComments()
        matches = self.LEXICAL_ELEMENTS_REGEX.findall(inputWithoutComments)
        matchTypes = self._getMatchTypes(matches)
        flatMatches = list(itertools.chain(*matches))
        tokens = [match for match in flatMatches if match]
        return list(zip(tokens, matchTypes))

    def hasMoreTokens(self):
        return self.nextToken

    def advance(self):
        self.curToken = self.nextToken

        if len(list(self.tokens)):
            self.nextToken = self.tokens.pop(0)
        else:
            self.nextToken = False