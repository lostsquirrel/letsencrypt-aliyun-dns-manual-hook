## 工具介绍
Let’s Encrypt通配符证书申请，只能用DNS plugins的验证方式。其原理就是依照提示增加某个TXT记录的域名进行验证。整个流程都是需要配合certbot的提示并手动执行。  
如果想自动完成这个过程，根据官方文档提供的资料，需要写有两个hook脚本来替代人工操作：  
- **--manual-auth-hook**  
- **--manual-cleanup-hook**

这个工具是专门针对阿里云（万网）域名使用的，其他域名供应商的请勿使用。

## 使用步骤
### 一、下载代码
```
git clone https://github.com/lostsquirrel/letsencrypt-aliyun-dns-manual-hook.git
docker build -t certbot/alidns:v1.0.0 .
```

### 二、配置appid和appsecret
首先去自己的阿里云域名管理后台，申请有增加和删除域名权限的appid和appsecret。具体申请步骤请自行摸索，网上应该有很多资料。  
然后把申请好的appid和appsecret填入到**config.ini**文件中。
```
[aliyun]
appid=your-appid
appsecret=your-appsecret
```

### 三、申请通配符证书
官方的证书申请工具certbot，有两个参数 **--manual-auth-hook** 和 **--manual-cleanup-hook**  
即分别指定脚本，去增加TXT记录的域名和删除。

所以配合到本工具使用就是：
```
certbot certonly \
...
--manual-auth-hook 'python /path/to/manual-hook.py --auth' \
--manual-cleanup-hook 'python /path/to/manual-hook.py --cleanup'
```

使用方法
```
docker run -it --rm --net host --name certbot \
            -v "/etc/letsencrypt:/etc/letsencrypt" \
            -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
            -v "$(PWD)/config.ini:/etc/alidns/config.ini" \
            certbot/alidns:v1.0.0 \
            certonly -a manual \
            --email your-email@example.com \
            --preferred-challenges dns-01 \
            --server https://acme-v02.api.letsencrypt.org/directory \
            -d *.yourdomain.com
```

如果想强制生成或者更新通配符证书，则使用 **-f** 参数
```

```

如使用过程有任何问题，欢迎issue。
