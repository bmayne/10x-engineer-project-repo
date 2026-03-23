import React, { useState, useEffect } from 'react';
import styles from '../styles/PromptForm.module.css';
import { getCollections } from '../api/collections';

const PromptForm = ({ onSubmit, initialData = {}}) => {
    const [title, setTitle] = useState(initialData.title || '');
    const [description, setDescription] = useState(initialData.description || '');
    const [content, setContent] = useState(initialData.content || '');
    const [collectionId, setCollectionId] = useState(initialData.collection_id || '');
    const [collections, setCollections] = useState([]); // State for collections

    useEffect(() => {
        const fetchCollections = async () => {
            try {
                const data = await getCollections();
                setCollections(data.collections); // Update state with fetched collections
            } catch (error) {
                console.error('Failed to fetch collections:', error);
            }
        };

        fetchCollections();
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (title && description && content) { // Ensure content is included
            onSubmit({ title, description, content, collection_id: collectionId});
        }
    };

    return (
        <form className={styles.promptForm} onSubmit={handleSubmit}>
            <div>
                <label>Title</label>
                <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
            </div>
            <div>
                <label>Description</label>
                <textarea value={description} onChange={(e) => setDescription(e.target.value)} required />
            </div>
            <div>
                <label>Content</label> {/* Add Content field */}
                <textarea value={content} onChange={(e) => setContent(e.target.value)} required />
            </div>
            <div>
                <label>Collection</label>
                <select value={collectionId} onChange={(e) => setCollectionId(e.target.value)}>
                    <option value="">No Collection</option>
                    {collections.map((collection) => (
                        <option key={collection.id} value={collection.id}>
                            {collection.name}
                        </option>
                    ))}
                </select>
            </div>
            <button type="submit">Save</button>
        </form>
    );
};

export default PromptForm;