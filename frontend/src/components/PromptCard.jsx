import React from 'react';
import styles from './PromptCard.module.css';

const PromptCard = ({ prompt }) => {
    return (
        <div className={styles.promptCard}>
            <h2>{prompt.title}</h2>
            <p>{prompt.description}</p>
            {/* Additional prompt details can be displayed here */}
        </div>
    );
};

export default PromptCard;
