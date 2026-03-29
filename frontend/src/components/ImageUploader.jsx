import React, { useState, useCallback } from 'react';
import { LuCloudUpload as UploadCloud, LuImage as ImageIcon, LuX as X } from 'react-icons/lu';

const ImageUploader = ({ onUpload, isLoading }) => {
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  function processFile(file) {
    // Only accept images
    if (!file.type.match('image.*')) {
      alert('Please upload an image file (JPEG, PNG).');
      return;
    }
    
    setSelectedFile(file);
    
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(file);
  }

  const clearFile = (e) => {
    e.stopPropagation();
    setSelectedFile(null);
    setPreview(null);
  };

  const handleProcessClick = (e) => {
    e.stopPropagation();
    if (selectedFile) {
      onUpload(selectedFile, preview);
    }
  };

  return (
    <div className="upload-section fade-in">
      <div 
        className={`uploader-box glass-panel ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-upload').click()}
      >
        <input 
          id="file-upload" 
          type="file" 
          accept="image/*" 
          onChange={handleChange} 
          style={{ display: 'none' }} 
        />
        
        {!preview ? (
          <>
            <UploadCloud className="upload-icon" />
            <div className="uploader-text">Drag & drop your image here</div>
            <div className="uploader-subtext">or click to browse from your device</div>
          </>
        ) : (
          <div className="file-selected">
            <img src={preview} alt="Upload preview" className="file-preview" />
            <div className="file-actions">
              <button 
                type="button" 
                className="btn-secondary" 
                onClick={clearFile}
                disabled={isLoading}
              >
                <X size={18} style={{ marginRight: '8px', verticalAlign: 'middle' }}/>
                Clear Selection
              </button>
              <button 
                type="button" 
                className="btn-primary flex items-center gap-2" 
                onClick={handleProcessClick}
                disabled={isLoading}
              >
                {isLoading ? (
                  'Analyzing Image...'
                ) : (
                  <>
                    <ImageIcon size={18} style={{ marginRight: '8px', verticalAlign: 'middle' }}/>
                    Analyze Image
                  </>
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUploader;
