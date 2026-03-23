import React from 'react';
import styles from '../styles/CollectionList.module.css';

const CollectionList = ({ collections }) => {
    return (
        <div className={styles.collectionList}>
            <ul>
                {collections.map(collection => (
                    <li key={collection.id}>{collection.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default CollectionList;
