import React from 'react';
import styles from './Sidebar.module.css';

const Sidebar = () => {
    return (
        <aside className={styles.sidebar}>
            <nav>
                <ul>
                    <li>Collection 1</li>
                    <li>Collection 2</li>
                    <li>Collection 3</li>
                    {/* Add more collections or links as needed */}
                </ul>
            </nav>
        </aside>
    );
};

export default Sidebar;
