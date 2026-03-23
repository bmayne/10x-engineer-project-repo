import React, { useState } from 'react';
import styles from '../styles/PromptForm.module.css';

const PromptForm = ({ onSubmit, initialData = {} }) => {
    const [title, setTitle] = useState(initialData.title || '');
    const [description, setDescription] = useState(initialData.description || '');
    const [content, setContent] = useState(initialData.content || ''); // Add state for content

    const handleSubmit = (e) => {
        e.preventDefault();
        if (title && description && content) { // Ensure content is included
            onSubmit({ title, description, content });
        }
    };

    return (
        <form className={styles.promptForm} onSubmit={handleSubmit}>
            <div>
                <label>Title</label>
                <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
            </div>
            <div>
                <label>Content</label> {/* Add Content field */}
                <textarea value={content} onChange={(e) => setContent(e.target.value)} required />
            </div>
            <div>
                <label>Description</label>
                <textarea value={description} onChange={(e) => setDescription(e.target.value)} required />
            </div>
            <button type="submit">Save</button>
        </form>
    );
};

export default PromptForm;