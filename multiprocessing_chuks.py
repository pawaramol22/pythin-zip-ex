import multiprocessing
import regex

def find_keywords_in_chunk(chunk, keywords):
    matches = []
    for keyword in keywords:
        keyword_matches = regex.finditer(keyword, chunk)
        matches.extend((keyword, match.group()) for match in keyword_matches)
    return matches

def process_text_chunk(text_chunk, keywords):
    return find_keywords_in_chunk(text_chunk, keywords)

def break_text_into_chunks(text, chunk_size):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def main(text, chunk_size, keywords):
    chunks = break_text_into_chunks(text, chunk_size)
    pool = multiprocessing.Pool()

    results = pool.starmap(process_text_chunk, [(chunk, keywords) for chunk in chunks])

    # Flatten the list of matches
    all_matches = [match for sublist in results for match in sublist]

    # Process or print the matches as needed
    for keyword, match in all_matches:
        print(f"Keyword '{keyword}' found: {match}")

if __name__ == "__main__":
    large_text = 'Your large text string goes here...'
    chunk_size = 100 * 1024  # 100 KB
    search_keywords = ['pattern1', 'pattern2', 'pattern3']

    main(large_text, chunk_size, search_keywords)
