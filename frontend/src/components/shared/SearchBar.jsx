import React from 'react';
import styles from './SearchBar.module.css';

const SearchBar = ({ value, onChange, placeholder = 'Search...' }) => {
    return (
        <input
            type="text"
            className={styles.searchBar}
            value={value}
            onChange={onChange}
            placeholder={placeholder}
        />
    );
};

export default SearchBar;
