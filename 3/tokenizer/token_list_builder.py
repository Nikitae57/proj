from enum import Enum
import re


class TokensTypes:
    typeNameToRegex = {
        'SELECT': r'SELECT',
        'DISTINCT': r'DISTINCT',
        'ALL': r'ALL',
        'COMMA': r',',
        'FROM': r'FROM',
        'WHERE': r'WHERE',
        'ORDER': r'ORDER',
        'GROUP': r'GROUP',
        'BY': r'BY',
        'ASC': r'ASC',
        'DESC': r'DESC',
        'HAVING': r'HAVING',
        'LIMIT': r'LIMIT',
        'AS': r'AS',
        'OPEN_BRACKET': r'\(',
        'CLOSE_BRACKET': r'\)',
        'WILDCARD': r'\*',
        'EQUAL': r'=',
        'NOT_EQUAL': r'!=',
        'NOT': r'NOT',
        'LIKE': r'LIKE',
        'OR': r'OR',
        'AND': r'AND',
        'IS': r'IS',
        'NULL': r'NULL',
        'MORE': r'>',
        'MORE_OR_EQUAL': r'>=',
        'LESS': r'<',
        'LESS_OR_EQUAL': r'<=',
        'PLUS': r'\+',
        'MINUS': r'-',
        'MULTIPLY': r'\*',
        'DIVIDE': r'\/',
        'DIGIT': r'^-?[0-9]+(\.[0-9]+)?$',
        'NAME': r'(`\S+`|[A-Za-z_][A-Za-z_0-9]*(\.[A-Za-z_0-9]+)?)'
    }

    SELECT = 'SELECT'
    DISTINCT = 'DISTINCT'
    ALL = 'ALL'
    COMMA = 'COMMA'
    FROM = 'FROM'
    WHERE = 'WHERE'
    ORDER = 'ORDER'
    GROUP = 'GROUP'
    BY = 'BY'
    HAVING = 'HAVING'
    ASC = 'ASC'
    DESC = 'DESC'
    LIMIT = 'LIMIT'
    AS = 'AS'
    OPEN_BRACKET = 'OPEN_BRACKET'
    CLOSE_BRACKET = 'CLOSE_BRACKET'
    WILDCARD = 'WILDCARD'
    DIGIT = 'DIGIT'
    NAME = 'NAME'
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    NOT = 'NOT'
    LIKE = 'LIKE'
    OR = 'OR'
    AND = 'AND'
    IS = 'IS'
    NULL = 'NULL'
    MORE = 'MORE'
    MORE_OR_EQUAL = 'MORE_OR_EQUAL'
    LESS = 'LESS'
    LESS_OR_EQUAL = 'LESS_OR_EQUAL'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'


class TokenListBuilder:
    @staticmethod
    def buildTokenList(wordsList):
        tokenList = []
        typeNameToRegex = TokensTypes.typeNameToRegex
        for i, word in enumerate(wordsList):
            foundTokenType = None
            for tokenType in typeNameToRegex:
                isMatching = re.fullmatch(
                    TokensTypes.typeNameToRegex[tokenType],
                    word
                )
                if isMatching:
                    foundTokenType = tokenType
                    break

            if foundTokenType is None:
                exceptionStr = 'Invalid SQL token: "' + word + '" at {} position'.format(i)
                raise Exception(exceptionStr)
            else:
                tokenList.append((foundTokenType, word))

        return tokenList

