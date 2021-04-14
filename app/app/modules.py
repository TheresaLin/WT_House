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
        # data collection
        'collection': 'annotation'
    }

    _id = SequenceField(required=True, primary_key=True)
    img_path = StringField()
    text = StringField()
    status = StringField()
    clientip = StringField()
