import React from 'react';
import styles from '../styles/Sidebar.module.css';

const Sidebar = ({ title, items, selectedItem, onItemClick, onAddClick }) => {
    return (
        <aside className={styles.sidebar}>
            <div className={styles.sidebarHeader}>
                <h2>{title}</h2>
                <button 
                    aria-label={`Add ${title}`} 
                    className={styles.addButton} 
                    onClick={onAddClick} // Trigger the add action here
                >
                    +
                </button>
            </div>
            <nav>
                <ul>
                    {items.map((item) => (
                        <li key={item.id} onClick={() => onItemClick(item)}
                        className={item.id === selectedItem?.id ? styles.selectedItem : ''}>
                            {title === 'Prompts' ? item.title : item.name}
                        </li>
                    ))}
                </ul>
            </nav>
        </aside>
    );
};

export default Sidebar;