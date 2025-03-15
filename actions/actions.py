

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


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

        dispatcher.utter_message(text="Bạn có thể cho tôi biết thêm thông tin về phim bạn muốn xem được không như thể loại, diễn viên, đạo diễn, năm sản xuất, ...")

        return []
    
class ActionSuggestMovieGenre(Action):
    
    def name(self) -> Text:
        return "action_suggest_movie_genre"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Đây có thể là phim bạn yêu cầu")

        return []
