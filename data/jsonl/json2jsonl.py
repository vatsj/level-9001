"""
from Claude
thanks Claude
"""

import json
import re

def process_completion(completion):
    # Escape newlines and quotes
    completion = completion.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    return completion

def convert_to_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        content = infile.read()
        # Split the content into individual JSON objects
        json_objects = re.findall(r'\{.*?\}', content, re.DOTALL)
        
        for obj in json_objects:
            try:
                # Parse the JSON object
                data = json.loads(obj)
                # Process the completion field
                data['completion'] = process_completion(data['completion'])
                # Write the processed object as a single line
                json.dump(data, outfile, ensure_ascii=False)
                outfile.write('\n')
            except json.JSONDecodeError as e:
                print(f"Error processing object: {e}")
                print(f"Problematic object: {obj}")

# Usage
input_file = 'manual.jsonl'  # Replace with your input file name
output_file = 'manual-formatted.jsonl'  # Replace with your desired output file name

convert_to_jsonl(input_file, output_file)
print(f"Conversion complete. Output written to {output_file}")