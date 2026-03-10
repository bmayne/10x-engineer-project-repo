"""Utility functions for PromptLab"""

from fastapi import HTTPException
from datetime import datetime
from typing import List
from app.models import Prompt


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filters prompts by a specific collection ID.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to filter.
        collection_id (str): The collection ID to filter by.

    Returns:
        List[Prompt]: A list of Prompt objects that belong to the specified collection.

    Example Usage:
        filtered_prompts = filter_prompts_by_collection(prompts_list, 'collection123')
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Searches prompts by title or description matching a query.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to search.
        query (str): The search keyword.

    Returns:
        List[Prompt]: A list of Prompt objects that match the search query.

    Example Usage:
        search_results = search_prompts(prompts_list, 'keyword')
    """
    if not query:
        return []
    
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def raise_if_not_found(entity, entity_type: str) -> None:
    if not entity:
        raise HTTPException(status_code=404, detail=f"{entity_type} not found")