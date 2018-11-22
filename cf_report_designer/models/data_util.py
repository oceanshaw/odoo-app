# -*- coding: utf-8 -*-
# 康虎软件工作室
# http://www.khcloud.net
# QQ: 360026606
# wechat: 360026606
#--------------------------

"""
AES有5种加密操作模式：
        1. 电码本模式（Electronic Codebook Book (ECB)）
        2. 密码分组链接模式（Cipher Block Chaining (CBC)）
        3. 计算器模式（Counter (CTR)）
        4. 密码反馈模式（Cipher FeedBack (CFB)）
        5. 输出反馈模式（Output FeedBack (OFB)）

用Python实现AES加密和解密
https://blog.csdn.net/zhchs2012/article/details/79032656

一、前言
AES，高级加密标准（英语：Advanced Encryption Standard）。是用来替代DES，目前比较流行的加密算法。
它是一种对称加密算法，与上一篇博文提到过的RSA非对称算法不同，AES只有一个密钥，这个密钥既用来加密，也用于解密。

AES只是个基本算法，实现AES有几种模式，主要有ECB、CBC、CFB和OFB这几种（其实还有个CTR）：

1.ECB模式（电子密码本模式：Electronic codebook）
ECB是最简单的块密码加密模式，加密前根据加密块大小（如AES为128位）分成若干块，之后将每块使用相同的密钥单独加密，解密同理。

2.CBC模式（密码分组链接：Cipher-block chaining）
CBC模式对于每个待加密的密码块在加密前会先与前一个密码块的密文异或然后再用加密器加密。第一个明文块与一个叫初始化向量的数据块异或。

3.CFB模式（密文反馈：Cipher feedback）
与ECB和CBC模式只能够加密块数据不同，CFB能够将块密文（Block Cipher）转换为流密文（Stream Cipher）。

4.OFB模式（输出反馈：Output feedback）
OFB是先用块加密器生成密钥流（Keystream），然后再将密钥流与明文流异或得到密文流，解密是先用块加密器生成密钥流，再将密钥流与密文流异或得到明文，由于异或操作的对称性所以加密和解密的流程是完全一样的。

二、代码实现与解析
照旧先上代码：

from Crypto.Cipher import AES
import base64

class AEScoder():
    def __init__(self):
        self.__encryptKey = "iEpSxImA0vpMUAabsjJWug=="
        self.__key = base64.b64decode(self.__encryptKey)
    # AES加密
    def encrypt(self,data):
        BS = 16
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        cipher = AES.new(self.__key, AES.MODE_ECB)
        encrData = cipher.encrypt(pad(data))
        #encrData = base64.b64encode(encrData)
        return encrData
    # AES解密
    def decrypt(self,encrData):
        #encrData = base64.b64decode(encrData)
        #unpad = lambda s: s[0:-s[len(s)-1]]
        unpad = lambda s: s[0:-s[-1]]
        cipher = AES.new(self.__key, AES.MODE_ECB)
        decrData = unpad(cipher.decrypt(encrData))
        return decrData.decode('utf-8')

简析1：这里采用了面向对象的写法，创建了一个类，同时也偷懒直接把密钥写死成了类的属性。如果有灵活修改密钥的需求，将密钥作为参数传进去即可。
简析2：例子里用了ECB模式，这是AES加密最简单也是很常用的模式。另外一个常用模式是CBC，会比ECB模式多一个初始偏移向量iv：cipher = AES.new(self.__key, AES.MODE_CBC, iv)。
简析3：pad和unpad分别是填充函数和逆填充函数。因为AES加密对加密文本有长度要求，必须是密钥字节数的倍数。这里的encryptKey在经过base64解码后的长度是16个字节。
简析3拓展：实际上AES加密有AES-128、AES-192、AES-256三种，分别对应三种密钥长度128bits（16字节）、192bits（24字节）、256bits（32字节）。当然，密钥越长，安全性越高，加解密花费时间也越长。默认的是AES-128，其安全性完全够用。

填充算法拓展
这里采用的填充算法其实有个专有名词，叫pkcs7padding。
简单解释就是缺几位就补几：填充字符串由一个字节序列组成，每个字节填充该填充字节序列的长度。
如果要填充8个字节,那么填充的字节的值就是0x08；要填充7个字节,那么填入的值就是0x07；以此类推。
如果文本长度正好是BlockSize长度的倍数，也会填充一个BlockSize长度的值。这样的好处是，根据最后一个Byte的填充值即可知道填充字节数。

实际上，java中实现AES加密算法的默认模式是Cipher.getInstance("AES/ECB/PKCS5Padding")
PKCS#5在填充方面，是PKCS#7的一个子集：PKCS#5只是对于8字节（BlockSize=8）进行填充，填充内容为0x01-0x08；但是PKCS#7不仅仅是对8字节填充，其BlockSize范围是1-255字节。
然而因为AES并没有64位（8字节）的块, 如果采用PKCS5, 那么实质上就是采用PKCS7。
"""
import os
import sys
import hashlib
import string
import random
import base64
from binascii import b2a_hex, a2b_hex

