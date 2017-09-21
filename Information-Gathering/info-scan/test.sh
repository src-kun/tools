#! /bin/bash

#SNMP Agent Default Community Name (public) List Host

arr=('www.shandong.gov.cn' 'www.sdzx.gov.cn' 'www.sdrd.gov.cn' 'www.sdtzb.org.cn' 'www.mirror.gov.cn' 'www.sdpeace.gov.cn' 'www.jinan.gov.cn' 'www.qingdao.gov.cn' 'www.zibo.gov.cn' 'www.zaozhuang.gov.cn' 'www.dongying.gov.cn' 'www.yantai.gov.cn' 'www.weifang.gov.cn' 'www.jining.gov.cn' 'www.taian.gov.cn' 'www.taishan.gov.cn' 'www.weihai.gov.cn' 'www.rizhao.gov.cn' 'www.laiwu.gov.cn' 'www.linyi.gov.cn' 'www.dezhou.gov.cn' 'www.liaocheng.gov.cn' 'www.binzhou.gov.cn' 'www.heze.gov.cn' 'dzwww.com' 'dzdaily.com.cn' 'dzwww.net' 'dzwww.com.cn' 'www.iqilu.com' 'www.sdnews.com.cn' 'www.china-sd.com' 'www.sdchina.com' 'www.e23.cn' 'www.qingdaonews.com' 'www.jiaodong.net' 'www.my0538.com' 'www.shm.com.cn' 'www.qlwb.com.cn' 'www.qtv.com.cn  ' 'www.zaozhuangdaily.com.cn' 'www.dongyingnews.cn' 'www.wfcmw.cn' 'www.jn001.com ' 'www.weihai.tv' 'www.rznews.cn' 'www.laiwunews.cn' 'www.ilinyi.net' 'www.dztv.tv' 'www.bzcm.net' 'www.heze.cn' 'www.lcxw.cn' 'www.lcxw.com')

for ip in ${arr[@]}
do
	python bloblast.py $ip
done

