import pytest
from app.utils import filter_prompts_by_collection, search_prompts
from app.models import Prompt

class TestUtils:
    """Test suite for utility functions."""

    def test_filter_prompts_by_collection(self):
        prompts = [
            Prompt(id="1", title="Prompt 1", content="Content 1", collection_id="abc"),
            Prompt(id="2", title="Prompt 2", content="Content 2", collection_id="def"),
        ]
        filtered = filter_prompts_by_collection(prompts, "abc")
        assert len(filtered) == 1
        assert filtered[0].collection_id == "abc"

    def test_search_prompts(self):
        prompts = [
            Prompt(id="1", title="Hello World", content="Content"),
            Prompt(id="2", title="Another Title", content="Different Content"),
        ]
        results = search_prompts(prompts, "hello")
        assert len(results) == 1
        assert results[0].title == "Hello World"

    def test_edge_case_empty_search(self):
        prompts = [Prompt(id="1", title="Sample", content="Content")]
        results = search_prompts(prompts, "")
        assert len(results) == 0

    def test_edge_case_no_collection_prompts(self):
        prompts = [Prompt(id="1", title="Sample", content="Content")]
        filtered = filter_prompts_by_collection(prompts, "invalid_id")
        assert len(filtered) == 0
