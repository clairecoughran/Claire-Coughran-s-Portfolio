# Project 4: Retrieval-Augmented Generation (RAG) System

## Authors

Claire Coughran

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system that allows users to ask questions about paddleboard and kayak rules, regulations, and general advice in Colordao. The system retrieves relevant document chunks using vector similarity search and uses a large language model to generate answers based on the retrieved context.

## Features

* Document ingestion from PDF and web sources
* Text chunking with overlap
* Vector embeddings stored in ChromaDB
* Semantic similarity search
* OpenAI-powered answer generation
* Gradio web interface
* Interactive Plotly visualization of document embeddings

## Requirements

Install dependencies:

* Claire_Coughran_Project4.ipynb
```bash
pip install -r requirements.txt
```
* Document_Preperation.ipynb
```bash
pip install -r text_parse_requirements.txt
```

## Project Structure

```text
Project 4/
├── Claire_Coughran_Project4.ipynb
├── Document_Preperation.ipynb
├── text_parse_requirements.txt
├── README.md
├── Cleaned Txt Files/
│   ├── Colorado_Boating_Handbook.txt
│   ├── Colorado_Kayaking_Laws.txt
│   ├── Colorado_Paddleboard_Laws.txt
│   ├── Safety_Checklist.txt
│   ├── Colorado_Paddleboard_Guide.txt
│   └── Best_Paddleboarding_Colorado.txt
└── PDF Source Files/
    ├── Kayak_Paddle_Board_Checklist.pdf
    └── Colorado_Boating_Handbook.pdf
```

## Usage

1. Enter a question in the Gradio interface.
2. The system retrieves the most relevant document chunks.
3. The LLM generates an answer using the retrieved context.
4. Relevant source chunks are displayed alongside the answer.


## Example Questions

* What type of life jacket do I need for paddleboarding in [calm/choppy/rough] water?
* what should I check before I go kayaking on the river?
* Where is the best place to go if I want a [private/exciting/beautiful] paddle?


## External Libraries

* OpenAI
* ChromaDB
* Gradio
* PyPDF
* PyMuPDF
* BeautifulSoup4
* Requests
* Selenium
* Plotly

## Acknowledgments

Developed for Project 4 COMP4451 coursework at University of Denver.
