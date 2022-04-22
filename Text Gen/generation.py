import os
import sys
import argparse
import pandas as pd
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer




parser = argparse.ArgumentParser(description='Generation Of Jokes')


parser.add_argument('--start', default="What do you call a molecule of sodium carrying a gun?",
                    help="Start of the joke, it is recommended that you use a question aswer format")

parser.add_argument('--max_length',default=100,
                    help='The maximum amount of characters allowed in the generated text')

parser.add_argument('--temperature',default=1.0,
                    help='Temperature makes the distribution P(w|w_{1:t-1})  sharper meaning that high likelihood words are more likely and low likelihood words are less likely')

parser.add_argument('--top_p',default=0.95,
                    help='top_p sampling chooses from the smallest possible set of words whose cumulative probability exceeds the probability p')

parser.add_argument('--top_k',default=50,
                    help='In each sampling step we limit our sampling pool to top_k words')


parser.add_argument('--repetition_penalty',default=1.0,
                    help='Used to penalize words that have already been used')

parser.add_argument('--do_sample',default=True,
                    help='Pick the next word dependent on the conditional probaiblity distribution')

parser.add_argument('--num_return_sequences',default=3,
                    help='The number of generated sequences you want to return for a given hook')
        
args = parser.parse_args()




model = AutoModelForCausalLM.from_pretrained('testing')
tokenizer = AutoTokenizer.from_pretrained('gpt2')



encoded_prompt = tokenizer(args.start, add_special_tokens=True, return_tensors="pt").input_ids
input_ids = encoded_prompt

output_sequences = model.generate(
        input_ids=input_ids,
        max_length=args.max_length,
        temperature=args.temperature,
        top_k=args.top_k,
        top_p=args.top_p,
        repetition_penalty=args.repetition_penalty,
        do_sample=args.do_sample,
        num_return_sequences=args.num_return_sequences
    )



if len(output_sequences.shape) > 2:
    output_sequences.squeeze_()

generated_sequences = []
stop_token='<eop>'
for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
    print(f"=== GENERATED SEQUENCE {generated_sequence_idx + 1} ===")
    generated_sequence = generated_sequence.tolist()

        # Decode text
    text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

        # Remove all text after the stop token
    text = text[: text.find(stop_token) if stop_token else None]

        # Add the prompt at the beginning of the sequence. Remove the excess text that was used for pre-processing
    total_sequence = (
        text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True)) :]
    )

    generated_sequences.append(total_sequence)


path='GeneratedJokes'
if not os.path.exists(path):
    os.makedirs(path)
else:
    pass

JokesToFrame={'Hook':args.start,'Joke':generated_sequences}
JokesToFrame=pd.DataFrame(JokesToFrame)
JokesToFrame.to_csv('GeneratedJokes/Jokes.csv')
