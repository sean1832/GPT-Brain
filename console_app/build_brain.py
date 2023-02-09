import openai
import textwrap
import utilities


openai.api_key = utilities.open_file(r'.user\API-KEYS.txt').strip()

def main():
    all_text = utilities.open_file(r'.user\input.txt')

    # split text into smaller chunk of 4000 char each
    chunks = textwrap.wrap(all_text, 4000)

    result = []

    for chunk in chunks:
        embedding = utilities.embedding(chunk.encode(encoding='ASCII', errors='ignore').decode())
        info = {'content':chunk, 'vector':embedding}
        print(info, '\n\n\n')
        result.append(info)

    utilities.write_json_file(result, r'.user\brain-data.json')

if __name__ == '__main__':
    main()
