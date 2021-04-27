from mongoengine import *


# Create your models here.
class Examples(Document):
    # poem
    meta = {

        'collection': 'examples'
    }

    _id = SequenceField(required=True, primary_key=True)
    id = StringField()
    path = StringField()
    text = StringField()


    @queryset_manager
    def show_newest(doc_cls, queryset):

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

class Val(Document):
    meta = {
            'collection': 'validation'
    }

    _id = SequenceField(required=True, primary_key=True)
    img_path = StringField()
    text = StringField()
    status = StringField()
    clientip = StringField()
    eval_cnt = IntField()
