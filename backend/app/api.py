"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch, PromptVersion,
    PromptVersionList, Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Checks the health of the API service.

    Returns:
        HealthResponse: An object indicating the health status and version of the service.

    Example Usage:
        curl -X GET http://localhost:8000/health
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = Query("created_at"),
    sort_order: Optional[str] = Query("desc")
):
    """Lists all prompts, with optional filtering, searching, and sorting.

    Args:
        collection_id (Optional[str]): ID of the collection to filter by.
        search (Optional[str]): Search query to filter prompts.
        sort_by (Optional[str]): Field by which to sort the prompts.
        sort_order (Optional[str]): Order of sorting (asc or desc).

    Returns:
        PromptList: A list of prompts and total count.

     Example Usage:
        # List prompts sorted by title in ascending order
        curl -X GET "http://localhost:8000/prompts?sort_by=title&sort_order=asc"
        
        # List prompts in a specific collection with a search term, sorted by creation date
        curl -X GET "http://localhost:8000/prompts?collection_id=123&search=example&sort_by=created_at&sort_order=desc"
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Validate sort_by and sort_order
    if sort_by not in ["title", "created_at"]:
        raise HTTPException(status_code=400, detail="Invalid sorting field")
    
    if sort_order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort order")

    # Sort the prompts based on the sort_by field and order
    reverse = sort_order == "desc"
    prompts.sort(key=lambda x: getattr(x, sort_by), reverse=reverse)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Gets a specific prompt by prompt ID.

    Args:
        prompt_id (str): The ID of the prompt to retrieve.

    Returns:
        Prompt: The requested prompt object.

    Example Usage:
        curl -X GET http://localhost:8000/prompts/123
    """
    # This will now properly return a 404 if the prompt doesn't exist
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt
    

@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Creates a new prompt.

    Args:
        prompt_data (PromptCreate): The data for the new prompt.

    Returns:
        Prompt: The created prompt object.

    Example Usage:
        curl -X POST http://localhost:8000/prompts -d '{"title": "New Prompt"}'
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Updates a specific prompt with new data.

    Args:
        prompt_id (str): The ID of the prompt to update.
        prompt_data (PromptUpdate): The new data for the prompt.

    Returns:
        Prompt: The updated prompt object.

    Example Usage:
        curl -X PUT http://localhost:8000/prompts/123 -d '{"title": "Updated Title"}'
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    """Patches a specific prompt with partial updates.

    Args:
        prompt_id (str): The ID of the prompt to patch.
        prompt_data (PromptPatch): The fields to update in the prompt.

    Returns:
        Prompt: The patched prompt object.

    Example Usage:
        curl -X PATCH http://localhost:8000/prompts/123 -d '{"content": "Updated Content"}'
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Update only provided fields
    update_data = existing.model_dump()
    updated_fields = prompt_data.model_dump(exclude_unset=True)
    update_data.update(updated_fields)

    update_data['updated_at'] = get_current_time()
    updated_prompt = Prompt(**update_data)

    storage.update_prompt(prompt_id, updated_prompt)
    return updated_prompt


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Deletes a specific prompt.

    Args:
        prompt_id (str): The ID of the prompt to delete.

    Returns:
        None

    Example Usage:
        curl -X DELETE http://localhost:8000/prompts/123
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


@app.post("/prompts/{prompt_id}/versions", response_model=PromptVersion, status_code=201)
def create_prompt_version(prompt_id: str, version_data: PromptVersion):
    """Create a new version for a specific prompt."""
    version = PromptVersion(**version_data.model_dump())
    version.prompt_id = prompt_id
    return storage.create_prompt_version(version)


@app.get("/prompts/versions/{version_id}", response_model=PromptVersion)
def get_prompt_version(version_id: str):
    """Retrieve a specific prompt version by its ID."""
    version = storage.get_prompt_version(version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    return version


@app.get("/prompts/{prompt_id}/versions", response_model=PromptVersionList)
def list_versions_for_prompt(prompt_id: str):
    """List all versions associated with a specific prompt ID."""
    versions = storage.list_versions_for_prompt(prompt_id)
    return PromptVersionList(versions=versions, total=len(versions))


@app.put("/prompts/versions/{version_id}", response_model=PromptVersion)
def update_prompt_version(version_id: str, version_data: PromptVersion):
    """Update an existing prompt version identified by version ID."""
    updated_version = storage.update_prompt_version(version_id, version_data.model_dump(exclude_unset=True))
    if not updated_version:
        raise HTTPException(status_code=404, detail="Version not found")
    return updated_version


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections(
    filter_by: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """Lists all collections with optional filtering.

    Args:
        filter_by (Optional[str]): The field by which to filter collections.
        search (Optional[str]): The search query to filter collections.

    Returns:
        CollectionList: A list of collections and the total count.

    Example Usage:
        curl -X GET "http://localhost:8000/collections?filter_by=name&search=Alpha"
    """
    collections = storage.get_all_collections()
    
    # Implement filtering logic if search is provided
    if search and filter_by in ["name"]:  # Assuming name is the only filterable field here
        search_lower = search.lower()
        collections = [c for c in collections if search_lower in getattr(c, filter_by).lower()]
    
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Gets a specific collection by collection ID.

    Args:
        collection_id (str): The ID of the collection to retrieve.

    Returns:
        Collection: The requested collection object.

    Example Usage:
        curl -X GET http://localhost:8000/collections/456
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Creates a new collection.

    Args:
        collection_data (CollectionCreate): The data for the new collection.

    Returns:
        Collection: The created collection object.

    Example Usage:
        curl -X POST http://localhost:8000/collections -d '{"name": "New Collection"}'
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Deletes a specific collection and updates related prompts.

    Args:
        collection_id (str): The ID of the collection to delete.

    Returns:
        None

    Example Usage:
        curl -X DELETE http://localhost:8000/collections/456
    """
    # Retrieve all existing prompts
    all_prompts = storage.get_all_prompts()

    # Update all prompts that belong to the deleted collection to have no collection_id
    for prompt in all_prompts:
        if prompt.collection_id == collection_id:
            prompt.collection_id = None
            storage.update_prompt(prompt.id, prompt)  # Update prompt with collection_id set to None

    # Proceed with deleting the specified collection
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    return None
