from django.contrib import admin

from .models import Category,Park,Tag,Review,UserMessage,UserMessageGroup

#Adminクラスを作る(管理サイト上の表記を変えることができる)
class UserMessageAdmin(admin.ModelAdmin):
    #一覧表示時に表示させるフィールドを指定する
    list_display = [ "dt","content","user","group" ]


class UserMessageGroupAdmin(admin.ModelAdmin):

    #TIPS:多対多のlist_displayで指定できない。ループして所属ユーザーを作った上で表示させる。
    list_display    = [ "dt","user_list" ]

    def user_list(self,obj):
        users  = []
        for user in obj.user.all():
            users.append(user)

        return users



admin.site.register(Category)
admin.site.register(Park)
admin.site.register(Tag)
admin.site.register(Review)

#Adminクラスを指定する
admin.site.register(UserMessage,UserMessageAdmin)
admin.site.register(UserMessageGroup,UserMessageGroupAdmin)

