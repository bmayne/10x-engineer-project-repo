import pytest
from pydantic import ValidationError
from app.models import Prompt, Collection
from uuid import uuid4

class TestModels:
    def test_prompt_validation(self):
        # Test successful validation
        prompt_id = str(uuid4())
        prompt = Prompt(id=prompt_id, title="Valid Title", content="Valid content")
        assert prompt.title == "Valid Title"

        # Test validation error for empty title
        with pytest.raises(ValidationError) as exc_info:
            Prompt(id=prompt_id, title="", content="Valid content")
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_collection_validation(self):
        # Test successful validation
        collection_id = str(uuid4())
        collection = Collection(id=collection_id, name="Valid Name")
        assert collection.name == "Valid Name"

        # Test validation error for empty name
        with pytest.raises(ValidationError) as exc_info:
            Collection(id=collection_id, name="")
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_prompt_default_values(self):
        # Assuming some default values like empty description
        prompt = Prompt(id=str(uuid4()), title="Title", content="Content")
        assert prompt.description is None

    def test_prompt_serialization(self):
        prompt = Prompt(id=str(uuid4()), title="Serialize", content="Serialize content")
        data = prompt.model_dump()
        assert data["title"] == "Serialize"
        assert "created_at" in data  # Assuming auto-generated fields like timestamps

    def test_collection_serialization(self):
        collection = Collection(id=str(uuid4()), name="Serialize Collection")
        data = collection.model_dump()
        assert data["name"] == "Serialize Collection"