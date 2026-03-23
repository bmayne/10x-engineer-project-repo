import fetchWrapper from './client';

export const getCollections = async () => {
    return fetchWrapper('/collections');
};

export const getCollection = async (id) => {
    return fetchWrapper(`/collections/${id}`);
};

export const createCollection = async (data) => {
    return fetchWrapper('/collections', {
        method: 'POST',
        body: JSON.stringify(data),
    });
};

export const deleteCollection = async (id) => {
    return fetchWrapper(`/collections/${id}`, {
        method: 'DELETE',
    });
};
