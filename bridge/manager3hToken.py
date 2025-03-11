# -*- coding: utf-8 -*-
import base64

class Encript3hTokenUtil():

    def __init__(self):
        self.pattern_token = ['{','}','J','o','#','h','i','7','G','H','I','j','s','?','R','K','M','S','k','Q','a','d','D','E','T','V','n','N','F','l','m','r','p','q','W','X','Y','5','6','L','c','Z','2','A','B','C','t','b','v','w','x','y','z','1','g','8','9','@','O','P',' ','3','4','.','e','f','0']
        self.pattern_3hash = ['{','}','v','w','S','#','T','V','W','C','D','1','x','?','Q','R','i','7','E','5','@','2','A','B','o','p','O','P','6','k','Y','K','l','m','8','n','F','r','G',' ','N','X','L','M','c','d','z','.','0','s','t','j','H','3','4','Z','9','a','b','I','J','e','f','g','h','q','y']

    def encript3h(self, textPlain):
        result = ""
        index = 0
        for character in textPlain:
            result += self.encript3HChar(character, len(textPlain), index)
            index += 1
        return result

    def encript3HChar(self,character, size, token_index):
        if character in self.pattern_token:
            p_index = self.pattern_token.index(character)
            indice = (p_index + size + token_index) % len(self.pattern_token)
            return self.pattern_3hash[indice]
        return character

    def decript3H(self, textPlain):
        result = ""
        index = 0
        for character in textPlain:
            result += self.dencript3HChar(character, len(textPlain), index)
            index += 1
        return result

    def dencript3HChar(self, character, size, token_index):
        indice = 0
        if character in self.pattern_3hash:
            if (self.pattern_3hash.index(character) - size - token_index) > 0:
                indice = (self.pattern_3hash.index(character) - size - token_index) % len(self.pattern_3hash)
            else:
                indice = len(self.pattern_token) + (self.pattern_3hash.index(character) - size - token_index) % len(self.pattern_3hash)
            indice = indice % len(self.pattern_3hash)
            return self.pattern_token[indice]
        else:
            return character


class DataBridge():

    def __init__(self, data3HToken):
        encript = Encript3hTokenUtil()
        clearInfo = encript.decript3H(data3HToken)
        self.textPlainMessage = clearInfo
        self.origin = clearInfo[:64]
        self.mac, self.originClient, self.version  = self.origin.split('#')
        self.sequence = clearInfo[-16:]
        self.content = base64.b64decode(clearInfo[64:-16])


if __name__ == '__main__':
    texto = input("Texto a encriptar:\n")
    encripta = Encript3hTokenUtil()
    result = encripta.encript3h(texto)
    print("Encriptado       :[{}]".format(result))
    print("Desencriptado    :[{}]".format(encripta.decript3H(result)))
