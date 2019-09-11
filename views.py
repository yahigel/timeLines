from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Post
from .forms import PostForm
from bs4 import BeautifulSoup

import sys
import codecs
import requests
import re
import time

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

#初期表示
def index(request):
    posts = Post.objects.all()
    form = PostForm()
    context = {'form': form}
    return render(request,'timeLines/index.html',context)


#create押下後
def create(request):

	#リクエストから年表作成ワードと項目数を取得
    form = PostForm(request.POST)
    searchWord = request.POST["年表作成ワード"]
    rimitKomoku = int(request.POST["項目数"])

	#取得した年表作成ワードで年表作成
    resultList = getTL(searchWord, "")

	#取得した年表作成ワードで記事内のアンカリンク取得
    linkDic = getLinkDic(searchWord)

	#年表作成ワードの検索結果より少ないものを検索結果のリストに追加
    searchWordResultListRength = len(resultList)
    for keyword in linkDic:
        TL = getTL(keyword, linkDic[keyword])
        if searchWordResultListRength > len(TL):
            resultList = resultList + TL
            if len(resultList) > rimitKomoku:
                break

    resultList.sort()
    context = {'form': form,'resultList':resultList}
    return render(request,'timeLines/index.html',context)


#引数を元にしたアンカリンクの辞書を返す。
def getLinkDic(searchWord):
    linkDic = {}
    try:
        html_doc = requests.get("https://ja.wikipedia.org/wiki/" + searchWord).text
    except Exception as err:
        return linkDic

    soup = BeautifulSoup(html_doc, 'html.parser') # BeautifulSoupの初期化
    scriptIndex = soup.find('div', id="bodyContent")
    real_page_tags = scriptIndex.find_all("a")
    for tag in real_page_tags:
        tagUrl = tag.get("href")
        if tagUrl is not None:
            if "#" != tagUrl[:1] and "/wiki/Category:" != tagUrl[:15] and "/wiki/Portal:" != tagUrl[:13]:
                linkDic[tag.text] = tag.get("href")
    return linkDic


