from utils.CCPSDK.CCPRestSDK import REST
# import ConfigParser


accountSid = '8aaf07087249953401727c857d61199f'
# 说明：主账号，登陆云通讯网站后，可在控制台首页中看到开发者主账号ACCOUNT SID。

accountToken = '7936c612923948e0b4844e47c2168352'
# 说明：主账号Token，登陆云通讯网站后，可在控制台首页中看到开发者主账号AUTH TOKEN。

appId = '8aaf07087249953401727c857e8519a5'
# 请使用管理控制台中已创建应用的APPID。

serverIP = 'app.cloopen.com'
# 说明：请求地址，生产环境配置成app.cloopen.com。

serverPort = '8883'
# 说明：请求端口 ，生产环境为8883.

softVersion = '2013-12-26'  # 说明：REST API版本号保持不变。


# def sendTemplateSMS(to, datas, tempId):
#     # 初始化REST SDK
#     rest = REST(serverIP, serverPort, softVersion)
#     rest.setAccount(accountSid, accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     for k, v in result.iteritems():
#         if k == 'templateSMS':
#             for k, s in v.iteritems():
#                 print
#                 '%s:%s' % (k, s)
#         else:
#             print
#             '%s:%s' % (k, v)

if __name__ == '__main__':
    accountSid = '8aaf07087249953401727c857d61199f'
    accountToken = '7936c612923948e0b4844e47c2168352'
    appId = '8aaf07087249953401727c857e8519a5'

    rest = REST(
        accoundSid=accountSid,
        accountToken=accountToken,
        appId=appId
    )
    ret = rest.sendTemplateSMS(to='18827551859',datas=['xxx','111'],tempId="1")
