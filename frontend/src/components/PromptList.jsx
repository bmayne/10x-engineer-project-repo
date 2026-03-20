import React from 'react';
import PromptCard from './PromptCard';
import styles from './PromptList.module.css';

const PromptList = ({ prompts }) => {
    return (
        <div className={styles.promptList}>
            {prompts.map(prompt => (
                <PromptCard key={prompt.id} prompt={prompt} />
            ))}
        </div>
    );
};

export default PromptList;
