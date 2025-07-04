# Game Information RAG Pipeline

This project is a Retrieval-Augmented Generation (RAG) pipeline for extracting, processing, and querying character information from game fandom wikis. It scrapes HTML pages, processes the content into markdown, stores embeddings in a FAISS vector database, and uses a language model to answer user queries.

## Project Structure

```
Fandom-query/
  crawler/
    crawler.py
    main.py
    rag.py
    scraper.py
  data/
    faiss/
    processed/
    raw/
    vectors/
  data_processing/
    embedder.py
  llm/
  .env
  README.md
```

## Main Components

- **crawler/scraper.py**: Extracts structured data from HTML files and saves as markdown.
- **crawler/main.py**: Streamlit app for user interaction. Handles the pipeline: crawling, scraping, vectorizing, and querying.
- **crawler/rag.py**: Loads markdown, creates/loads FAISS vector store, and runs the RAG pipeline using a language model.
- **data/**: Stores raw HTML, processed markdown, and vector databases.

## Setup

1. **Install dependencies**  
   Make sure you have Python 3.10+ and install required packages:
   ```sh
   pip install -r requirements.txt
   ```

2. **Environment Variables**  
   Create a `.env` file in `Fandom-query/` with your API keys and settings:
   ```
   LANGCHAIN_API_KEY=your_langchain_api_key
   LANGCHAIN_PROJECT=your_project_name
   ```

3. **Run the Streamlit App**  
   From the `Fandom-query/crawler/` directory:
   ```sh
   streamlit run main.py
   ```

## Usage

1. Enter the game name, character name, and your query in the Streamlit UI.
2. The pipeline will:
   - Crawl and scrape the relevant fandom wiki page.
   - Process and save the content as markdown.
   - Store embeddings in a FAISS vector database.
   - Use a language model to answer your query based on the character's information.

## Notes

- The project uses hardcoded data paths. Adjust `RAW_DATA_DIR`, `PROCESSED_DATA_DIR`, and `FAISS_INDEX_DIR` in the code if needed.
- Ensure you have the required API access for LangChain and Ollama models.

## License

MIT License

---

For more details, see the code in [crawler/main.py](crawler/main.py), [crawler/scraper.py](crawler/scraper.py), and