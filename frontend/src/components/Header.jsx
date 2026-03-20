import React from 'react';
import styles from './Header.module.css';

const Header = () => {
    return (
        <header className={styles.header}>
            <div className={styles.logo}>MyApp</div>
            <nav className={styles.navigation}>
                {/* Add navigation items here */}
            </nav>
        </header>
    );
};

export default Header;
