import React from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import styles from './Layout.module.css';

const Layout = ({ children }) => {
    return (
        <div className={styles.layout}>
            <Header />
            <div className={styles.mainContent}>
                <Sidebar />
                <div className={styles.contentArea}>
                    {children}
                </div>
            </div>
        </div>
    );
};

export default Layout;
