import React from 'react';
import styles from '../styles/Header.module.css'; // Correct path to CSS

const Header = ({ currentView, onSelectView }) => {
    return (
        <header className={styles.header}>
            <div className={styles.logo}>PromptLab</div>
            <nav className={styles.navigation}>
                <ul>
                    <li
                        className={currentView === 'Prompts' ? styles.activeTab : styles.inactiveTab}
                        onClick={() => onSelectView('Prompts')}
                    >
                        Prompts
                    </li>
                    <li
                        className={currentView === 'Collections' ? styles.activeTab : styles.inactiveTab}
                        onClick={() => onSelectView('Collections')}
                    >
                        Collections
                    </li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
