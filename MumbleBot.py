import os
import pymumble_py3 as pymumble
import time
import PyChatGPT


class GPTMumbleBot:

    def __init__(self):
        self.gpt_response = "No Answer from OpenAI!"
        self.openai_conn = PyChatGPT.ChatGPT(api_key=os.environ["OPENAI_API_KEY"])
        self.setup_Mumble_Connection()

    def setup_Mumble_Connection(self):
        host = os.environ["MumbleServer"]
        port = 64738
        user = "gpt"
        password = os.environ["MumbleServerPWD"]
        certfile = os.environ["MumbleCertPath"]
        keyfile = os.environ["MumbleCertKeyPath"]
        self.mumble_conn = pymumble.Mumble(host, user, port, password, certfile, keyfile)
        self.mumble_conn.start()
        self.mumble_conn.is_ready()
        self.mumble_conn.callbacks.set_callback(pymumble.constants.PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, self.message_received)

    def message_received(self, message):
        if len(message.message) > 7 and message.message[:7] == "Hey GPT":
            user_request = message.message[7:]
            self.sendAI_answer(user_request)

    def sendAI_answer(self, user_request):
        self.gpt_response = self.openai_conn.human_request(user_request)
        self.mumble_conn.channels.find_by_name("MumbleGeramble").send_text_message(self.gpt_response)


if __name__ == "__main__":

    MumbleBot = GPTMumbleBot()
    while MumbleBot.mumble_conn.is_alive() and not MumbleBot.mumble_conn.exit:
        time.sleep(2)
