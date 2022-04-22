if __name__ == "__main__":
    from transformers import AutoModelForCausalLM
    import transformers
    from transformers import Trainer, TrainingArguments
    from transformers import AutoTokenizer
    from datasets import load_dataset
    import os 
    import torch

    device = 'gpu'
    if torch.cuda.is_available():
        device = 'cuda'
    

    datasets = load_dataset('csv', data_files={'train': ['data/train_cleaned.csv'],
                                                    'test': 'data/test_cleaned.csv'})

    model_checkpoint = "gpt2"
            

    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, use_fast=True)
    def tokenize_function(examples):
        return tokenizer(examples["text"])

    tokenized_datasets = datasets.map(tokenize_function, batched=True, remove_columns=["text"])
        # block_size = tokenizer.model_max_length
    block_size = 128

    def group_texts(examples):
        # Concatenate all texts.
        concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
        total_length = len(concatenated_examples[list(examples.keys())[0]])
            #print(concatenated_examples)
            # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
                # customize this part to your needs.
        total_length = (total_length // block_size) * block_size
            # Split by chunks of max_len.
        result = {
            k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
            for k, t in concatenated_examples.items()
        }
        result["labels"] = result["input_ids"].copy()
        return result

    # Tokenize the dataset
    lm_datasets = tokenized_datasets.map(
        group_texts,
        batched=True,
        batch_size=1000,
        
    )
    # Load in pre-trained gp2 weights
    model = AutoModelForCausalLM.from_pretrained(model_checkpoint)
    
    model_name = model_checkpoint.split("/")[-1]
    training_args = TrainingArguments(
        f"{model_name}-finetuned-jokegen",
        evaluation_strategy = "epoch",
        learning_rate=2e-5,
        weight_decay=0.01,
        push_to_hub=False,
    save_strategy='epoch'
    )

    trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=lm_datasets["train"],
    eval_dataset=lm_datasets["test"],
    )

    trainer.train()

    trainer.save_model('testing')





