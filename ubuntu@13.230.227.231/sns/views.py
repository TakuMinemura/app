from django.shortcuts import render,redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Park,Category,Tag,Review,UserMessage,UserMessageGroup
from .forms import ParkForm,CategorySearchForm,TagSearchForm,ReviewForm,UserForm,UserDetailForm,UserMessageForm,UserMessageGroupForm

from django.db.models import Q
from django.db.models import Count

from users.models import CustomUser



#LoginRequiredMixinにより未認証ユーザーはこのIndexViewが実行されず。ログインページへリダイレクトされる。
class IndexView(LoginRequiredMixin,View):

    #重複を除去する。(モデルオブジェクトから重複を取り除く)
    def distinct(self,obj):
        id_list     = [] # モデルオブエジェクトのidを記録する
        new_obj     = [] # 重複を除去した新しいモデルオブジェクトのリスト

        #モデルオブジェクトのリストから1つ取り出す。
        for o in obj:
            # idがid_listに含まれている場合
            if o.id in id_list:
                #次のループに行く(for文で使える構文、この命令を実行すると以降の処理はスキップして次のループに行く)
                continue

            #モデルオブジェクトのidを記録する
            id_list.append(o.id)
            #モデルオブジェクトを新しいリストに入れる
            new_obj.append(o)

        return new_obj

    def get(self, request, *args, **kwargs):

        context = {}
        context["categories"]   = Category.objects.all()
        context["tags"]         = Tag.objects.all()

        #TODO:ここで公園を検索するバリデーションを行う。

        #公園名の検索
        query   = Q()


        #パラメータの中にsearchがあるかどうかをチェック
        if "search" in request.GET:
            #searchを取り出す
            search      = request.GET["search"]

            raw_words   = search.replace("　"," ").split(" ")
            words       = [ w for w in raw_words if w != "" ]

            for w in words:
                query &= Q(name__contains=w)


        #カテゴリの検索
        form    = CategorySearchForm(request.GET)

        #カテゴリ検索を実現するには、入力値が数値であること、Categoryモデルに存在するidであることを確認する必要がある
        if form.is_valid():
            cleaned = form.clean()
            query &= Q(category=cleaned["category"].id)


        #多対多の検索
        form    = TagSearchForm(request.GET)

        if form.is_valid():
            # request.GET["tag"] = 全て文字列型 クエリパラメータ(クエリストリング)
            # cleaned = { "tag":["id","id",] }
            cleaned         = form.clean()
            selected_tags   = cleaned["tag"] 
            
            """
            #タグ未指定による検索を除外する(タグ未選択でもバリデーションOKになるので、ここで空リストを除外する)
            if selected_tags:
                # 指定したタグのいずれかを含む検索(重複あり)
                query &= Q(tag__in=selected_tags)
                
            for selected_tag in selected_tags:
                query &= Q(tag__in=selected_tag)
            """

            #公園で検索した結果
            parks       = Park.objects.filter(query).order_by("-dt")

            #タグ検索をする(中間テーブル未使用、指定したタグを全て含む)
            for tag in selected_tags:
                #絞り込みした結果の一時的に格納するリスト
                #new_parks   = []
                """
                #内包表記でも可
                for park in parks:
                    if tag in park.tag.all():
                        #指定したタグを含むモデルオブジェクトをnew_parksにアペンド
                        new_parks.append(park)
                """

                #new_parks = [ park for park in parks if tag in park.tag.all() ]

                #次の絞り込みで使用するため、parksへ代入(上書き)
                #parks       = new_parks

                #選択されたタグを含む公園(parks)のみを絞り込んでいく
                parks       = [ park for park in parks if tag in park.tag.all() ]

            print(parks)
            context["parks"]    = parks
        else:

            #ここでループしてモデルオブジェクト比較し、重複除去をする。
            context["parks"]    = Park.objects.filter(query).order_by("-dt")

        return render(request, "sns/index.html", context)

    def post(self, request, *args, **kwargs):

        form    = ParkForm(request.POST)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")
            print(form.errors)

        return redirect("sns:index")

index   = IndexView.as_view()

#公園の個別ページ
class SingleView(LoginRequiredMixin,View):
    def get(self, request, pk, *args, **kwargs):

        context = {}
        context["park"]     = Park.objects.filter(id=pk).first()
        context["reviews"]  = Review.objects.filter(park=pk).order_by("-dt")

        return render(request,"sns/single.html",context)

    def post(self, request, pk, *args, **kwargs):

        copied          = request.POST.copy()
        copied["park"]  = pk
        copied["user"]  = request.user.id

        form    = ReviewForm(copied)

        if form.is_valid():
            form.save()

        return redirect("sns:single", pk)

single  = SingleView.as_view()


#マイページ
class MypageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        context                 = {}
        context["user"]         = CustomUser.objects.filter(id=request.user.id).first()

        #TODO:ここでメッセージを表示する。
        context["groups"]       = UserMessageGroup.objects.filter(user=request.user.id).order_by("-dt")


        return render(request, "sns/mypage.html", context)

    def post(self, request, *args, **kwargs):


        print(request.POST)

        #first_nameとlast_nameの保存
        user    = CustomUser.objects.filter(id=request.user.id).first()
        form    = UserForm(request.POST,instance=user)

        #バリデーションNGの場合はここでリダイレクト
        if not form.is_valid():
            print(form.errors)
            return redirect("sns:mypage")

        form.save()



        #ユーザー詳細情報の保存
        form    = UserDetailForm(request.POST,request.FILES,instance=user)

        print(form)

        if not form.is_valid():
            print(form.errors)
            return redirect("sns:mypage")

        data    = form.save()


        print("保存")

        return redirect("sns:mypage")

mypage  = MypageView.as_view()


#ユーザー個別ページ
class UserView(LoginRequiredMixin,View):
    def get(self, request, pk, *args, **kwargs):

        context                 = {}
        context["user"]         = CustomUser.objects.filter(id=pk).first()

        return render(request, "sns/user.html", context)

    def post(self, request, pk, *args, **kwargs):

        #TODO:メッセージグループを作る
        dic             = {}
        #多対多のフィールドを保存する時、リスト型でバリデーションして保存する
        dic["user"]     = [ pk, request.user.id ]

        form    = UserMessageGroupForm(dic)

        if form.is_valid():
            print("グループ作成")
            form.save()
        else:
            print(form.errors)

        return redirect("sns:user",pk)

user    = UserView.as_view()


#メッセージの投稿
class MessageView(LoginRequiredMixin,View):

    def post(self, request, *args, **kwargs):

        copied          = request.POST.copy()
        copied["user"]  = request.user.id 

        form    = UserMessageForm(copied)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return redirect("sns:mypage")

message = MessageView.as_view()


#TODO:ここにメッセージを削除するビューを作る(メッセージのpkを指定して、削除する)



