import React from 'react';
import LegalLayout from '../components/LegalLayout';

const PrivacyPolicy = () => {
  return (
    <LegalLayout title="Privacy Policy" lastUpdated="January 26, 2026">
      <h3>1. Information We Collect</h3>
      <ul>
        <li><strong>Account Information:</strong> Name, email address, and login credentials.</li>
        <li><strong>User Content:</strong> Resumes and job descriptions provided for analysis.</li>
        <li><strong>Usage Data:</strong> IP addresses and browser types.</li>
      </ul>

      <h3>2. How We Use Your Information</h3>
      <p>Your data is used specifically to facilitate AI-driven job searches, maintain application functionality, and provide support.</p>

      <h3>3. Data Sharing</h3>
      <p>We do not sell your personal data. Data may be processed via third-party AI APIs or stored in our database for application use.</p>

      <h3>4. Security</h3>
      <p>We implement industry-standard measures, but cannot guarantee 100% security for data transmitted over the internet.</p>
    </LegalLayout>
  );
};

export default PrivacyPolicy;