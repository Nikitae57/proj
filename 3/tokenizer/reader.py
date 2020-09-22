import re


class Reader:
    @staticmethod
    def readSql(filePath):
        with open(filePath) as f:
            line = f.read().replace('\n', '')
            tokens = line.split(' ')
            tokens = [line for line in tokens if line != '']

            returnTokens = []
            for token in tokens:
                if token[len(token) - 1] == ',' and token != ',':
                    returnTokens.append(token[:-1])
                    returnTokens.append(',')
                else:
                    returnTokens.append(token)

            return returnTokens
