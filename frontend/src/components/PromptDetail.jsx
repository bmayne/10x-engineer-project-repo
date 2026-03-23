import React, { useState, useEffect } from 'react';
import styles from '../styles/PromptDetail.module.css';
import { getCollection } from '../api/collections';

const PromptDetail = ({ prompt, onEdit, onDelete }) => {
    const [collectionName, setCollectionName] = useState('');

    useEffect(() => {
        const fetchCollectionName = async () => {
            if (prompt.collection_id) { // Only fetch if prompt is tied to a collection
                try {
                    const collectionData = await getCollection(prompt.collection_id);
                    setCollectionName(collectionData.name);
                } catch (error) {
                    console.error('Failed to fetch collection name:', error);
                }
            } else {
                setCollectionName(''); // Clear previous collection name if no collection_id
            }
        };

        fetchCollectionName();
    }, [prompt.collection_id]);
    
    return (
        <div className={styles.promptDetail}>
            <h2>{prompt.title}</h2>
            <p><strong>Description:</strong> {prompt.description}</p>
            <p><strong>Content:</strong> {prompt.content}</p>
            {collectionName && (
                <p><strong>Collection:</strong> {collectionName}</p>
            )}
            <div className={styles.buttonContainer}>
                <button className={styles.editButton} onClick={onEdit}>Edit</button>
                <button className={styles.deleteButton} onClick={onDelete}>Delete</button>
            </div>
        </div>
    );
};

export default PromptDetail;


