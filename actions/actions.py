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

        dispatcher.utter_message(text="Xin chào bạn mình là bot nè!")

        return []

# Suggestions  
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

class ActionSuggestMovieDirector(Action):
    
    def name(self) -> Text:
        return "action_suggest_movie_director"

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
    
# Thì có 2 trường hợp 1 là xác nhận lại thông tin phim vừa chọn
# 2 là hỏi thông tin phim từ tên phim
# Hỏi thông tin từ tên phim
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
            genre = "aaa"

            dispatcher.utter_message(text="Thể loại của bộ phim {} là thể loại: {}".format(movie_name, genre))

        return []

class ActionAskMovieDirecter(Action):

    def name(self) -> Text:
        return "action_ask_movie_director"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_name = tracker.get_slot("movie")
        if (movie_name == None):
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, bạn vui lòng nhập tên phim bạn muốn xem")
        else:
            # Gọi thử LLM hoặc database để lấy thông tin phim
            # goi BE neu co thi tra ve
            director = "hhh"

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

class ActionAskMovieLength(Action):

    def name(self) -> Text:
        return "action_ask_movie_length"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_name = tracker.get_slot("movie")
        if (movie_name == None):
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, bạn vui lòng nhập tên phim bạn muốn xem")
        else:
            # Gọi thử LLM hoặc database để lấy thông tin phim
            # goi BE neu co thi tra ve
            length = "120 phút"

            dispatcher.utter_message(text="Thời lượng của bộ phim {} là {}".format(movie_name, length))

        return []

class ActionAskMovieLanguage(Action):

    def name(self) -> Text:
        return "action_ask_movie_language"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_name = tracker.get_slot("movie")
        if (movie_name == None):
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, bạn vui lòng nhập tên phim bạn muốn xem")
        else:
            # Gọi thử LLM hoặc database để lấy thông tin phim
            # goi BE neu co thi tra ve
            language = "Tiếng Anh"

            dispatcher.utter_message(text="Ngôn ngữ của bộ phim {} là {}".format(movie_name, language))

        return []

class ActionAskMoviePlot(Action):

    def name(self) -> Text:
        return "action_ask_movie_plot"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_name = tracker.get_slot("movie")
        if (movie_name == None):
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, bạn vui lòng nhập tên phim bạn muốn xem")
        else:
            # Gọi thử LLM hoặc database để lấy thông tin phim
            # goi BE neu co thi tra ve
            plot = "viruss"

            dispatcher.utter_message(text="Nội dung của bộ phim {} là {}".format(movie_name, plot))

        return []

# Hỏi thông tin từ phim đã chọn
class ActionAskSelectedMovieGenre(Action):
    
    def name(self) -> Text:
        return "action_ask_selected_movie_genre"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_selected = tracker.get_slot("movie_selected")  # Lấy giá trị của slot movie_selected

        if movie_selected is None:
            dispatcher.utter_message(
                text="Bạn chưa chọn bộ phim nào. Vui lòng chọn một bộ phim trước."
            )
        else:
            # Giả sử gọi BE hoặc DB để lấy thông tin thể loại phim
            genre = "Hành động"  # Giá trị này có thể thay đổi theo dữ liệu thực tế

            dispatcher.utter_message(
                text="Thể loại của bộ phim '{}' là: {}".format(movie_selected, genre)
            )

        return []

class ActionAskSelectedMovieDirector(Action):

    def name(self) -> Text:
        return "action_ask_selected_movie_director"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_selected = tracker.get_slot("movie_selected")  # Lấy giá trị của slot movie_selected

        if movie_selected is None:
            dispatcher.utter_message(
                text="Bạn chưa chọn bộ phim nào. Vui lòng chọn một bộ phim trước."
            )
        else:
            # Giả sử gọi BE hoặc DB để lấy thông tin đạo diễn phim
            director = "Christopher Nolan"  # Giá trị này có thể thay đổi theo dữ liệu thực tế

            dispatcher.utter_message(
                text="Đạo diễn của bộ phim '{}' là: {}".format(movie_selected, director)
            )

        return []

class ActionAskSelectedMovieActor(Action):

    def name(self) -> Text:
        return "action_ask_selected_movie_actor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_selected = tracker.get_slot("movie_selected")  # Lấy giá trị của slot movie_selected

        if movie_selected is None:
            dispatcher.utter_message(
                text="Bạn chưa chọn bộ phim nào. Vui lòng chọn một bộ phim trước."
            )
        else:
            # Giả sử gọi BE hoặc DB để lấy thông tin diễn viên phim
            actor = "Leonardo DiCaprio, Brad Pitt"  # Giá trị này có thể thay đổi theo dữ liệu thực tế

            dispatcher.utter_message(
                text="Diễn viên của bộ phim '{}' là: {}".format(movie_selected, actor)
            )

        return []

