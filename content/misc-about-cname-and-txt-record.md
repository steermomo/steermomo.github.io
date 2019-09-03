Title: namecheap中设置裸域CNAME与TXT解析的问题 
Date: 2019-09-03 18:20
Modified: 2019-09-03 18:20
Category: DNS,
Tags: DNS, CNAME, namecheap, 
Slug: 
Summary: 

起因是我在Google Search Console中设置自己的域名, 在namecheap配置了TXT记录, 却一直查不到对应的TXT解析结果. 不管是等半天还是重新设置都不管用. 


解析的结果
```bash
$ dig steer.space -t TXT

; <<>> DiG 9.11.3-1ubuntu1.5-Ubuntu <<>> steer.space -t TXT
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 18305
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;steer.space.                   IN      TXT

;; ANSWER SECTION:
steer.space.            1799    IN      CNAME   steermomo.github.io.

;; AUTHORITY SECTION:
github.io.              900     IN      SOA     ns-1622.awsdns-10.co.uk. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400

;; Query time: 352 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Tue Sep 03 10:36:30 CST 2019
;; MSG SIZE  rcvd: 160
```

看namecheap的文档说明[^1], 才发现一个问题
>  **NOTE:** Before setting up your mail service, be sure that there is no CNAME record created for a **bare domain**, (e.g., *yourdomain.tld*) in the **Host records** section, or email will not work correctly. CNAME has the highest priority and prevails over all the other records for the host name, including MX Records which are responsible for mail delivery.



我在裸域上直接设置了CNAME, 解析到github pages, 而CNAME的优先级最高, 会忽略所有其他的记录. 如果想要设置Google search console的话, 站点只能绑定到子域名上, 而反之则不行.







[^1]: [NAMECHEAP:How can I set up MX records required for mail service?](https://www.namecheap.com/support/knowledgebase/article.aspx/322/2237/how-can-i-set-up-mx-records-required-for-mail-service)