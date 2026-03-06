"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sorts a list of prompts by their creation date.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to be sorted.
        descending (bool, optional): Determines the sorting order. Defaults to True.

    Returns:
        List[Prompt]: The sorted list of Prompt objects.

    Example Usage:
        sorted_prompts = sort_prompts_by_date(prompts_list)
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


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
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Validates the content of a prompt.

    Checks if the prompt content:
    - Is not empty or just whitespace
    - Contains at least 10 characters

    Args:
        content (str): The content of the prompt to validate.

    Returns:
        bool: True if the content is valid, otherwise False.

    Example Usage:
        is_valid = validate_prompt_content('Sample prompt content')
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Variables are in the format {{variable_name}}
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
