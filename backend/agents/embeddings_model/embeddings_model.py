# Author: Vodohleb04
from typing import Dict, List
import torch
from transformers import BertTokenizerFast, BertModel
from jsonschema import validate, ValidationError
from aiologger.loggers.json import JsonLogger
import backend.agents.embeddings_model.embeddings_model_validation as json_validation
from backend.agents.embeddings_model.pure_embeddings_model import PureEmbeddingsModel


logger = JsonLogger.with_default_handlers(
    level="DEBUG",
    serializer_kwargs={'ensure_ascii': False},
)


class EmbeddingsModel(PureEmbeddingsModel):
    snippet_window_size: int = 30
    snippet_intersection_with_prev_window: int = 10

    recommendation_window_size: int = 512
    recommendation_intersection_with_prev_window: int = 256


    def __init__(self, model: BertModel, tokenizer: BertTokenizerFast, dtype: torch.dtype, device: torch.device):
        """
        :param model: transformers.BertModel - embeddings model based on BERT architecture.
        :param tokenizer: transformers.BertTokenizerFast - tokenizer of the given model
        :param dtype: torch.dtype - dtype, used in model
        :param device: torch.device - device, where model is located
        """
        if model.device.type != device.type:
            raise ValueError(f"Expected model to be located on the same device, as the given parameter, but got {model.device.type} and {device.type}")
        self._model = model
        self._tokenizer = tokenizer
        self._dtype = dtype
        self._device = device


    @staticmethod
    def _get_snippets(text, offset_mapping):
        snippets_list = []
        for i in range(offset_mapping.shape[0]):
            # offset_mapping[i][j] is array of len(2)
            # offset_mapping[i][0] is always [0, 0] and maps to [CLS] special token
            first_char_idx = offset_mapping[i][1][0]
            # offset_mapping[i][j] is always [0, 0] and maps to [SEP] special token if j = (offset_mapping.shape[1] - 1)
            j = offset_mapping.shape[1] - 2
            while offset_mapping[i][j][1] == 0 and j > 0:  # j == 0 is maps to [CLS] special token
                j -= 1  # offset_mapping[i][j] = [0, 0] maps to [PAD], but the part of the text is needed
            after_last_char_idx = offset_mapping[i][j][1]
            # offset_mapping[i][j][1] is the index of the element after the last element of the window
            # for the last window offset_mapping[i][j][1] == len(original_text)

            snippets_list.append(
                text[first_char_idx: after_last_char_idx]
            )
        return snippets_list


    @staticmethod
    def _get_snippet_bound(offset_mapping_of_snippet):
        # offset_mapping_of_snippet[j] is array of len(2)
        # offset_mapping_of_snippet[0] is always [0, 0] and maps to [CLS] special token
        first_char_idx = offset_mapping_of_snippet[1][0]
        # offset_mapping_of_snippet[j] is always [0, 0] and maps to [SEP] special token if j = (offset_mapping_of_snippet.shape[0] - 1)
        j = offset_mapping_of_snippet.shape[0] - 2
        while offset_mapping_of_snippet[j][1] == 0 and j > 0:  # j == 0 is maps to [CLS] special token
            j -= 1  # offset_mapping_of_snippet[j] = [0, 0] maps to [PAD], but the part of the text is needed
        after_last_char_idx = offset_mapping_of_snippet[j][1]
        # offset_mapping_of_snippet[j][1] is the index of the element after the last element of the window
        # for the last window offset_mapping_of_snippet[j][1] == len(original_text)

        return first_char_idx, after_last_char_idx


    def _tokenize_text(self, text, window_size, intersection_with_prev_window, return_offset_mapping):
        tokenized_text = self._tokenizer(
            text,
            padding="max_length", truncation=True, max_length=window_size, stride=intersection_with_prev_window,
            return_tensors='pt', return_overflowing_tokens=True, return_offsets_mapping=return_offset_mapping
        )
        input_ids = tokenized_text["input_ids"]
        token_type_ids = tokenized_text["token_type_ids"]
        attention_mask = tokenized_text["attention_mask"]
        if return_offset_mapping:
            return input_ids, token_type_ids, attention_mask, tokenized_text["offset_mapping"]
        else:
            return input_ids, token_type_ids, attention_mask


    def _make_snippet_embedding(self, json_params: Dict):
        with torch.no_grad():
            input_ids, token_type_ids, attention_mask, offset_mapping = self._tokenize_text(
                json_params["text"], json_params["window_size"], json_params["intersection_with_prev_window"],
                return_offset_mapping=True
            )
            input_ids = input_ids.to(self._device)
            token_type_ids = token_type_ids.to(self._device)
            attention_mask = attention_mask.to(self._device)

            embedding = self._model(input_ids, token_type_ids, attention_mask)
            embedding = embedding.last_hidden_state.mean(dim=-2)  # mean embeddings for every token (doesn't mix snippets)
            embedding = embedding.cpu()

            result = []
            for i in range(embedding.shape[0]):
                first_idx, after_last_idx = self._get_snippet_bound(offset_mapping[i])
                result.append(
                    {"embedding": embedding[i].tolist(), "snippet_text": json_params["text"][first_idx : after_last_idx]}
                )
            return result


    async def make_snippet_embedding(self, json_params: Dict):
        try:
            validate(json_params, json_validation.make_snippet_embedding)
        except ValidationError as ex:
            await logger.error(f"make_snippet_embedding, ValidationError({ex.args[0]})")
            return []  # raise ValidationError

        if not json_params.get("window_size", False):
            json_params["window_size"] = self.snippet_window_size

        if not json_params.get("intersection_with_prev_window", False):
            json_params["intersection_with_prev_window"] = self.snippet_intersection_with_prev_window

        return self._make_snippet_embedding(json_params)


    def _make_recommendation_embedding(self, json_params: Dict):
        with torch.no_grad():
            input_ids, token_type_ids, attention_mask = self._tokenize_text(
                json_params["text"], json_params["window_size"], json_params["intersection_with_prev_window"],
                return_offset_mapping=False
            )
            input_ids = input_ids.to(self._device)
            token_type_ids = token_type_ids.to(self._device)
            attention_mask = attention_mask.to(self._device)

            embedding = self._model(input_ids, token_type_ids, attention_mask)
            embedding = embedding.last_hidden_state.mean(dim=-2)  # mean embeddings for every token (doesn't mix snippets)
            embedding = embedding.mean(dim=-2)  # mean window embedding of text (window1 + window2 + ... + window-n)/window_amount

            return {"embedding": embedding.cpu().squeeze().tolist()}


    async def make_recommendation_embedding(self, json_params: Dict):
        try:
            validate(json_params, json_validation.make_recommendation_embedding)
        except ValidationError as ex:
            await logger.error(f"make_recommendation_embedding, ValidationError({ex.args[0]})")
            return {}  # raise ValidationError

        if not json_params.get("window_size", False):
            json_params["window_size"] = self.recommendation_window_size

        if not json_params.get("intersection_with_prev_window", False):
            json_params["intersection_with_prev_window"] = self.recommendation_intersection_with_prev_window

        return self._make_recommendation_embedding(json_params)




