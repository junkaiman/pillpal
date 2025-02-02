from src.query import query
from src.gpt_summarize import gpt_summarize

if __name__ == "__main__":

    query_url = "https://www.drugs.com/imprints.php?imprint=93551&color=&shape=0" 
    json_dir = "./configs"

    print(f"Querying {query_url}...")
    query_json_path = query(query_url, json_dir)

    print(f"Summarizing {query_json_path}...")
    gpt_json_path = gpt_summarize(query_json_path, json_dir)

    print(f"Saved to path {gpt_json_path}.")
