# -*- coding: utf-8 -*-
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, PeftModel
from transformers import Trainer, TrainingArguments
import torch

# Carga dataset
dataset = load_dataset("csv", data_files="dataset_b2.csv", delimiter="|")
print(dataset)

# Modelo y tokenizer
model_name = "google/gemma-2-9b-it"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", dtype=torch.float16)

# Aplicar LoRA (si ya lo hiciste, conserva)
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj","v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# Preprocess correcto: prompt separado de la respuesta y labels en -100 para prompt
def preprocess(example):
    instruction = example.get("instruction", "") or ""
    input_text = example.get("input", "") or ""
    output_text = example.get("output", "") or ""

    prompt = (
        "### Instrucción:\n"
        f"{instruction}\n\n"
        "### Entrada:\n"
        f"{input_text}\n\n"
        "### Respuesta:\n"
    )

    # Tokenizar prompt y output por separado
    prompt_ids = tokenizer(prompt, truncation=True, max_length=256, add_special_tokens=False)["input_ids"]
    output_ids = tokenizer(output_text, truncation=True, max_length=256, add_special_tokens=False)["input_ids"]

    input_ids = prompt_ids + output_ids
    attention_mask = [1] * len(input_ids)
    labels = [-100] * len(prompt_ids) + output_ids

    return {"input_ids": input_ids, "attention_mask": attention_mask, "labels": labels}

# Mapear dataset (no batched para evitar problemas con la tokenización personalizada)
tokenized = dataset.map(preprocess, batched=False)
tokenized = tokenized["train"].train_test_split(test_size=0.2)

# Collate dinámico que usa tokenizer.pad y deja labels con -100
def collate_fn(features):
    # features: lista de dicts con input_ids, attention_mask, labels (listas de distinto length)
    batch = tokenizer.pad(
        features,
        padding=True,
        return_tensors="pt"
    )
    # Construir labels padded con -100
    labels = [f["labels"] for f in features]
    max_len = batch["input_ids"].shape[1]
    padded_labels = torch.full((len(labels), max_len), -100, dtype=torch.long)
    for i, lab in enumerate(labels):
        lab_t = torch.tensor(lab, dtype=torch.long)
        padded_labels[i, : lab_t.shape[0]] = lab_t
    batch["labels"] = padded_labels
    return batch

# Training args (ajusta a tu GPU/memoria)
training_args = TrainingArguments(
    output_dir="./lora_model",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=8,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_steps=200,
    save_total_limit=2,
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"],
    data_collator=collate_fn
)

trainer.train()

# Guardar adaptadores LoRA y tokenizer
model.save_pretrained("./lora_model")
tokenizer.save_pretrained("./lora_model")
