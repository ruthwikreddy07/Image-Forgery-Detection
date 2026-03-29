import React, { useState } from 'react';
import { LuMicroscope as Microscope } from 'react-icons/lu';
import './App.css';
import ImageUploader from './components/ImageUploader';
import ResultsViewer from './components/ResultsViewer';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [originalImage, setOriginalImage] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = async (file, previewDataUrl) => {
    setIsLoading(true);
    setOriginalImage(previewDataUrl);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/detect-forgery', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const data = await response.json();
      
      if (data.error) {
         throw new Error(data.error);
      }
      
      setResult(data);
    } catch (err) {
      console.error("Error during upload:", err);
      setError(err.message || 'Failed to connect to the analysis server. Make sure it is running.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setOriginalImage(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-content fade-in">
          <Microscope className="title-icon" strokeWidth={1.5} />
          <h1>
             <span className="gradient-text">Advanced</span> Forgery Detection
          </h1>
          <p>
            Upload an image to scan for copy-move tampering using AI-powered ORB feature matching and descriptor analysis.
          </p>
        </div>
      </header>

      <main className="main-content">
        {error && (
          <div className="glass-panel" style={{ padding: '1.5rem', border: '1px solid rgba(255, 59, 48, 0.4)', background: 'rgba(255, 59, 48, 0.1)', color: '#ff453a', maxWidth: '800px', width: '100%', textAlign: 'center' }}>
            <strong>Analysis Failed:</strong> {error}
          </div>
        )}

        {!result && !isLoading && (
          <ImageUploader onUpload={handleUpload} isLoading={isLoading} />
        )}

        {isLoading && (
          <div className="loader-container fade-in">
             <div className="spinner"></div>
             <h2 className="gradient-text animate-pulse">Running ORB Detection...</h2>
             <p style={{ color: 'var(--text-secondary)' }}>Extracting features & matching descriptors</p>
          </div>
        )}

        {result && !isLoading && (
          <ResultsViewer 
            originalImage={originalImage} 
            result={result} 
            onReset={handleReset} 
          />
        )}
      </main>
    </div>
  );
}

export default App;
