from transformers import TokenClassificationPipeline, AutoModelForTokenClassification, AutoTokenizer
from transformers.pipelines import AggregationStrategy
import torch


class KeyphraseExtractionPipeline(TokenClassificationPipeline):
    def __init__(self, model_name):
        model = AutoModelForTokenClassification.from_pretrained(model_name)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(device)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        super().__init__(
            model=model,
            tokenizer=tokenizer
        )

    def postprocess(self, all_outputs):
        results = super().postprocess(
            all_outputs=all_outputs,
            aggregation_strategy=AggregationStrategy.SIMPLE,
        )
        return list(set([result.get("word").strip() for result in results]))
