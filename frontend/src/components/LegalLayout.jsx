import React from 'react';

const LegalLayout = ({ title, lastUpdated, children }) => {
  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1>{title}</h1>
        <p><strong>Last Updated:</strong> {lastUpdated}</p>
      </header>
      <hr style={styles.divider} />
      <main style={styles.content}>
        {children}
      </main>
      <footer style={styles.footer}>
        <p>This is a student project developed for educational purposes.</p>
      </footer>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '40px 20px',
    lineHeight: '1.6',
    color: '#333',
    fontFamily: 'sans-serif'
  },
  header: {
    marginBottom: '20px'
  },
  divider: {
    border: '0',
    borderTop: '1px solid #eee',
    margin: '20px 0'
  },
  content: {
    textAlign: 'left'
  },
  footer: {
    marginTop: '40px',
    fontSize: '0.9rem',
    color: '#777',
    textAlign: 'center'
  }
};

export default LegalLayout;