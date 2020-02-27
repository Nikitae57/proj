from enum import Enum


class TokensTypes(Enum):
    SELECT = 'SELECT'
    DISTINCT = 'DISTINCT'
    ALL = 'ALL'
    COMMA = ','
    FROM = 'FROM'
    WHERE = 'WHERE'
    GROUP_BY = 'GROUP BY'
    HAVING = 'HAVING'
    ORDER_BY = 'ORDER BY'
    LIMIT = 'LIMIT'
    OPEN_BRACKET = '('
    CLOSE_BRACKET = ')'
    AS = 'AS'
    WILDCARD = '*'

class TokenListBuilder:
    regExpToType = {
        'SELECT': TokensTypes.SELECT,
        'DISTINCT': TokensTypes.DISTINCT,
        'ALL': TokensTypes.ALL,
        ',': TokensTypes.COMMA,
        'GROUP BY': TokensTypes.GROUP_BY,

    }

    @staticmethod
    def buildTokenList(wordsList):
