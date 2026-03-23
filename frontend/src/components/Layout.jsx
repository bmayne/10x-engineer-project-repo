import React, { useState, useEffect } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import styles from '../styles/Layout.module.css';
import PromptList from './PromptList';
import PromptDetail from './PromptDetail';
import CollectionDetail from './CollectionDetail'; // Import CollectionDetail component
import Button from './shared/Button';
import Modal from './shared/Modal';
import PromptForm from './PromptForm';
import CollectionForm from './CollectionForm';
import { getPrompts, createPrompt } from '../api/prompts';
import { getCollections, createCollection } from '../api/collections';

const Layout = () => {
  const [selectedView, setSelectedView] = useState('Prompts');
  const [isPromptModalOpen, setIsPromptModalOpen] = useState(false);
  const [isCollectionModalOpen, setIsCollectionModalOpen] = useState(false);
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [selectedCollection, setSelectedCollection] = useState(null); // Track selected collection

  useEffect(() => {
    // Reset selected prompt or collection when switching views
    if (selectedView === 'Prompts') {
      setSelectedCollection(null); // Clear selected collection
    } else if (selectedView === 'Collections') {
      setSelectedPrompt(null); // Clear selected prompt
    }

    if (selectedView === 'Prompts') {
      const fetchPrompts = async () => {
        try {
          const data = await getPrompts();
          setPrompts(data.prompts);
        } catch (error) {
          console.error('Failed to fetch prompts:', error);
        }
      };

      fetchPrompts();
    } else if (selectedView === 'Collections') {
      const fetchCollections = async () => {
        try {
          const data = await getCollections();
          setCollections(data.collections);
        } catch (error) {
          console.error('Failed to fetch collections:', error);
        }
      };

      fetchCollections();
    }
  }, [selectedView]);

  const handleAddPrompt = () => setIsPromptModalOpen(true);
  const handleAddCollection = () => setIsCollectionModalOpen(true);
  const handleModalClose = () => {
    setIsPromptModalOpen(false);
    setIsCollectionModalOpen(false);
  };

  const handlePromptSubmit = async (promptData) => {
    try {
      const newPrompt = await createPrompt(promptData);
      setPrompts((prevPrompts) => [...prevPrompts, newPrompt]);
      setIsPromptModalOpen(false);
    } catch (error) {
      console.error('Failed to create prompt:', error);
    }
  };

  const handleCollectionSubmit = async (collectionData) => {
    try {
      const newCollection = await createCollection(collectionData);
      setCollections((prevCollections) => [...prevCollections, newCollection]);
      setIsCollectionModalOpen(false);
    } catch (error) {
      console.error('Failed to create collection:', error);
    }
  };

  const renderContent = () => {
    if (selectedView === 'Prompts') {
      return (
        <div className={styles.contentArea}>
          {selectedPrompt && <PromptDetail prompt={selectedPrompt} />}
        </div>
      );
    } else if (selectedView === 'Collections') {
      return (
        <div className={styles.contentArea}>
          {selectedCollection && (
            <CollectionDetail
              collection={selectedCollection}
              prompts={prompts.filter(prompt => prompt.collection_id === selectedCollection.id)}
            />
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className={styles.layout}>
      <Header className={styles.header} currentView={selectedView} onSelectView={setSelectedView} />
      <div className={styles.mainContainer}>
        <Sidebar 
          title={selectedView}
          items={selectedView === 'Prompts' ? prompts : collections}
          onItemClick={selectedView === 'Prompts' ? setSelectedPrompt : setSelectedCollection}
          onAddClick={selectedView === 'Prompts' ? handleAddPrompt : handleAddCollection}
        />
        <main className={styles.mainContent}>
          {renderContent()}
        </main>
      </div>
      <Modal isOpen={isPromptModalOpen} onClose={handleModalClose}>
        <PromptForm onSubmit={handlePromptSubmit} />
      </Modal>
      <Modal isOpen={isCollectionModalOpen} onClose={handleModalClose}>
        <CollectionForm onSubmit={handleCollectionSubmit} />
      </Modal>
    </div>
  );
};

export default Layout;