if __name__ == "__main__":
    import asyncio
    async def main():
        with open("/home/yackub/PycharmProjects/Guide/backend/agents/embeddings_model/articles/84we1w8qq2c2dg.md", 'r') as f:
            txt1 = f.read().lower()
        with open("/home/yackub/PycharmProjects/Guide/backend/agents/embeddings_model/articles/ibfwev78vg7xbc09.md", 'r') as f:
            txt2 = f.read().lower()
        with open("/home/yackub/PycharmProjects/Guide/backend/agents/embeddings_model/articles/ec2642c8et.md",'r') as f:
            txt3 = f.read().lower()


        tokenizer = BertTokenizerFast.from_pretrained("DeepPavlov/rubert-base-cased")
        model = BertModel.from_pretrained("DeepPavlov/rubert-base-cased")

        device = torch.device("cpu")
        dtype = torch.float32

        emb_model = EmbeddingsModel(model, tokenizer, dtype, device)
        print("###1###")
        emb1 = (await emb_model.make_recommendation_embedding(
            {"text": txt1, "window_size": 512, "intersection_with_prev_window": 256}
        ))["embedding"]
        print("###2###")
        emb2 = (await emb_model.make_recommendation_embedding(
            {"text": txt2, "window_size": 512, "intersection_with_prev_window": 256}
        ))["embedding"]
        print("###3###")
        emb3 = (await emb_model.make_recommendation_embedding(
            {"text": txt3, "window_size": 512, "intersection_with_prev_window": 256}
        ))["embedding"]



        def cosine_dist(emb1, emb2):
            len1 = torch.sqrt(torch.sum(torch.square(emb1)))
            len2 = torch.sqrt(torch.sum(torch.square(emb2)))
            return 1 - (emb1 @ emb2) / (len1 * len2)

        emb1 = torch.as_tensor(emb1)
        emb2 = torch.as_tensor(emb2)
        emb3 = torch.as_tensor(emb3)

        print("###1@2###")
        print(cosine_dist(emb1, emb2))
        print("###1@3###")
        print(cosine_dist(emb1, emb3))
        print("###2@3###")
        print(cosine_dist(emb2, emb3))


        snippets = await emb_model.make_snippet_embedding(
            {"text": txt1, "window_size": 30, "intersection_with_prev_window": 10}
        )

        print(len(snippets))
        print(len(snippets[0]["embedding"]))


    asyncio.run(main())


