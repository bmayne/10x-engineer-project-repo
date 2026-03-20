import React, { useState } from 'react';
import styles from './CollectionForm.module.css';

const CollectionForm = ({ onSubmit }) => {
    const [name, setName] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ name });
    };

    return (
        <form className={styles.collectionForm} onSubmit={handleSubmit}>
            <div>
                <label>Collection Name</label>
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <button type="submit">Create Collection</button>
        </form>
    );
};

export default CollectionForm;
