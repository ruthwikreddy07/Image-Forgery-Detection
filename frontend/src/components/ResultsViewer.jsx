import React from 'react';
import { LuShieldAlert as ShieldAlert, LuShieldCheck as ShieldCheck, LuArrowLeft as ArrowLeft, LuDownload as Download } from 'react-icons/lu';

const ResultsViewer = ({ originalImage, result, onReset }) => {
  const isForged = result.is_forged;
  
  return (
    <div className="results-container fade-in">
      <div className="glass-panel results-header">
        <button className="btn-secondary" onClick={onReset} style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 16px' }}>
          <ArrowLeft size={18} />
          New Scan
        </button>
        
        <div className={`status-badge ${isForged ? 'forged' : 'authentic'}`}>
          {isForged ? (
            <>
              <ShieldAlert className="icon" />
              <span>Forgery Detected</span>
            </>
          ) : (
            <>
              <ShieldCheck className="icon" />
              <span>No Forgery Detected</span>
            </>
          )}
        </div>
        
        <a 
          href={result.processed_image} 
          download="forgery_report.jpg" 
          className="btn-primary"
          style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 16px' }}
        >
          <Download size={18} />
          Export
        </a>
      </div>

      <div className="glass-panel stats-panel">
        <div style={{ marginTop: '-1.5rem', background: isForged ? 'rgba(255, 59, 48, 0.1)' : 'rgba(48, 209, 88, 0.1)', padding: '1rem', borderRadius: '12px', display: 'inline-block', marginBottom: '2rem', border: `1px solid ${isForged ? 'rgba(255, 59, 48, 0.3)' : 'rgba(48, 209, 88, 0.3)'}` }}>
          {isForged ? (
            <h2 style={{ color: '#ff453a', margin: 0 }}>High Risk: Duplicate Regions Found</h2>
          ) : (
             <h2 style={{ color: '#32d74b', margin: 0 }}>Low Risk: Document Appears Authentic</h2>
          )}
        </div>
        
        <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', flexWrap: 'wrap' }}>
          <div className="stat-box">
            <span className="stat-value">{result.forgery_count}</span>
            <span className="stat-label">Matched Keypoints</span>
          </div>
          <div className="stat-box">
             <span className="stat-value" style={{ color: isForged ? '#ff453a' : '#32d74b' }}>
                {isForged ? 'FAIL' : 'PASS'}
             </span>
             <span className="stat-label">System Verdict</span>
          </div>
          <div className="stat-box">
             <span className="stat-value">ORB</span>
             <span className="stat-label">Detection Algorithm</span>
          </div>
        </div>
      </div>

      <div className="glass-panel results-content">
        <div className="image-panel">
          <h3>Original Upload</h3>
          <img src={originalImage} alt="Original" />
        </div>
        
        <div className="image-panel">
          <h3>
            Analysis Overlay
            {isForged && <span style={{ fontSize: '0.8REM', color: 'var(--text-secondary)', background: 'rgba(255,255,255,0.1)', padding: '2px 8px', borderRadius: '4px', marginLeft: 'auto' }}>Matched points linked</span>}
          </h3>
          <img src={result.processed_image} alt="Processed Forgery Map" />
        </div>
      </div>
    </div>
  );
};

export default ResultsViewer;
