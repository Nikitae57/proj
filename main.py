from tree_builders.ast_builder import AstBuilder
from tokenize.reader import Reader
from tokenize.token_list_builder import TokenListBuilder

wordList = Reader.readSql('test/1')
tokenList = TokenListBuilder.buildTokenList(wordList)
astTree = AstBuilder.buildAst(tokenList)

print(tokenList)


