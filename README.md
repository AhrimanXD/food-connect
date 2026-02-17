# Food Connect

A web platform connecting restaurants with surplus food to NGOs and community organizations. Built with Flask, SQLAlchemy, and Ollama for AI-powered semantic search.

## Features

- **Food Donation Portal**: Restaurants can easily donate surplus food by filling out a simple form
- **Semantic Search**: AI-powered search using Ollama embeddings to find relevant food offers
- **AI Summaries**: Automatically generated summaries of matching offers using RAG
- **Claim System**: NGOs can claim available food offers
- **Expiration Management**: Automatic deactivation of expired offers

## Tech Stack

- **Backend**: Flask
- **Database**: SQLite with SQLAlchemy ORM
- **AI**: Ollama (mxbai-embed-large for embeddings, Llama-3.2-1B for text generation)
- **Frontend**: Jinja2 templates

## Prerequisites

- Python 3.13+
- [Ollama](https://ollama.com/) installed and running locally

## Installation

1. Clone the repository:
```bash
git clone <https://github.com/AhrimanXD/food-connect.git>
cd food-connect
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start Ollama and pull required models:
```bash
ollama serve
ollama pull mxbai-embed-large
ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

5. Run the application:
```bash
python app.py
```

6. Open your browser at `http://localhost:5000`

## Usage

- **Browse Offers**: Visit the home page to see all available food donations
- **Search**: Use the search bar to find specific food items using natural language
- **Donate Food**: Click "Donate" to add a new food offer
- **Claim Food**: Click "Claim" on an offer to claim it (restaurant will be contacted)

## Project Structure

```
food-connect/
├── app.py              # Main Flask application
├── models.py           # SQLAlchemy database models
├── ai.py               # AI embeddings and RAG functionality
├── utils.py            # Utility functions
├── config.py           # Configuration settings
├── seed_offers.py      # Script to seed sample data
├── templates/          # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── navbar.html
│   └── donation_form.html
└── requirements.txt    # Python dependencies
```

## License

MIT