from Crypto import Random
from Crypto.Cipher import AES

___1 = ('C') #此处16|24|32个字符
___2 = ('FS') #此处16|24|32个字符
___3 = ('O') #此处16|24|32个字符
___4 = ('F') #此处16|24|32个字符
___5 = ('T') #此处16|24|32个字符
___6 = ('S') #此处16|24|32个字符

def get_machine_code():
    """获取机器码"""
    import uuid
    return str(uuid.UUID(int=uuid.getnode()))

___7 = ('t') #此处16|24|32个字符
___8 = ('u') #此处16|24|32个字符
___9 = ('d') #此处16|24|32个字符
___10 = ('i') #此处16|24|32个字符
___11 = ('o72') #此处16|24|32个字符
___12 = ('0') #此处16|24|32个字符
___13 = ('1') #此处16|24|32个字符

AES_IV = "1234567890123456"

def get__():
    return ''.join(___1+___2+___3+___4+___5+___6+___7+___8+___9+___10+___11+___12+___13)

# padding算法
BS = len(get__())
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class AESCoder(object):
    """
        使用示例:
        aes_encrypt = AESCoder()
        text = "python 加密"
        e = aes_encrypt.encrypt(text)
        d = aes_encrypt.decrypt(e)
        print text
        print e
        print d

        e = "ZBt7JVo0hubHZ5FLIhngEaz+n46vQfHTGxa1cL4CqA8="
        d = aes_encrypt.decrypt(e)
        print d
    """
    def __init__(self, key=False, mode=AES.MODE_CBC):
        self.key = key or get__()
        self.mode = mode

    @staticmethod
    def rand_aes_key(size=16, by_base64=True, chars = string.ascii_uppercase + string.digits):
        """
        :param size:  生成随机字符串的长度，可选值为16、24、32
        :param chars:  生成字符串的取值范围
        :param by_base64:  是否编码为base64
        :return:
        """
        res =  ''.join(random.choice(chars) for _ in range(size))
        return base64.b64encode(res) if by_base64 else res

    #加密函数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, AES_IV)
        self.ciphertext = cryptor.encrypt(pad(text))
        #AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
        return base64.b64encode(self.ciphertext)

    #解密函数
    def decrypt(self, text):
        decode = base64.b64decode(text)
        cryptor = AES.new(self.key, self.mode, AES_IV)
        plain_text = cryptor.decrypt(decode)
        return plain_text


# # padding算法
# BS = AES.block_size # aes数据分组长度为128 bit
# pad = lambda s: s + (BS - len(s) % BS) * chr(0)
#
# # 内容编码方式
#
# ENCODE_HEX = 1
# ENCODE_BASE16 = 2
# ENCODE_BASE32 = 3
# ENCODE_BASE64 = 4
# ENCODE_BASE91 = 5
# ENCODE_BASE128 = 6
# ENCODE_ASCII85 = 7
#
# class AESCoder:
#     """
#     example:
#
#     msg = "00000000-0000-0000-0000-185e0f17f231"
#     key = AESCoder.rand_aes_key(16, False)
#     aes = AESCoder(key, AES.MODE_CBC)
#     msg1 = aes.encrypt(msg)
#     print(msg1)
#     msg2 = aes.decrypt(msg1)
#     print(msg2)
#     """
#     def __init__(self, key, mode):
#         self.key = key
#         self.mode = mode
#         self.encode_method = ENCODE_BASE64
#
#     def set_encode_method(self, method=ENCODE_BASE64):
#         self.encode_method = method
#
#     @staticmethod
#     def rand_aes_key(size=16, by_base64=True, chars = string.ascii_uppercase + string.digits):
#         """
#         :param size:  生成随机字符串的长度，可选值为16、24、32
#         :param chars:  生成字符串的取值范围
#         :param by_base64:  是否编码为base64
#         :return:
#         """
#         res =  ''.join(random.choice(chars) for _ in range(size))
#         return base64.b64encode(res) if by_base64 else res
#
#     def encrypt(self, plaintext):
#         """
#         加密
#         :param plaintext: 待加密文本
#         :return:
#         """
#
#         # 生成随机初始向量IV
#         iv = Random.new().read(AES.block_size)
#         cryptor = AES.new(self.key, self.mode, iv)
#         ciphertext = cryptor.encrypt(pad(plaintext))
#         # 这里统一把加密后的字符串转化为16进制字符串
#         # 在下节介绍base64时解释原因
#         if self.encode_method == ENCODE_HEX:
#             return b2a_hex(iv + ciphertext)
#         else:
#             return base64.b64encode(iv + ciphertext)
#
#
#     def decrypt(self, ciphertext):
#         """
#         解密
#         :param ciphertext: 待解密文本
#         :return:
#         """
#         if self.encode_method == ENCODE_HEX:
#             ciphertext = a2b_hex(ciphertext)
#         else:
#             ciphertext = base64.b64decode(ciphertext)
#
#         iv = ciphertext[0:AES.block_size]
#         ciphertext = ciphertext[AES.block_size:len(ciphertext)]
#         cryptor = AES.new(self.key, self.mode, iv)
#         plaintext = cryptor.decrypt(ciphertext)
#         plaintext = plaintext.rstrip(chr(0))
#         return plaintext


