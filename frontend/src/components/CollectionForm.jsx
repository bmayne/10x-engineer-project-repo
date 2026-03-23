import React, { useState, useEffect, useRef } from 'react';
import styles from '../styles/CollectionForm.module.css';

const CollectionForm = ({ onSubmit, errorMessage }) => {
    const [name, setName] = useState('');
    const nameRef = useRef(null); // Reference to the name input

    useEffect(() => {
        nameRef.current?.focus(); // Automatically focus on title input on component mount
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ name });
    };

    return (
        <form className={styles.collectionForm} onSubmit={handleSubmit}>
            {errorMessage && <div className={styles.error}>{errorMessage}</div>}
            <div>
                <label>Collection Name</label>
                <input type="text" ref={nameRef} value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <button type="submit">Create Collection</button>
        </form>
    );
};

export default CollectionForm;
