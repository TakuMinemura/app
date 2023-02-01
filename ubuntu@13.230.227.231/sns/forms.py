from django import forms

from .models import Park,Review,UserMessageGroup,UserMessage

#ユーザーモデルのフォームを作る
#from django.contrib.auth.models import User

#カスタムユーザーモデルのフォームを作る
from users.models import CustomUser


class ParkForm(forms.ModelForm):

    class Meta:
        model   = Park
        fields  = ["category","name","tag","lat","lon"]

class CategorySearchForm(forms.ModelForm):
    class Meta:
        # ForeignKeyフィールドを使うことで、1対多の1側に存在するidであることをチェックできる。
        model   = Park
        fields  = ["category"]

class TagSearchForm(forms.ModelForm):

    class Meta:
        model   = Park
        fields  = ["tag"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model   = Review
        fields  = ["park","comment","star","user"] #userフィールドをバリデーションする


#ユーザーの姓名を書き換える
class UserForm(forms.ModelForm):
    class Meta:
        model   = CustomUser
        fields  = ["first_name","last_name"]


#ユーザー詳細情報をバリデーションする
class UserDetailForm(forms.ModelForm):
    class Meta:
        model   = CustomUser
        fields  = ["nickname","description","icon","birthday"]






class UserMessageGroupForm(forms.ModelForm):
    class Meta:
        model   = UserMessageGroup
        fields  = [ "user" ]

#メッセージのフォーム
class UserMessageForm(forms.ModelForm):
    class Meta:
        model   = UserMessage
        fields  = [ "group","content","user" ]


