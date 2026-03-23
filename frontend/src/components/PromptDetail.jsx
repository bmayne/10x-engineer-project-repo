import React from 'react';
import styles from '../styles/PromptDetail.module.css';

const PromptDetail = ({ prompt }) => {
    return (
        <div className={styles.promptDetail}>
            <h2>{prompt.title}</h2>
            <p><strong>Description:</strong> {prompt.description}</p>
            <p><strong>Content:</strong> {prompt.content}</p> {/* Add Content with a Label */}
        </div>
    );
};

export default PromptDetail;
