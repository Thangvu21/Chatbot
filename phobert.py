from typing import Any, Dict, List, Text
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR], is_trainable=True
)
class PhoBERTEmbedder(GraphComponent):
    def __init__(self, config: Dict[Text, Any], model_storage: ModelStorage, resource: Resource):
        self.model_name = "vinai/phobert-base"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name).to(self.device)
        self.model.eval()

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config, model_storage, resource)

    def train(self, training_data: TrainingData) -> Resource:
        """Huấn luyện mô hình bằng cách tạo embedding cho dữ liệu huấn luyện và lưu model."""
        
        # Xử lý dữ liệu huấn luyện để trích xuất embedding
        training_data = self.process_training_data(training_data)
        
        # Lưu model vào `ModelStorage`
        with self.model_storage.write_to(self.resource) as model_dir:
            torch.save(self.model.state_dict(), model_dir / "phobert_model.pt")
        
        return self.resource


    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        for example in training_data.training_examples:
            example.set("text_features", self._get_sentence_embedding(example.get("text")))
        return training_data

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            message.set("text_features", self._get_sentence_embedding(message.get("text")))
        return messages

    def _get_sentence_embedding(self, text: Any):
        """Tạo embedding từ câu đầu vào, xử lý lỗi kiểu dữ liệu."""
        
        # Đảm bảo text là chuỗi, nếu không trả về vector 0
        if not isinstance(text, str):
            print(f"Warning: Expected string, but got {type(text)}. Returning zero vector.")
            return np.zeros(768)  # PhoBERT có 768 chiều

        # Tokenization với batch size 1
        tokens = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=256).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**tokens)
        
        # Lấy embedding trung bình
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
        
        return embeddings
