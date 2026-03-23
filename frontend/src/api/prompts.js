import fetchWrapper from './client';

export const getPrompts = async () => {
    return fetchWrapper('/prompts');
};

export const getPrompt = async (id) => {
    return fetchWrapper(`/prompts/${id}`);
};

export const getPromptsByCollection = async (collectionId) => {
    return fetchWrapper(`/prompts?collection_id=${collectionId}`);
};

export const createPrompt = async (data) => {
    return fetchWrapper('/prompts', {
        method: 'POST',
        body: JSON.stringify(data),
    });
};

export const updatePrompt = async (id, data) => {
    return fetchWrapper(`/prompts/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    });
};

export const deletePrompt = async (id) => {
    return fetchWrapper(`/prompts/${id}`, {
        method: 'DELETE',
    });
};
