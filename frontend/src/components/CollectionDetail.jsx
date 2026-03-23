import React from 'react';
import styles from '../styles/CollectionDetail.module.css';

const CollectionDetail = ({ collection, prompts, onEdit, onDelete }) => {
    return (
        <div className={styles.collectionDetail}>
            <h2>{collection.name}</h2>
            <h3>Prompts in this Collection:</h3>
            <ul>
                {prompts.map(prompt => (
                    <li key={prompt.id}>{prompt.title}</li>
                ))}
            </ul>
            <div className={styles.buttonContainer}>
                <button className={styles.deleteButton} onClick={onDelete}>Delete</button>
            </div>
        </div>
    );
};

export default CollectionDetail;