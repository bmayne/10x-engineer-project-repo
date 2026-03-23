import React from 'react';
import styles from '../styles/CollectionDetail.module.css';

const CollectionDetail = ({ collection, prompts, onDelete }) => {
    return (
        <div className={styles.collectionDetail}>
            <h2>{collection.name}</h2>
            {prompts.length > 0 ? (
                <>
                    <h3>Prompts in this Collection:</h3>
                    <ul>
                        {prompts.map(prompt => (
                            <li key={prompt.id}><strong>Title:</strong> {prompt.title}</li>
                        ))}
                    </ul>
                </>
            ) : (
                <p>There are no Prompts in this Collection</p> // Message for empty collections
            )}
            <div className={styles.buttonContainer}>
                <button className={styles.deleteButton} onClick={onDelete}>Delete</button>
            </div>
        </div>
    );
};

export default CollectionDetail;