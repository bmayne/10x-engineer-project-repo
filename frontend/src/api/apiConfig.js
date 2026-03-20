// Use this file to configure API integration

const BASE_URL = 'http://localhost:8000'; // Updated to point to the backend API

export const fetchData = async (endpoint) => {
    try {
        const response = await fetch(`${BASE_URL}/${endpoint}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    } catch (error) {
        console.error('Failed to fetch data:', error);
    }
};

