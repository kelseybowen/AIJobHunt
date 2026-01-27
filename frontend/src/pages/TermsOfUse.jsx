import React from 'react';
import LegalLayout from '../components/LegalLayout';

const TermsOfUse = () => {
  return (
    <LegalLayout title="Terms of Use" lastUpdated="January 26, 2026">
      <h3>1. Acceptance of Terms</h3>
      <p>By using this application, you agree to these terms and all applicable laws.</p>

      <h3>2. Use License</h3>
      <p>Permission is granted for personal, non-commercial use. You may not reverse engineer the software or use it for unlawful purposes.</p>

      <h3>3. Disclaimer of AI Accuracy</h3>
      <p><strong>The information provided is for informational purposes only.</strong> We do not guarantee the accuracy of AI-generated content or specific employment outcomes.</p>

      <h3>4. Limitations</h3>
      <p>The developers are not liable for any damages arising from the use of this project.</p>
    </LegalLayout>
  );
};

export default TermsOfUse;