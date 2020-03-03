from reader import Reader
from token_list_builder import TokenListBuilder

wordList = Reader.readSql('1')
tokenList = TokenListBuilder.buildTokenList(wordList)
print(tokenList)


