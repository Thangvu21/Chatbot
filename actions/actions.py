from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import os
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

# Lấy giá trị từ .env
FASTAPI_URL = os.getenv("FASTAPI_URL")

class ActionAffirm(Action):
    
    def name(self) -> Text:
        return "action_affirm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Cảm ơn bạn đã xác nhận")

        return []

class ActionThanks(Action):

    def name(self) -> Text:
        return "action_thanks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Rất vui đã giúp được bạn, chúc bạn một ngày tốt lành!")

        return []

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
    
class ActionSuggestMovie(Action):

    def name(self) -> Text:
        return "action_suggest_movie"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # truy thêm db gọi BE có thể tự form trả lời luôn
        # gọi rag cho chi tiết hơn hay không
        # phản hồi lại cho người dùng
        dispatcher.utter_message(text="Bạn có thể cho tôi biết thêm thông tin về phim bạn muốn xem được không như thể loại, diễn viên, đạo diễn, năm sản xuất, ...")

        return []
    
class ActionSuggestMovieGenre(Action):
    
    def name(self) -> Text:
        return "action_suggest_movie_genre"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Gửi request đến FastAPI
        user_message = tracker.latest_message.get("text") 
        response = requests.post(FASTAPI_URL, json={"question": user_message})

        if response.status_code == 200:
            data = response.json()
            movie_recommendation = data.get("chatbot_response", "Xin lỗi, tôi không tìm thấy gợi ý nào.")
        else:
            movie_recommendation = "Có lỗi xảy ra khi lấy dữ liệu từ FastAPI."

        # Trả lời user
        dispatcher.utter_message(text=movie_recommendation)

        return []

# Hỏi thông tin phim từ tên phim
class ActionAskMovieGenre(Action):
    
    def name(self) -> Text:
        return "action_ask_movie_genre"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_name = tracker.get_slot("movie")
        if (movie_name == None):
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, bạn vui lòng nhập tên phim bạn muốn xem")
        else:
            # Gọi thử LLM hoặc database để lấy thông tin phim
            # goi BE neu co thi tra ve
            genre = ""

            dispatcher.utter_message(text="Thể loại của bộ phim {} là thể loại{}".format(movie_name, genre))

        return []

class ActionAskMovieDirecter(Action):

    def name(self) -> Text:
        return "action_ask_movie_directer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_name = tracker.get_slot("movie")
        if (movie_name == None):
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, bạn vui lòng nhập tên phim bạn muốn xem")
        else:
            # Gọi thử LLM hoặc database để lấy thông tin phim
            # goi BE neu co thi tra ve
            director = ""

            dispatcher.utter_message(text="Đạo diễn của bộ phim {} là {}".format(movie_name, director))

        return []
    
class ActionAskMovieActor(Action):

    def name(self) -> Text:
        return "action_ask_movie_actor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_name = tracker.get_slot("movie")
        if (movie_name == None):
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, bạn vui lòng nhập tên phim bạn muốn xem")
        else:
            # Gọi thử LLM hoặc database để lấy thông tin phim
            # goi BE neu co thi tra ve
            actor = "abc"

            dispatcher.utter_message(text="Diễn viên của bộ phim {} là {}".format(movie_name, actor))

        return []

# action rep confirm
class ActionUserConfirmMoive(Action):

    def name(self) -> Text:
        return "action_user_confirm_movie"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):
        
        movie_name = tracker.get_slot("movie")

        if not movie_name:
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, vui lòng nhập tên phim.")
            return [SlotSet("movie", None)]  # Đảm bảo slot vẫn rỗng để bot hỏi lại
        
        # Set slot nếu có giá trị movie
        dispatcher.utter_message(text=f"Bạn muốn xem phim {movie_name} nhỉ bạn muốn biết thêm thông tin nào ta?")
        return [SlotSet("movie", movie_name)]

# ACtionAskConfirmedmoive
class ActionAskConfirmedMovie(Action):

    def name(self) -> Text:
        return "action_ask_confirmed_movie"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):
        
        movie_name = tracker.get_slot("movie")

        if not movie_name:
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, vui lòng nhập tên phim.")
            return [SlotSet("movie", None)]  # Đảm bảo slot vẫn rỗng để bot hỏi lại
        
        # Set slot nếu có giá trị movie
        dispatcher.utter_message(text=f"Phim bạn vừa chọn là {movie_name} bạn muốn biết thêm thông tin nào ta?")
        return [SlotSet("movie", movie_name)]