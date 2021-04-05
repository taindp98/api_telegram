import requests
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_pagination import InlineKeyboardPaginator
from telegram import ForceReply

class ConversationManagement:
    def __init__(self,update):

        # if update.message:
            # if update.message.text:
        self.chat_id = update.message.chat.id
        self.msg_id = update.message.message_id
        self.text = update.message.text.encode('utf-8').decode()

        self.converse_api_url = 'https://chatbot-hcmut.herokuapp.com/api/convers-manager'
        self.input_data = {}
        self.input_data['message'] = self.text

        # print('====')
        # print(self.text)

        self.input_data['state_tracker_id'] = self.chat_id
        self.list_mess_response = []

        self.total_page = 0
    

    def process_mess(self):
        response_object = requests.post(url=self.converse_api_url, json=self.input_data)
        response_object_json = response_object.json()

        # print('response_object_json',self.response_object_json)

        self.list_mess_response = [item.replace('\n', r'').replace(r'"',r'') for item in response_object_json['message']]
        
        # print('list_mess_response',self.list_mess_response)
        
        self.total_page = len(self.list_mess_response)

        # print('total_page',self.total_page)

    def render_mess(self,page):
        
        return self.list_mess_response[page-1]

    def single_mess(self,page,bot):

        bot.sendMessage(
            chat_id=self.chat_id, 
            text=self.render_mess(page), 
            reply_to_message_id=self.msg_id
            )

    def paginator(self,page,bot,first_res):

        paginator = InlineKeyboardPaginator(
            page_count = self.total_page,
            current_page=page,
            data_pattern='Trang#{page}'
        )

        if first_res:
            bot.sendMessage(
                chat_id=self.chat_id, 
                # text=text,
                text = self.render_mess(page),
                reply_to_message_id=self.msg_id,
                reply_markup=paginator.markup
                )
        else:
            bot.delete_message(
                self.chat_id,
                self.msg_id
            )
            bot.sendMessage(
                chat_id=self.chat_id, 
                # text=text,
                text = self.render_mess(page),
                reply_to_message_id=self.msg_id,
                reply_markup=paginator.markup
                )
            # bot.editMessageText(
            #     chat_id=self.chat_id, 
            #     # text=text,
            #     text = self.render_mess(page),
            #     message_id = self.msg_id,
            #     # reply_to_message_id=self.msg_id,
            #     # reply_markup=paginator.markup
            #     # reply_markup = ForceReply()
            )
