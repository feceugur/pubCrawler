from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline


# https://huggingface.co/davanstrien/deberta-v3-base_fine_tuned_food_ner
tokenizer = AutoTokenizer.from_pretrained('davanstrien/deberta-v3-base_fine_tuned_food_ner')
model = AutoModelForTokenClassification.from_pretrained('davanstrien/deberta-v3-base_fine_tuned_food_ner')


text = "I wanna eat hamburger"

inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

ner = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")
#print(ner(text))
print(ner(text)[0]['word'])