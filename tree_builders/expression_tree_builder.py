from tokenize.token_list_builder import TokensTypes as t
import re

class ExpressionTreeBuilder:
    @staticmethod
    def buildExprTree(tokensList: list):
        andCondition = andCondition(tokensList)

    @staticmethod
    def andCondition(tokenList):
        # lastPosition - индекс токена с которого надо продолжать
        condition, lastPosition = condition(tokenList)

    @staticmethod
    def condition(tokenList):
        operand, lastPosition = summand(tokenList)

    @staticmethod
    def summand(tokenList):
        factor, lastPosition = factor(tokenList)

    @staticmethod
    def factor(tokenList):
        term, lastPosition = term(tokenList)

    @staticmethod
    def term(tokenList):
        token = tokenList[0]
        allowedTokenTypes = [t.DIGIT, t.NAME]

        isTerm = token[0] in allowedTokenTypes


class Expression:
    def __init__(self, andCondition, expression=None):
        self.andCondition = andCondition
        self.expression = expression


class AndCondition:
    def __init__(self, condition, andCondition=None):
        self.condition = condition
        self.andCondition = andCondition


class Condition:
    def __init__(self, operandFirst=None, expression=None, isNot=None, compare=None, operandSecond=None, like=None):
        self.operandFirst = operandFirst
        self.expression = expression
        self.isNot = isNot
        self.compare = compare
        self.operandSecond = operandSecond
        self.like = like


class Summand:
    def __init__(self, factor, operator=None, summand=None):
        self.factor = factor
        self.operator = operator
        self.summand = summand


class Factor:
    def __init__(self, term, operator=None, factor=None):
        self.term = term
        self.operator = operator
        self.factor = factor


class Term:
    def __init__(self, value):
        self.value = value
