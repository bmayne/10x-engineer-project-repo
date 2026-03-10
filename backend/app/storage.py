"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, PromptVersion, Collection


class Storage:
    """In-memory storage for prompts and collections.

    This class acts as a temporary in-memory storage, substituting for a database
    by storing `Prompt` and `Collection` objects.
    
    Attributes:
        _prompts (Dict[str, Prompt]): A dictionary storing prompts by their IDs.
        _collections (Dict[str, Collection]): A dictionary storing collections by their IDs.
    """

    def __init__(self):
        """Initializes a new Storage instance with empty storage."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._prompt_versions: Dict[str, PromptVersion] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Stores a new prompt in the storage.

        Args:
            prompt (Prompt): The prompt object to store.

        Returns:
            Prompt: The stored prompt instance.

        Example Usage:
            >>> storage.create_prompt(Prompt(id='1', text='Sample prompt', collection_id='1'))
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieves a prompt by its ID.

        Args:
            prompt_id (str): The unique identifier of the prompt.

        Returns:
            Optional[Prompt]: The prompt object if found, otherwise None.

        Example Usage:
            >>> prompt = storage.get_prompt('1')
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieves all prompts stored.

        Returns:
            List[Prompt]: A list of all prompt objects.

        Example Usage:
            >>> all_prompts = storage.get_all_prompts()
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Updates an existing prompt by its ID.

        Args:
            prompt_id (str): The unique identifier of the prompt to update.
            prompt (Prompt): The new prompt object with updated data.

        Returns:
            Optional[Prompt]: The updated prompt object if update was successful, otherwise None.

        Example Usage:
            >>> updated_prompt = storage.update_prompt('1', new_prompt)
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Deletes a prompt by its ID.

        Args:
            prompt_id (str): The unique identifier of the prompt to delete.

        Returns:
            bool: True if the prompt was deleted, otherwise False.

        Example Usage:
            >>> result = storage.delete_prompt('1')
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    def create_prompt_version(self, version: PromptVersion) -> PromptVersion:
        self._prompt_versions[version.id] = version
        return version

    def get_prompt_version(self, version_id: str) -> Optional[PromptVersion]:
        return self._prompt_versions.get(version_id)

    def list_versions_for_prompt(self, prompt_id: str) -> List[PromptVersion]:
        return [v for v in self._prompt_versions.values() if v.prompt_id == prompt_id]

    def update_prompt_version(self, version_id: str, version_data: dict) -> Optional[PromptVersion]:
        version = self._prompt_versions.get(version_id)
        if version:
            for key, value in version_data.items():
                setattr(version, key, value)
            return version
        return None

    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Stores a new collection in the storage.

        Args:
            collection (Collection): The collection object to store.

        Returns:
            Collection: The stored collection instance.

        Example Usage:
            >>> storage.create_collection(Collection(id='1', name='Sample Collection'))
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieves a collection by its ID.

        Args:
            collection_id (str): The unique identifier of the collection.

        Returns:
            Optional[Collection]: The collection object if found, otherwise None.

        Example Usage:
            >>> collection = storage.get_collection('1')
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieves all collections stored.

        Returns:
            List[Collection]: A list of all collection objects.

        Example Usage:
            >>> all_collections = storage.get_all_collections()
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Deletes a collection by its ID.

        Args:
            collection_id (str): The unique identifier of the collection to delete.

        Returns:
            bool: True if the collection was deleted, otherwise False.

        Example Usage:
            >>> result = storage.delete_collection('1')
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieves all prompts belonging to a specific collection.

        Args:
            collection_id (str): The unique identifier of the collection.

        Returns:
            List[Prompt]: A list of prompt objects associated with the given collection.

        Example Usage:
            >>> prompts = storage.get_prompts_by_collection('1')
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Clears all stored prompts and collections.

        Example Usage:
            >>> storage.clear()
        """
        self._prompts.clear()
        self._collections.clear()
        self._prompt_versions.clear()


# Global storage instance
storage = Storage()
