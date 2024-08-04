import json

def transform_jsonl_to_json(input_file, output_file):
    completions = []
    
    # Read the input file and extract completions
    with open(input_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                choices = data['response']['body']['choices']
                for choice in choices:
                    content = choice['message']['content']
                    try:
                        # Try to parse content as JSON
                        completion = json.loads(content)
                    except json.JSONDecodeError:
                        # If parsing fails, use the content as is
                        completion = content
                    completions.append(completion)
            except KeyError as e:
                print(f"KeyError: {e}. Skipping this line.")
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}. Skipping this line.")
    
    # Write the completions to the output file with each JSON on a new line
    with open(output_file, 'w') as f:
        f.write('{\n"jsons": [\n')
        for i, completion in enumerate(completions):
            json.dump(completion, f)
            if i < len(completions) - 1:
                f.write(',\n')
            else:
                f.write('\n')
        f.write(']\n}')

# Usage
input_file = 'data/openai_batch_output.jsonl'
output_file = 'data/processed_batch_output.jsonl'
transform_jsonl_to_json(input_file, output_file)