#引数を元にした年表リストを返す。
def getTL(searchWord, linkUrl):
    #キーワードが何年、何月、何日などであった場合空のリストを返す
    jikouList=[]
    if re.match('.*(\d+年)', searchWord) is not None:
        return jikouList
    if re.match('.*(\d+月\d+日)', searchWord) is not None:
        return jikouList

    #linkUrlが存在する場合linkUrlで、無い場合はキーワードで検索
    if len(linkUrl) > 0:
        try:
            html_doc = requests.get("https://ja.wikipedia.org" + linkUrl).text
        except Exception as err:
            return jikouList
    else:
        try:
            html_doc = requests.get("https://ja.wikipedia.org/wiki/" + searchWord).text
        except Exception as err:
            return jikouList

    #BeautifulSoupの初期化
    soup = BeautifulSoup(html_doc, 'html.parser')

    #bodyContentの取得
    scriptIndex = soup.find('div', id="bodyContent")
    try:
        honbun = scriptIndex.text
    except AttributeError as err:
        return jikouList

	#---------------------------------年表作成のために記事を編集 ここから---------------------------------
    chikan = honbun.replace('\n','')

    matchedList = re.findall(r"[0-9][0-9][0-9]+年",chikan)
    for matched in matchedList:
        chikan = chikan.replace(matched,'\n' + matched)

    chikan = re.sub(r"[　 \t]+",'',chikan)
    chikan = re.sub(r"\n+",'\n',chikan)
    chikan = re.sub(r"[。].*\n",'。\n',chikan)
    chikan = re.sub(r"^(?!.*。).+$",'',chikan, flags=re.MULTILINE)
    chikan = re.sub(r"\[[0-9]+\]",'',chikan, flags=re.MULTILINE)
    chikan = re.sub(r"\[編集\]",'',chikan, flags=re.MULTILINE)

    #元号の表示を削除
    GENGO = "[令和平成昭和大正明治慶応元治文久万延安政嘉永弘化天保文政文化享和寛政天明安永明和宝暦寛延延享寛保元文享保正徳宝永元禄貞享天和延宝寛文万治明暦承応慶安正保寛永元和慶長文禄天正元亀永禄弘治天文享禄大永永正文亀明応延徳長享文明応仁文正寛正長禄康正享徳宝徳文安嘉吉永享正長応永明徳康応嘉慶至徳永徳康暦永和応安貞治康安延文文和観応貞和康永暦応元中弘和天授文中建徳正平興国延元建武正慶元弘元徳嘉暦正中元亨元応文保正和応長延慶徳治嘉元乾元正安永仁正応弘安建治文永弘長文応正元正嘉康元建長宝治寛元仁治延応暦仁嘉禎文暦天福貞永寛喜安貞嘉禄元仁貞応承久建保建暦承元建永元久建仁正治建久文治元暦寿永養和治承安元承安嘉応仁安永万長寛応保永暦平治保元久寿仁平久安天養康治永治保延長承天承大治天治保安元永永久天永天仁嘉承長治康和承徳永長嘉保寛治応徳永保承暦承保延久治暦康平天喜永承寛徳長久長暦長元万寿治安寛仁長和寛弘長保長徳正暦永祚永延寛和永観天元貞元天延天禄安和康保応和天徳天暦天慶承平延長延喜昌泰寛平仁和元慶貞観天安斉衡仁寿嘉祥承和天長弘仁大同延暦天応宝亀神護景雲天平神護天平宝字天平勝宝天平感宝天平神亀養老霊亀和銅慶雲大宝朱鳥白雉大化]"
    chikan = re.sub(r"（"+ GENGO + GENGO + "[0-9]+年）",'',chikan)
    chikan = re.sub(r"（"+ GENGO + GENGO + "元年）",'',chikan)

    #括弧が片方のみの行を削除
    chikan = re.sub(r"^.*（(?!.*）).+$",'',chikan, flags=re.MULTILINE)
    chikan = re.sub(r"^(?!.*（).+）.*$",'',chikan, flags=re.MULTILINE)

    SUBPAT="[ - に、の頃かけてころ春夏秋冬）上旬下旬元旦ごろまはで。]"
    matchedList2 = re.findall(r"[0-9][年月日]" + SUBPAT + "*",chikan)
    for matched in matchedList2:
        chikan = chikan.replace(matched, re.sub(r""+ SUBPAT + "+",'\t',matched))
    chikan = re.sub(r"\t+",'\t',chikan)
    chikan = re.sub(r"\t+",'\t',chikan)
    chikan = re.sub(r"- ",'',chikan)
    chikan = re.sub(r"^.*頁.+$",'',chikan, flags=re.MULTILINE)
    chikan = re.sub(r"^.*p\..+$",'',chikan, flags=re.MULTILINE)
    chikan = re.sub(r"^.*[年月日][。].*$",'',chikan, flags=re.MULTILINE)

    matchedList3 = re.findall(r"[0-9][年月日]（.+）" + SUBPAT + "+",chikan)
    for matched in matchedList3:
        chikan = chikan.replace(matched, re.sub(r"（.+）",'',matched))

    chikan = re.sub(r"^(?!.*[年月日]).+$",'',chikan, flags=re.MULTILINE)
    chikan = re.sub(r"^.*閲覧。\n",'',chikan, flags=re.MULTILINE)
    chikan = re.sub(r"^.*アーカイブ。\n",'',chikan, flags=re.MULTILINE)
    chikan = re.sub(r"^.*カテゴリ.*\n",'',chikan, flags=re.MULTILINE)
    chikan = re.sub(r"^.*にて。\n",'',chikan, flags=re.MULTILINE)

    chikan = re.sub(r"^\n",'',chikan, flags=re.MULTILINE)
    chikan = re.sub(r"\n",'\t'+ searchWord +'\n',chikan, flags=re.MULTILINE)
    jikouList = chikan.split("\n") 
    jikouList.sort()
	#---------------------------------年表作成のために記事を編集 ここまで---------------------------------

    for jikou in jikouList:
        if len(jikou) < 20:
            jikouList.remove(jikou)
        if 'iki' in jikou:
            jikouList.remove(jikou)

    return jikouList
