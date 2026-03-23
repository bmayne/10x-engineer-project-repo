import React from 'react';
import styles from '../styles/PromptDetail.module.css';

const PromptDetail = ({ prompt, onEdit, onDelete }) => {
    return (
        <div className={styles.promptDetail}>
            <h2>{prompt.title}</h2>
            <p><strong>Description:</strong> {prompt.description}</p>
            <p><strong>Content:</strong> {prompt.content}</p> 
            <div className={styles.buttonContainer}>
                <button className={styles.editButton} onClick={onEdit}>Edit</button>
                <button className={styles.deleteButton} onClick={onDelete}>Delete</button>
            </div>
        </div>
    );
};

export default PromptDetail;
