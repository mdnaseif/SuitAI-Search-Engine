import json
import os
from PIL import Image
from transformers import LlamaForCausalLM, LlamaTokenizer, Trainer, TrainingArguments
from datasets import Dataset, DatasetDict
from peft import LoraConfig, get_peft_model
import torch
from tqdm import tqdm
import deepspeed

# Define paths to data folder, JSON file containing Q&A pairs, and images folder
data_folder = '/media/akoubaa/new_ssd/naseif/Desktop/capstone/data'
json_file = os.path.join(data_folder, 'data.json')
images_folder = os.path.join(data_folder, 'images')

# Load JSON data
with open(json_file, 'r') as f:
    data = json.load(f)

# Preprocess data
def preprocess_data(data):
    inputs = []
    labels = []
    for item in tqdm(data, desc="Processing items"):
        conversations = item['conversations']
        for conv in conversations:
            if conv['from'] == 'human':
                inputs.append(conv['value'])
            elif conv['from'] == 'gpt':
                labels.append(conv['value'])
    return inputs, labels

inputs, labels = preprocess_data(data)

# Load the tokenizer
tokenizer = LlamaTokenizer.from_pretrained('llava-hf/llava-1.5-13b-hf')

# Tokenize data
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=512)

# Create dataset
dataset = Dataset.from_dict({"text": inputs, "labels": labels})

# Adding tqdm progress bar to the map function for tokenization
tokenized_dataset = dataset.map(tokenize_function, batched=True, desc="Tokenizing dataset", batch_size=16)

# Split dataset into training and validation sets
split_dataset = tokenized_dataset.train_test_split(test_size=0.1)

# Configuration for LoRA using PEFT
lora_config = LoraConfig(
    r=4,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

# Load model
model = LlamaForCausalLM.from_pretrained('llava-hf/llava-1.5-13b-hf')

# Apply LoRA using PEFT
model = get_peft_model(model, lora_config)

# Define training arguments with DeepSpeed configuration
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    push_to_hub=False,
    save_total_limit=2,
    deepspeed="ds_config.json"  # Path to DeepSpeed config file
)

# Initialize Trainer with DeepSpeed
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=split_dataset['train'],
    eval_dataset=split_dataset['test'],
)

# Train the model
trainer.train()

# Save the fine-tuned model and tokenizer
model.save_pretrained("./finetuned_model")
tokenizer.save_pretrained("./finetuned_model")
