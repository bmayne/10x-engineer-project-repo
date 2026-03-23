const BASE_URL = 'https://obscure-spoon-jvp9554jqvc769-8000.app.github.dev';

const handleResponse = async (response) => {
    if (response.ok) {  // Check for any 2xx status code
        // If status is 204, return a success without processing JSON
        if (response.status === 204) return true;
        return response.json();  // For other 2xx status with content
    } else {
        const errorData = await response.json();
        const error = new Error('An error occurred');
        error.data = errorData;
        error.status = response.status;
        throw error;
    }
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
