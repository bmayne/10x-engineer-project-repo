# API Reference Documentation

This API Reference provides a comprehensive guide to the available endpoints, including request/response examples, error formats, and authentication details.

## Endpoints Overview

### 1. Prompts

#### POST /prompts
- **Description**: Create a new prompt.
- **Request Body**:
  - `id` (string): The unique identifier for the prompt.
  - `text` (string): The text of the prompt.
  - `collection_id` (string): The ID of the collection to which the prompt belongs.
- **Response**:
  - **200 OK**: Returns the created prompt object.
  - **Example**:
    ```json
    {
        "id": "1",
        "text": "Sample Prompt",
        "collection_id": "1"
    }
    ```
- **Errors**:
  - **400 Bad Request**: Invalid input data.
  - **409 Conflict**: Prompt ID already exists.

#### GET /prompts/{id}
- **Description**: Retrieve a prompt by its ID.
- **Response**:
  - **200 OK**: Returns the prompt object.
  - **Example**:
    ```json
    {
        "id": "1",
        "text": "Sample Prompt",
        "collection_id": "1"
    }
    ```
- **Errors**:
  - **404 Not Found**: Prompt not found.

#### PUT /prompts/{id}
- **Description**: Update an existing prompt by its ID.
- **Request Body**:
  - `text` (string): The updated text of the prompt.
  - `collection_id` (string): The updated collection ID.
- **Response**:
  - **200 OK**: Returns the updated prompt object.
- **Errors**:
  - **400 Bad Request**: Invalid input data.
  - **404 Not Found**: Prompt not found.

#### PATCH /prompts/{id}
- **Description**: Partially update an existing prompt by its ID.
- **Request Body**:
  - `text` (Optional[str]): The new text for the prompt.
  - `collection_id` (Optional[str]): The new collection ID for the prompt.
- **Response**:
  - **200 OK**: Returns the updated prompt object with changes applied.
  - **Example**:
    ```json
    {
        "id": "1",
        "text": "Updated Prompt Text"
    }
    ```
- **Errors**:
  - **400 Bad Request**: Invalid input data.
  - **404 Not Found**: Prompt not found.

#### DELETE /prompts/{id}
- **Description**: Delete a prompt by its ID.
- **Response**:
  - **204 No Content**
- **Errors**:
  - **404 Not Found**: Prompt not found.

### 2. Collections

#### POST /collections
- **Description**: Create a new collection.
- **Request Body**:
  - `id` (string): The unique identifier for the collection.
  - `name` (string): The name of the collection.
- **Response**:
  - **200 OK**: Returns the created collection object.
  - **Example**:
    ```json
    {
        "id": "1",
        "name": "Sample Collection"
    }
    ```
- **Errors**:
  - **400 Bad Request**: Invalid input data.
  - **409 Conflict**: Collection ID already exists.

#### GET /collections/{id}
- **Description**: Retrieve a collection by its ID.
- **Response**:
  - **200 OK**: Returns the collection object.
  - **Example**:
    ```json
    {
        "id": "1",
        "name": "Sample Collection"
    }
    ```
- **Errors**:
  - **404 Not Found**: Collection not found.

#### DELETE /collections/{id}
- **Description**: Delete a collection by its ID.
- **Response**:
  - **204 No Content**
- **Errors**:
  - **404 Not Found**: Collection not found.

## Error Response Format
- **Format**: All error responses will have the format:
  ```json
  {
      "error": "Error message"
  }
  ```

## Authentication
Currently, no authentication is required to access these endpoints.