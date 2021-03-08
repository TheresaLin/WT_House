from mongoengine import *


# Create your models here.
class Examples(Document):
    # poem
    meta = {
        # 数据库中显示的名字
        'collection': 'examples'
    }

    _id = SequenceField(required=True, primary_key=True)
    id = StringField()
    path = StringField()
    text = StringField()

    # 可以定义查询集
    @queryset_manager
    def show_newest(doc_cls, queryset):
        # 通过poem_id降序显示
        return queryset.order_by('-_id')


class Ann(Document):
    meta = {
        # 数据库中显示的名字
        'collection': 'annotation'
    }

    _id = SequenceField(required=True, primary_key=True)
    img_path = StringField()
    text = StringField()

    # 可以定义查询集
    @queryset_manager
    def find_same_id(doc_cls, queryset):
        for img_path in annotation.objects:
            return img_path

    def find_same_text(doc_cls, queryset):
        for text in annotation.objects:
            return text



class Ann_Find(Document):
    meta = {
        # 数据库中显示的名字
        'collection': 'annotation'
    }

    _id = SequenceField(required=True, primary_key=True)
    img_path = StringField()
    text = StringField()