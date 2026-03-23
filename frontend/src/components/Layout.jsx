import React, { useState, useEffect } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import styles from '../styles/Layout.module.css';
import PromptDetail from './PromptDetail';
import CollectionDetail from './CollectionDetail'; // 
import Spinner from './Spinner';
import Modal from './shared/Modal';
import PromptForm from './PromptForm';
import CollectionForm from './CollectionForm';
import { getPrompt, getPrompts, getPromptsByCollection, createPrompt, updatePrompt, deletePrompt } from '../api/prompts';
import { getCollection, getCollections, createCollection, deleteCollection } from '../api/collections';

const Layout = () => {
  const [selectedView, setSelectedView] = useState('Prompts');
  const [isPromptModalOpen, setIsPromptModalOpen] = useState(false);
  const [isCollectionModalOpen, setIsCollectionModalOpen] = useState(false);
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [selectedPrompt, setSelectedPrompt] = useState(null);
  const [selectedCollection, setSelectedCollection] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [collectionPrompts, setCollectionPrompts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(''); // State for error messages



  useEffect(() => {
    // Reset selected prompt or collection when switching views
    if (selectedView === 'Prompts') {
      setSelectedCollection(null); // Clear selected collection
    } else if (selectedView === 'Collections') {
      setSelectedPrompt(null); // Clear selected prompt
    }

    setLoading(true);

    if (selectedView === 'Prompts') {
      const fetchPrompts = async () => {
        try {
          const data = await getPrompts();
          setPrompts(data.prompts);
        } catch (error) {
          console.error('Failed to fetch prompts:', error);
        } finally {
          setLoading(false);
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
        } finally {
          setLoading(false);
        }
      };
      fetchCollections();
    }
  }, [selectedView]);

  const handleAddPrompt = () => {
    setIsPromptModalOpen(true);
    setIsEditing(false);
  }

  const handleEditPrompt = () => {
    setIsPromptModalOpen(true);
    setIsEditing(true);
  };

  const handleAddCollection = () => setIsCollectionModalOpen(true);
  const handleModalClose = () => {
    setIsPromptModalOpen(false);
    setIsCollectionModalOpen(false);
    setErrorMessage('');
  };

  const handlePromptSubmit = async (promptData) => {
    try {
      if (isEditing && selectedPrompt) {
        // Update existing prompt
        const updatedPrompt = await updatePrompt(selectedPrompt.id, promptData);
        setPrompts((prevPrompts) =>
          prevPrompts.map((p) => (p.id === updatedPrompt.id ? updatedPrompt : p))
        );
        setSelectedPrompt(updatedPrompt);
      } else {
        const newPrompt = await createPrompt(promptData);
        setPrompts((prevPrompts) => [...prevPrompts, newPrompt]);
        setSelectedPrompt(newPrompt);
      }
      setIsPromptModalOpen(false);
      setErrorMessage(''); // Clear error if successful
    } catch (error) {
      if (error.data && error.data.detail) {
        setErrorMessage(error.data.detail); // Display detailed error message
      } else {
        setErrorMessage('Failed to save prompt.'); // Generic fallback message
      }
    }
  };

  const handleCollectionSubmit = async (collectionData) => {
    try {
      const newCollection = await createCollection(collectionData);
      setCollections((prevCollections) => [...prevCollections, newCollection]);
      setSelectedCollection(newCollection);
      setIsCollectionModalOpen(false);
      setErrorMessage(''); // Clear error if successful
    } catch (error) {
      if (error.data && error.data.detail) {
        setErrorMessage(error.data.detail); // Display detailed error message
      } else {
        setErrorMessage('Failed to save collection.'); // Generic fallback message
      }
    }
  };

  const handleDeletePrompt = async () => {
    if (selectedPrompt) {
        const userConfirmed = window.confirm(`Are you sure you want to delete the prompt titled "${selectedPrompt.title}"?`);
        if (userConfirmed) {
            try {
                const success = await deletePrompt(selectedPrompt.id);
                if (success) {
                    setPrompts((prevPrompts) => prevPrompts.filter(p => p.id !== selectedPrompt.id));
                    setSelectedPrompt(null); // Clear the selected prompt
                }
            } catch (error) {
                console.error('Failed to delete prompt:', error);
            }
        }
    }
  };

  const handleDeleteCollection = async () => {
    if (selectedCollection) {
        const userConfirmed = window.confirm(`Are you sure you want to delete the collection named "${selectedCollection.name}"?`);
        if (userConfirmed) {
            try {
                const success = await deleteCollection(selectedCollection.id);
                if (success) {
                    setCollections((prevCollections) => prevCollections.filter(c => c.id !== selectedCollection.id));
                    setSelectedCollection(null); // Clear the selected collection
                }
            } catch (error) {
                console.error('Failed to delete collection:', error);
            }
        }
    }
  };

  const handleSelectPrompt = async (prompt) => {
    try {
      setLoading(true);
      const fetchedPrompt = await getPrompt(prompt.id);
      setSelectedPrompt(fetchedPrompt);
    } catch (error) {
      console.error('Failed to fetch prompt details:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectCollection = async (collection) => {
    try {
      setLoading(true);
      const fetchedCollection = await getCollection(collection.id);
      setSelectedCollection(fetchedCollection);
      const fetchedPrompts = await getPromptsByCollection(collection.id); // Fetch associated prompts
      setCollectionPrompts(fetchedPrompts.prompts);
    } catch (error) {
      console.error('Failed to fetch collection details:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderContent = () => {
    if (selectedView === 'Prompts') {
      return (
        <div className={styles.contentArea}>
          {selectedPrompt && <PromptDetail prompt={selectedPrompt} onEdit={handleEditPrompt} onDelete={handleDeletePrompt}/>}
        </div>
      );
    } else if (selectedView === 'Collections') {
      return (
        <div className={styles.contentArea}>
          {selectedCollection && (
            <CollectionDetail
              collection={selectedCollection}
              prompts={collectionPrompts} onDelete={handleDeleteCollection}
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
          selectedItem={selectedView === 'Prompts' ? selectedPrompt : selectedCollection}
          onItemClick={selectedView === 'Prompts' ? handleSelectPrompt : handleSelectCollection}
          onAddClick={selectedView === 'Prompts' ? handleAddPrompt : handleAddCollection}
        />
        <main className={styles.mainContent}>
          {loading ? (
            <Spinner />
          ) : (
          <>
            {renderContent()}
          </>
          )}
        </main>
      </div>
      <Modal isOpen={isPromptModalOpen} onClose={handleModalClose}>
        <PromptForm onSubmit={handlePromptSubmit} initialData={isEditing ? selectedPrompt : {}} errorMessage={errorMessage}/>
      </Modal>
      <Modal isOpen={isCollectionModalOpen} onClose={handleModalClose}>
        <CollectionForm onSubmit={handleCollectionSubmit} errorMessage={errorMessage}/>
      </Modal>
    </div>
  );
};

export default Layout;
