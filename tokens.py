from enum import Enum


class Tokens(Enum):
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
