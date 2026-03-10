import pytest
from app.storage import storage
from app.models import Prompt, PromptVersion, Collection
from uuid import uuid4
from pydantic import ValidationError

class TestStorage:
    """Test suite for storage CRUD operations and data persistence."""

    def test_create_and_read_prompt(self):
        # Create a new prompt
        prompt_id = str(uuid4())
        prompt = Prompt(id=prompt_id, title="Test Prompt", content="Test content")
        storage.create_prompt(prompt)

        # Retrieve the created prompt
        retrieved_prompt = storage.get_prompt(prompt_id)
        assert retrieved_prompt is not None
        assert retrieved_prompt.title == "Test Prompt"
        assert retrieved_prompt.content == "Test content"

    def test_update_prompt(self):
        # Create a prompt and update it
        prompt_id = str(uuid4())
        prompt = Prompt(id=prompt_id, title="Old Title", content="Old content")
        storage.create_prompt(prompt)

        # Update the prompt
        updated_data = {"title": "New Title", "content": "New content"}
        updated_prompt = Prompt(**{**prompt.model_dump(), **updated_data})
        storage.update_prompt(prompt_id, updated_prompt)

        # Retrieve and assert
        retrieved_prompt = storage.get_prompt(prompt_id)
        assert retrieved_prompt.title == "New Title"
        assert retrieved_prompt.content == "New content"

    def test_delete_prompt(self):
        # Create and delete a prompt
        prompt_id = str(uuid4())
        prompt = Prompt(id=prompt_id, title="Delete Me", content="Some content")
        storage.create_prompt(prompt)
        storage.delete_prompt(prompt_id)

        # Assert it no longer exists
        assert storage.get_prompt(prompt_id) is None

    def test_persistent_prompts(self):
        # Ensure prompts persist within session
        prompt_id1 = str(uuid4())
        prompt_id2 = str(uuid4())
        prompt1 = Prompt(id=prompt_id1, title="Persistent 1", content="Content 1")
        prompt2 = Prompt(id=prompt_id2, title="Persistent 2", content="Content 2")
        storage.create_prompt(prompt1)
        storage.create_prompt(prompt2)

        # Retrieve and assert both prompts are persisted
        assert len(storage.get_all_prompts()) >= 2

    def test_create_and_get_prompt_version(self):
        # Create a PromptVersion
        prompt_id = str(uuid4())
        version_data = PromptVersion(prompt_id=prompt_id, title="Version 1", content="Initial content")
        created_version = storage.create_prompt_version(version_data)

        # Retrieve the PromptVersion by ID
        retrieved_version = storage.get_prompt_version(created_version.id)
        assert retrieved_version is not None
        assert retrieved_version.title == "Version 1"
        assert retrieved_version.content == "Initial content"

    def test_list_versions_for_prompt(self):
        # Create and add multiple versions for a specific prompt
        prompt_id = str(uuid4())
        version1 = PromptVersion(prompt_id=prompt_id, title="Version 1", content="Content 1")
        version2 = PromptVersion(prompt_id=prompt_id, title="Version 2", content="Content 2")

        storage.create_prompt_version(version1)
        storage.create_prompt_version(version2)

        # List all versions for the prompt_id
        versions = storage.list_versions_for_prompt(prompt_id)
        assert len(versions) == 2
        titles = {v.title for v in versions}
        assert "Version 1" in titles
        assert "Version 2" in titles

    def test_update_prompt_version(self):
        # Create a PromptVersion to update
        prompt_id = str(uuid4())
        version = PromptVersion(prompt_id=prompt_id, title="Initial Version", content="Initial content")
        storage.create_prompt_version(version)

        # Define the update and execute
        update_data = {"title": "Updated Version"}
        updated_version = storage.update_prompt_version(version.id, update_data)

        # Verify update
        assert updated_version is not None
        assert updated_version.title == "Updated Version"
        assert updated_version.content == "Initial content"

    def test_get_non_existent_prompt_version(self):
        # Attempt to retrieve a non-existing version
        retrieved_version = storage.get_prompt_version("non-existent-id")
        assert retrieved_version is None

    def test_create_collection(self):
        # Create a new collection
        collection_id = str(uuid4())
        collection = Collection(id=collection_id, name="Test Collection")
        storage.create_collection(collection)

        # Retrieve and assert
        retrieved_collection = storage.get_collection(collection_id)
        assert retrieved_collection is not None
        assert retrieved_collection.name == "Test Collection"

    def test_edge_case_empty_title(self):
        # Attempt to create a prompt with an empty title
        prompt_id = str(uuid4())
        prompt_data = {"id": prompt_id, "title": "", "content": "No title content"}
        
        # Expectation: ValidationError is raised due to title length
        with pytest.raises(ValidationError) as exc_info:
            prompt = Prompt(**prompt_data)
            storage.create_prompt(prompt)
        
        # Assert the error message is correct
        assert "title\n  String should have at least 1 character" in str(exc_info.value)