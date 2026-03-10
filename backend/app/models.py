"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    return str(uuid4())


def get_current_time() -> datetime:
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base class for Prompt models.

    Attributes:
        title (str): The title of the prompt. Must be between 1 and 200 characters.
        content (str): The actual content of the prompt. Must have at least 1 character.
        description (Optional[str]): A brief description of the prompt, maximum 500 characters.
        collection_id (Optional[str]): The ID of the associated collection.

    Example:
        >>> prompt = PromptBase(
        ...     title="Example Title",
        ...     content="This is the content of the prompt.",
        ...     description="An optional description.",
        ...     collection_id="123e4567-e89b-12d3-a456-426614174000"
        ... )
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Model for creating a new Prompt.
    
    Inherits attributes from PromptBase.
    """
    pass


class PromptUpdate(PromptBase):
    """Model for updating an existing Prompt.
    
    Inherits attributes from PromptBase.
    """
    pass


class PromptPatch(BaseModel):
    """Model for patching a Prompt with partial data.
    
    Attributes:
        title (Optional[str]): The title of the prompt. Must be between 1 and 200 characters.
        content (Optional[str]): The actual content of the prompt. Must have at least 1 character.
        description (Optional[str]): A brief description of the prompt, maximum 500 characters.
        collection_id (Optional[str]): The ID of the associated collection.
    
    Example:
        >>> patch_data = PromptPatch(
        ...     title="Updated Title",
        ...     content="Updated content of the prompt."
        ... )
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class Prompt(PromptBase):
    """Full Prompt model including metadata.

    Attributes:
        id (str): The unique identifier for the prompt. Defaults to a generated UUID.
        created_at (datetime): The time the prompt was created. Defaults to the current UTC time.
        updated_at (datetime): The time the prompt was last updated. Defaults to the current UTC time.

    Example:
        >>> prompt = Prompt(
        ...     title="Example Title",
        ...     content="This is the content of the prompt.",
        ...     id="123e4567-e89b-12d3-a456-426614174000",
        ...     created_at=datetime(2023, 11, 14, 14, 00, 00),
        ...     updated_at=datetime(2023, 11, 14, 14, 00, 00)
        ... )
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base class for Collection models.

    Attributes:
        name (str): The name of the collection. Must be between 1 and 100 characters.
        description (Optional[str]): A brief description of the collection, maximum 500 characters.

    Example:
        >>> collection = CollectionBase(
        ...     name="Example Collection",
        ...     description="An optional description of the collection."
        ... )
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Model for creating a new Collection.
    
    Inherits attributes from CollectionBase.
    """
    pass


class Collection(CollectionBase):
    """Full Collection model including metadata.
    
    Attributes:
        id (str): The unique identifier for the collection. Defaults to a generated UUID.
        created_at (datetime): The time the collection was created. Defaults to the current UTC time.

    Example:
        >>> collection = Collection(
        ...     name="Example Collection",
        ...     description="An optional description of the collection.",
        ...     id="123e4567-e89b-12d3-a456-426614174000",
        ...     created_at=datetime(2023, 11, 14, 14, 00, 00)
        ... )
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Model for a list of prompts.

    Attributes:
        prompts (List[Prompt]): A list containing Prompt objects.
        total (int): The total number of prompts in the list.

    Example:
        >>> prompt_list = PromptList(
        ...     prompts=[Prompt(title="Title 1", content="Content 1")],
        ...     total=1
        ... )
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Model for a list of collections.

    Attributes:
        collections (List[Collection]): A list containing Collection objects.
        total (int): The total number of collections in the list.

    Example:
        >>> collection_list = CollectionList(
        ...     collections=[Collection(name="Collection 1")],
        ...     total=1
        ... )
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Model for representing the health status of the service.

    Attributes:
        status (str): The current status of the service, e.g., 'Healthy'.
        version (str): The current version of the service.

    Example:
        >>> health = HealthResponse(
        ...     status="Healthy",
        ...     version="1.0.0"
        ... )
    """
    status: str
    version: str


class PromptVersion(BaseModel):
    id: str = Field(default_factory=generate_id)
    prompt_id: Optional[str] = None
    title: str
    content: Optional[str] = Field(None, min_length=1)
    created_at: datetime = Field(default_factory=get_current_time)


class PromptVersionList(BaseModel):
    versions: List[PromptVersion]
    total: int