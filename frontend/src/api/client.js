const BASE_URL = 'https://obscure-spoon-jvp9554jqvc769-8000.app.github.dev';

const handleResponse = async (response) => {
    if (!response.ok) {
        const errorData = await response.json();
        const error = new Error('An error occurred');
        error.data = errorData;
        error.status = response.status;
        throw error;
    }
    return response.json();
};

const fetchWrapper = async (url, options = {}) => {
    try {
        const response = await fetch(`${BASE_URL}${url}`, {
            headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
            ...options,
        });
        return await handleResponse(response);
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
};

export default fetchWrapper;
