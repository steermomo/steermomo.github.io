Title: namecheap中设置裸域CNAME与TXT解析的问题 
Date: 2019-09-03 18:20
Modified: 2019-09-03 18:20
Category: DNS
Tags: DNS, CNAME, namecheap, 
Slug: cname-txt-record-in-namecheap


起因是我在Google Search Console中设置自己的域名, 在namecheap配置了TXT记录, 却一直查不到对应的TXT解析结果. 不管是等半天还是重新设置都不管用. 

看namecheap的文档说明[^1], 才发现一个问题
>  **NOTE:** Before setting up your mail service, be sure that there is no CNAME record created for a **bare domain**, (e.g., *yourdomain.tld*) in the **Host records** section, or email will not work correctly. CNAME has the highest priority and prevails over all the other records for the host name, including MX Records which are responsible for mail delivery.



我在裸域上直接设置了CNAME, 解析到github pages, 而CNAME的优先级最高, 会忽略所有其他的记录. 如果想要设置Google search console的话, 站点只能绑定到子域名上, 而反之则不行.

将github pages绑定到`i`子域名, 再设置裸域的txt解析后, 解析查询正常
```bash
$ dig @8.8.8.8 -t txt steer.space

; <<>> DiG 9.11.3-1ubuntu1.5-Ubuntu <<>> @8.8.8.8 -t txt steer.space
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 47342
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;steer.space.                   IN      TXT

;; ANSWER SECTION:
steer.space.            1798    IN      TXT     "google-site-verification=aaaaaaaaa=============xxxxxxxU"
steer.space.            1799    IN      TXT     "v=spf1 include:xx.xx.registrar-servers.com ~all"

;; Query time: 761 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Tue Sep 03 11:04:35 CST 2019
;; MSG SIZE  rcvd: 184
```

<img src="http://ww1.sinaimg.cn/large/dd456925ly1g6m5d63awhj20mb09x74z.jpg" style="max-width: 80%">



[^1]: [NAMECHEAP:How can I set up MX records required for mail service?](https://www.namecheap.com/support/knowledgebase/article.aspx/322/2237/how-can-i-set-up-mx-records-required-for-mail-service)