from dotenv import load_dotenv
import google.generativeai as genai
import os
import pandas as pd
import random

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Load Data
train = pd.read_csv('./open/train.csv', encoding='utf-8-sig')
test = pd.read_csv('./open/test.csv', encoding='utf-8-sig')

# Prepare Examples for Prompt
samples = []
sample_size = min(50, len(train))  # Use up to 50 examples for better training
for i in range(sample_size):
    sample = f"input: {train['input'][i]}\noutput: {train['output'][i]}"
    samples.append(sample)
example_prompt = "\n\n".join(samples)

# System Prompt
system_prompt = (
    "You are a helpful assistant specializing in restoring obfuscated Korean reviews. "
    "Your task is to transform the given obfuscated Korean review into a clear, correct, "
    "and natural-sounding Korean review that reflects its original meaning. "
    "Below are examples of obfuscated Korean reviews and their restored forms:\n\n"
    f"Example, {samples}"  
    "Spacing and word length in the output must be restored to the same as in the input. "
    "Do not provide any description. Print only in Korean."
)

# Process Random Samples
random_indices = random.sample(range(len(train)), 5)  # Use random but fixed indices for reproducibility

for j, idx in enumerate(random_indices, start=1):
    query = train['input'][idx]
    expected_output = train['output'][idx]

    try:
        # Generate Content
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(f"{system_prompt}\n\ninput: {query}\noutput:")
        result = response.text.strip()

        # Print Results
        print(f"{j}번째 샘플")
        print(f"원본: {query}")
        print(f"복원 결과: {result}")
        print(f"정답: {expected_output}")
        print("정확도:", "일치" if result == expected_output else "불일치")
        print("-" * 50)

    except Exception as e:
        print(f"Error processing sample {j}: {e}")
