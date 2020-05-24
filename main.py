from tree_builders.ast_builder import AstBuilder
from tokenizer.reader import Reader
from tokenizer.token_list_builder import TokenListBuilder

wordList = Reader.readSql('test/1')
tokenList = TokenListBuilder.buildTokenList(wordList)
astTree = AstBuilder.buildAst(tokenList)

print(tokenList)


