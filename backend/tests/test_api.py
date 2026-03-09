"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealth:
    """Tests for health endpoint."""
    
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestPrompts:
    """Tests for prompt endpoints."""
    
    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data
    
    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0
    
    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)
        
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1
    
    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
    
    def test_get_prompt_not_found(self, client: TestClient):
        """Test that getting a non-existent prompt returns 404."""
        response = client.get("/prompts/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/prompts/{prompt_id}")
        # Note: This might fail due to Bug #1
        assert get_response.status_code in [404, 500]  # 404 after fix
    
    def test_update_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Update it
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the prompt",
            "description": "Updated description"
        }
        
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp would change
        
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
     
        # The updated_at should be different from original
        assert data["updated_at"] != original_updated_at

    def test_patch_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Update it
        updated_data = {
            "content": "Patched content for the prompt",
            "description": "Patched description"
        }
        
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp would change
        
        response = client.patch(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == updated_data["content"]
        assert data["description"] == updated_data["description"]
        assert data["title"] == sample_prompt_data["title"]
     
        # The updated_at should be different from original
        assert data["updated_at"] != original_updated_at
    
    def test_sorting_order(self, client: TestClient):
        """Test that prompts are sorted newest first."""
        import time
        
        # Create prompts with delay
        prompt1 = {"title": "First", "content": "First prompt content"}
        prompt2 = {"title": "Second", "content": "Second prompt content"}
        
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)
        
        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        
        # Newest (Second) should be first
        assert prompts[0]["title"] == "Second"

    def test_get_prompt_invalid_id(self, client: TestClient):
        response = client.get("/prompts/invalid-id")
        assert response.status_code == 404

    def test_create_prompt_empty_title(self, client: TestClient, sample_prompt_data):
        sample_prompt_data["title"] = ""
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 422

    def test_query_prompts_with_sorting(self, client: TestClient, sample_prompt_data):
        # Create multiple prompts
        prompt1 = {"title": "First", "content": "A content"}
        prompt2 = {"title": "Second", "content": "B content"}
        client.post("/prompts", json=prompt1)
        client.post("/prompts", json=prompt2)

        response = client.get("/prompts?sort_by=title&sort_order=asc")
        data = response.json()
        prompts = data["prompts"]
        # Test sorting order by title
        assert prompts[0]["title"] == "First"

class TestCollections:
    """Tests for collection endpoints."""
    
    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data
    
    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1
    
    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test deleting a collection that has prompts."""
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        
        # Delete collection
        client.delete(f"/collections/{collection_id}")
 
        prompts = client.get("/prompts").json()["prompts"]
        if prompts:
            assert prompts[0]["collection_id"] is None

    def test_create_collection_with_special_characters(self, client: TestClient, sample_collection_data):
        sample_collection_data["name"] = "!@#$%^&*()"
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201

    def test_list_collections_with_filter(self, client: TestClient, sample_collection_data):
        # Create several collections
        collection1 = {**sample_collection_data, "name": "Alpha"}
        collection2 = {**sample_collection_data, "name": "Beta"}
        
        client.post("/collections", json=collection1)
        client.post("/collections", json=collection2)
        
        # Test filtering collections by name containing "Alpha"
        response = client.get("/collections?filter_by=name&search=Alpha")
        assert response.status_code == 200
        data = response.json()
        collections = data["collections"]
        
        # Assert that only the filtered collection is returned
        assert len(collections) == 1
        assert collections[0]["name"] == "Alpha"