class ActionAskSelectedMovieLength(Action):

    def name(self) -> Text:
        return "action_ask_selected_movie_length"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_selected = tracker.get_slot("movie_selected")  # Lấy giá trị từ slot movie_selected

        if movie_selected is None:
            dispatcher.utter_message(
                text="Bạn chưa chọn bộ phim nào. Vui lòng chọn một bộ phim trước."
            )
        else:
            # Giả sử gọi BE hoặc DB để lấy thông tin thời lượng phim
            length = "120 phút"  # Giá trị có thể thay đổi dựa vào dữ liệu thực tế

            dispatcher.utter_message(
                text="Thời lượng của bộ phim '{}' là {}".format(movie_selected, length)
            )

        return []
    
class ActionAskSelectedMovieLanguage(Action):

    def name(self) -> Text:
        return "action_ask_selected_movie_language"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_selected = tracker.get_slot("movie_selected")  # Lấy giá trị từ slot movie_selected

        if movie_selected is None:
            dispatcher.utter_message(
                text="Bạn chưa chọn bộ phim nào. Vui lòng chọn một bộ phim trước."
            )
        else:
            # Giả sử gọi BE hoặc DB để lấy thông tin ngôn ngữ phim
            language = "Tiếng Nhật"  # Giá trị có thể thay đổi dựa vào dữ liệu thực tế

            dispatcher.utter_message(
                text="Ngôn ngữ của bộ phim '{}' là {}".format(movie_selected, language)
            )

        return []

class ActionAskSelectedMoviePlot(Action):

    def name(self) -> Text:
        return "action_ask_selected_movie_plot"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_selected = tracker.get_slot("movie_selected")  # Lấy giá trị từ slot movie_selected

        if movie_selected is None:
            dispatcher.utter_message(
                text="Bạn chưa chọn bộ phim nào. Vui lòng chọn một bộ phim trước."
            )
        else:
            # Giả sử gọi BE hoặc DB để lấy thông tin cốt truyện phim
            plot = "Ngọc kem."  # Giá trị có thể thay đổi dựa vào dữ liệu thực tế

            dispatcher.utter_message(
                text="Nội dung của bộ phim '{}' là: {}".format(movie_selected, plot)
            )

        return []

# action rep confirm
class ActionUserConfirmMovie(Action):

    def name(self) -> Text:
        return "action_user_confirm_movie"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        movie_selected = tracker.get_slot("movie")

        if not movie_selected:
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, vui lòng nhập tên phim.")
            return []  # Không cần set slot lại None
        
        dispatcher.utter_message(text=f"Bạn muốn xem phim {movie_selected} nhỉ? Bạn muốn biết thêm thông tin nào không?")
        return [SlotSet("movie_selected", movie_selected)]


# ACtionAskConfirmedmovie
class ActionAskConfirmedMovie(Action):

    def name(self) -> Text:
        return "action_ask_confirmed_movie"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):
        
        movie_name = tracker.get_slot("movie_selected")

        if not movie_name:
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, vui lòng nhập tên phim.")
            return [SlotSet("movie_selected", None)]  # Đảm bảo slot vẫn rỗng để bot hỏi lại
        
        # Set slot nếu có giá trị movie
        dispatcher.utter_message(text=f"Phim bạn vừa chọn là {movie_name} bạn muốn biết thêm thông tin nào ta?")
        return [SlotSet("movie_selected", movie_name)]
    
# schedule action
class ActionAskMovieSchedule(Action):

    def name(self) -> Text:
        return "action_ask_movie_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):
        
        movie_name = tracker.get_slot("movie")

        if not movie_name:
            dispatcher.utter_message(text="Chúng tôi chưa xác định được tên phim bạn muốn xem, vui lòng nhập tên phim.")
            return [SlotSet("movie", None)]  # Đảm bảo slot vẫn rỗng để bot hỏi lại
        
        # Set slot nếu có giá trị movie
        # Gọi BE để lấy lịch chiếu phim
        # giả sử lịch chiếu phim là 10h sáng
        schedule = "10h sáng"
        dispatcher.utter_message(text=f"Phim {movie_name} sẽ được chiếu vào lúc {schedule}. Bạn muốn xem phim {movie_name} vào lúc mấy giờ nhỉ?")
        return [SlotSet("movie", movie_name)]

class ActionAskSelectedMovieSchedule(Action):

    def name(self) -> Text:
        return "action_ask_selected_movie_schedule"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        movie_selected = tracker.get_slot("movie_selected")
        if movie_selected is None:
            dispatcher.utter_message(
                text="Bạn chưa chọn bộ phim nào. Vui lòng chọn một bộ phim trước."
            )
        schedule = "11h sáng"
        dispatcher.utter_message(text=f"Phim {movie_selected} sẽ được chiếu vào lúc {schedule}. Bạn muốn xem phim {movie_selected} vào lúc mấy giờ nhỉ?")
        return [SlotSet("movie_selected", movie_selected)]
    
class ActionAskMovieMultipleInfo(Action):

    def name(self) -> Text:
        return "action_ask_movie_multiple_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):

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
    
class ActionSuggestMovieMultipleInfo(Action):

    def name(self) -> Text:
        return "action_suggest_movie_multiple_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain):
        
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