from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA

class RSACipher():
    """
    RSA加密
    生成密钥对：
    rsa = RSACipher( pri_key='pri.pem', pub_key='pub.pem', key_path="./")
    rsa.gen_key_pair()

    加密：
    rsa = RSACipher( pri_key='pri.pem', pub_key='pub.pem', key_path="./")
    cipher_text = rsa.encrypt_str("00000000-0000-0000-0000-185e0f17f231")

    解密：
    rsa = RSACipher( pri_key='pri.pem', pub_key='pub.pem', key_path="./")
    cipher_text = rsa.decrypt_str("jUKq3d17wx7RoZ/mlEBBS/MVVLcoI5FWvkslVUmq1ApgQfnxzoT2gmjub4mS+f2ApIZxoXKHQQWmYCbgin5pxw==")
    """

    def __init__(self, pri_key='pri.pem', pub_key='pub.pem', key_path=os.path.abspath(os.path.dirname(__file__))):
        self.KEY_PRIVATE = pri_key
        self.KEY_PUBLIC = pub_key
        self.KEY_PATH = key_path

    def gen_key_pair(self):
        # 伪随机数生成器
        random_generator = Random.new().read
        # rsa算法生成实例
        rsa = RSA.generate(1024, random_generator)

        # master的秘钥对的生成
        private_pem = rsa.exportKey()

        with open(self.KEY_PATH + "/" + self.KEY_PRIVATE, 'w') as f:
            f.write(private_pem)

        public_pem = rsa.publickey().exportKey()
        with open(self.KEY_PATH + "/" + self.KEY_PUBLIC, 'w') as f:
            f.write(public_pem)

    def decrypt_str(self, encrypt_text):
        # 伪随机数生成器
        _key_path = self.KEY_PATH + "/" + self.KEY_PUBLIC
        if not os.path.isfile(_key_path):
            raise Exception("Decrypt key not exist or invalid!")

        random_generator = Random.new().read
        with open(self.KEY_PATH + "/" + self.KEY_PRIVATE) as f:
            key = f.read()
            rsakey = RSA.importKey(key)
            cipher = Cipher_pkcs1_v1_5.new(rsakey)
            plain_text = cipher.decrypt(base64.b64decode(encrypt_text), random_generator)
            return plain_text

    def encrypt_str(self, message):
        _key_path = self.KEY_PATH + "/" + self.KEY_PUBLIC
        if not os.path.isfile(_key_path):
            raise Exception("Encrypt key not exist or invalid!")

        with open(_key_path) as f:
            key = f.read()
            rsakey = RSA.importKey(key)
            cipher = Cipher_pkcs1_v1_5.new(rsakey)
            cipher_text = base64.b64encode(cipher.encrypt(message))
            return cipher_text


# plain_text = """11月2日召开的国务院常务会议公布了社保降费率的最新政策："""
#
# rsa = RSACipher( pri_key='pri.pem', pub_key='pub.pem', key_path="./")
# rsa.gen_key_pair()
# encrypted_text = rsa.encrypt_str(plain_text)
# print(encrypted_text)
# decrypted_text = rsa.decrypt_str(encrypted_text)
# print(decrypted_text)

