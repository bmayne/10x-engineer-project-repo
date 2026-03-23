# PromptLab

**Your AI Prompt Engineering Platform**

---

## Project Overview

PromptLab is a robust AI Prompt Engineering Platform designed to facilitate the management and organization of AI prompts. It allows teams to streamline their workflow by enabling them to store, edit, and test AI prompt templates. With integrated features like prompt organization, tagging, and version control, PromptLab aims to enhance productivity and efficiency in AI development.

## Features

- **Prompt Organization**: Tagging, categorization, and easy search functionality.
- **Version Control**: Track changes and maintain prompt versions.
- **Collaboration Tools**: Shared spaces and collaborative editing.
- **Integration Ready**: Seamlessly connect with other AI tools and platforms.

---

## Prerequisites and Installation

### Prerequisites
- **Python** 3.10 or higher
- **Node.js** 18 or higher (required from Week 4 for the frontend development)
- **Git**

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd promptlab
   ```

2. **Set up and run the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
3. **Set up and run the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
The frontend application will be served, typically at [http://localhost:5173](http://localhost:5173).
The API will be accessible at: [http://localhost:8000](http://localhost:8000).

API Documentation can be viewed at: [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Quick Start Guide

```bash
# Clone the repository
git clone <your-repo-url>
cd promptlab

# Set up and run the backend
cd backend
pip install -r requirements.txt
python main.py
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for detailed API usage.

---

## API Endpoint Summary

| Method | Endpoint                  | Description                                      |
|--------|---------------------------|--------------------------------------------------|
| GET    | `/health`                 | Check API health status                          |
| GET    | `/prompts`                | Retrieve a list of all prompts (filterable)      |
| GET    | `/prompts/{prompt_id}`    | Retrieve a specific prompt by its ID             |
| POST   | `/prompts`                | Create a new prompt                              |
| PUT    | `/prompts/{prompt_id}`    | Update an existing prompt                        |
| PATCH  | `/prompts/{prompt_id}`    | Partially update a prompt                        |
| DELETE | `/prompts/{prompt_id}`    | Delete a prompt                                  |
| GET    | `/collections`            | Retrieve all collections                         |
| GET    | `/collections/{collection_id}` | Get a specific collection by ID              |
| POST   | `/collections`            | Create a new collection                          |
| DELETE | `/collections/{collection_id}` | Delete a collection                              |

### Usage Examples

#### Creating a new Prompt

```bash
# POST request to create a new prompt
curl -X POST http://localhost:8000/prompts \
-H "Content-Type: application/json" \
-d '{"title": "New Prompt", "content": "Sample content here..."}'
```

#### Listing collection prompts

```bash
# GET request to list prompts
curl -X GET 'http://localhost:8000/prompts?collection_id=exampleCollectionId'
```

#### Updating a Prompt

```bash
# PUT request to update a prompt
curl -X PUT http://localhost:8000/prompts/<prompt_id> \
-H "Content-Type: application/json" \
-d '{"title": "Updated Title", "content": "Updated content...", "collection_id": "exampleCollectionId"}'
```

---

## Development Setup

To set up the development environment, ensure all prerequisites are installed, and follow the installation steps.
Use the following command to run tests and ensure the environment is correctly configured:

```bash
cd backend
pytest tests/ -v
```

## Contributing Guidelines

We welcome contributions to improve PromptLab. Please follow these guidelines:

1. **Fork the repository** and create a new branch for your feature or fix.
2. **Ensure code quality** and test your changes thoroughly.
3. **Submit a pull request** with a detailed description of the changes.

For more details, refer to the `CONTRIBUTING.md` file in the repo.

These guidelines ensure a smooth collaboration process and help maintain the code quality.