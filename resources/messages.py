from flask import jsonify, Blueprint,abort,make_response
from flask_restful import Resource,Api,reqparse,fields,marshal,marshal_with

import models

message_fields={
    'id':fields.Integer,
    'content':fields.String,
    'published_at':fields.String
}

def get_or_abort(id):
    try:
        msg=models.Message.get_by_id(id)
    except models.Message.DoesNotExist:
        abort(404,description="Massage not found")
    else:
        return msg,200


class BaseMessage(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'content',
            required = True,
            help ='konten wajib ada',
            location =['form','args','json'],

        )
        super().__init__()

class MessageList(BaseMessage):
    def get(self):
        messages=[marshal(message,message_fields)for message in models.Message.select()]
        return make_response(jsonify({'messages':messages}),200)

    def post(self):
        args = self.reqparse.parse_args()
        message=models.Message.create(**args)
        return marshal(message,message_fields),200


class Message(BaseMessage):
    @marshal_with(message_fields)
    def get(self,id):
        return get_or_abort(id)

    def put(self,id):
        args = self.reqparse.parse_args()
        message=models.Message.update(content=args.get('content')).where(models.Message.id == id).execute()
        return make_response(jsonify({'messgae':'berhasil mengupdate'}),200)

    def delete(self,id):
        message=models.Message.delete().where(models.Message.id == id).execute()
        return make_response(jsonify({'messgae':'berhasil menghapus'}),200)
    

messages_api= Blueprint('messages',__name__)
api =Api(messages_api) 

api.add_resource(MessageList, '/messages',endpoint='messages')
api.add_resource(Message, '/message/<int:id>',endpoint='message')