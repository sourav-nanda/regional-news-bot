import requests

class Telegram:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = f'https://api.telegram.org/bot{self.bot_token}'

    def send_message(self, chat_id, text):
        api_url = f'{self.base_url}/sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        response = requests.post(api_url, params=params)
        return response

    def send_document(self, chat_id, document_path):
        api_url = f'{self.base_url}/sendDocument'
        files = {'document': open(document_path, 'rb')}
        data = {'chat_id': chat_id}
        response = requests.post(api_url, files=files, data=data)
        return response

    def send_message_and_document(self, chat_id, text, document_path):
        response_text = self.send_message(chat_id, text)

        message_status="Text message sent successfully" if response_text.status_code == 200 else f"Failed to send text message. Status code: {response_text.status_code}, Response: {response_text.text}"
        
        print(message_status)

        response_document = self.send_document(chat_id, document_path)

        document_status="Document sent successfully" if response_document.status_code == 200 else f"Failed to send document. Status code: {response_document.status_code}, Response: {response_document.text}"
      
        print(document_status)
