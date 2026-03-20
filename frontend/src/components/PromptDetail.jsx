import React from 'react';
import styles from './PromptDetail.module.css';

const PromptDetail = ({ prompt }) => {
    return (
        <div className={styles.promptDetail}>
            <h1>{prompt.title}</h1>
            <p>{prompt.description}</p>
            {/* Display additional detailed information about the prompt here */}
        </div>
    );
};

export default PromptDetail;
