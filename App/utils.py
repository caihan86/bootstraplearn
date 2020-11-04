import base64
from urllib import parse

from Cryptodome import Random
from Cryptodome.Cipher import PKCS1_v1_5

from Cryptodome.PublicKey import RSA
from django.conf import settings


def create_rsa_key():
    """
    创建RSA密钥
    步骤说明：
    1、从 Crypto.PublicKey 包中导入 RSA，创建一个密码
    2、生成 1024/2048 位的 RSA 密钥
    3、调用 RSA 密钥实例的 exportKey 方法，传入口令、使用的 PKCS 标准以及加密方案这三个参数。
    4、将私钥写入磁盘的文件。
    5、使用方法链调用 publickey 和 exportKey 方法生成公钥，写入磁盘上的文件。
    """
    # 利用伪随机数来生成私钥和公钥
    random_generator = Random.new().read

    key = RSA.generate(2048,random_generator) #生成 1024/2048 位的 RSA 密钥
    encrypted_key = key.exportKey() #密钥实例
    with open("my_private_rsa_key.bin", "wb") as f:#私钥写入磁盘
        f.write(encrypted_key)
    with open("my_rsa_public.pem", "wb") as f: #公钥写入磁盘
        f.write(key.publickey().exportKey())

# if __name__ == '__main__':
#     create_rsa_key()
def decrypt_data(inputdata):
    # URLDecode
    data = parse.unquote(inputdata)
    # base64decode
    data = base64.b64decode(data)
    # 读取密钥
    private_key = RSA.import_key(settings.RSA_PRIVATE_KEY)
    # 使用 PKCS1_v1_5解密
    cipher_rsa = PKCS1_v1_5.new(private_key)
    # 当解密失败，会返回 sentinel
    sentinel = None
    ret = cipher_rsa.decrypt(data, sentinel)
    return ret.decode() #解码