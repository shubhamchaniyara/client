// import React, { useState } from 'react';
// import './App.css';

// function App() {
//   const [imageUrl, setImageUrl] = useState('');
//   const [question, setQuestion] = useState('');
//   const [result, setResult] = useState(null);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setResult(null);
//     const response = await fetch('http://localhost:5000/predict', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({
//         image_url: imageUrl,
//         question: question,
//       }),
//     });

//     const data = await response.json();
//     setResult(data);
//   };

//   return (
//     <div className="app-container">
//       <div className="form-container">
//         <h1 className="app-title">Visual Question Answering</h1>

//         <form onSubmit={handleSubmit} className="question-form">
//           <div className="form-group">
//             <label className="form-label">Image URL:</label>
//             <input
//               type="text"
//               value={imageUrl}
//               onChange={(e) => setImageUrl(e.target.value)}
//               required
//               className="form-input"
//               placeholder="Enter Image URL"
//             />
//           </div>
//           <div className="form-group">
//             <label className="form-label">Question:</label>
//             <input
//               type="text"
//               value={question}
//               onChange={(e) => setQuestion(e.target.value)}
//               required
//               className="form-input"
//               placeholder="Ask your question"
//             />
//           </div>
//           <button type="submit" className="submit-button">Submit</button>

//           {result && (
//             <div className="result-container">
//               <h2 className="result-title">Answer: {result.answer}</h2>
//               <p className="result-info">{result.info}</p>
//             </div>
//           )}
//         </form>
//       </div>

//       {/* Image Display */}
//       {imageUrl && (
//         <div className="image-container">
//           <img src={imageUrl} alt="Submitted" className="displayed-image" />
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

import React, { useState } from 'react';
import './App.css';

function App() {
  const [imageUrl, setImageUrl] = useState(''); // For handling image URL input
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [imageFile, setImageFile] = useState(null); // For handling uploaded image files
  const [useUrl, setUseUrl] = useState(false); // Boolean flag to switch between URL and file upload

  // Handle image upload
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file); // Store the file for the fetch request
      setImageUrl('');    // Reset image URL input if a file is uploaded
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(null);

    const formData = new FormData(); // Create a FormData object to hold file data

    if (useUrl) {
      formData.append('image_url', imageUrl); // Use the entered image URL
    } else if (imageFile) {
      formData.append('image', imageFile);    // Append the uploaded image file
    }

    formData.append('question', question);    // Append the question

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        body: formData, // Send the FormData object with file and question
      });

      if (!response.ok) {
        throw new Error('Network response was not OK');
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error during fetch:', error);
    }
  };

  return (
    <div className="app-container">
      <div className="form-container">
        <h1 className="app-title">Visual Question Answering</h1>

        <form onSubmit={handleSubmit} className="question-form">
          {/* Radio buttons to switch between URL and file upload */}
          <div className="form-group">
            <label>
              <input
                type="radio"
                value="url"
                checked={useUrl}
                onChange={() => setUseUrl(true)}
              />
              Enter Image URL
            </label>
            <label>
              <input
                type="radio"
                value="file"
                checked={!useUrl}
                onChange={() => setUseUrl(false)}
              />
              Upload Image
            </label>
          </div>

          {/* Conditionally render based on the selection */}
          {useUrl ? (
            <div className="form-group">
              <label className="form-label">Image URL:</label>
              <input
                type="text"
                value={imageUrl}
                onChange={(e) => setImageUrl(e.target.value)}
                required
                className="form-input"
                placeholder="Enter Image URL"
              />
            </div>
          ) : (
            <div className="form-group">
              <label className="form-label">Upload Image:</label>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                required
                className="form-input"
              />
            </div>
          )}

          <div className="form-group">
            <label className="form-label">Question:</label>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              required
              className="form-input"
              placeholder="Ask your question"
            />
          </div>

          <button type="submit" className="submit-button">Submit</button>

          {result && (
            <div className="result-container">
              <h2 className="result-title">Answer: {result.answer}</h2>
              <p className="result-info">{result.info}</p>
            </div>
          )}
        </form>
      </div>

      {/* Image Display */}
      {imageUrl && useUrl && (
        <div className="image-container">
          <img src={imageUrl} alt="Uploaded or Entered" className="displayed-image" />
        </div>
      )}

      {imageFile && !useUrl && (
        <div className="image-container">
          <img src={URL.createObjectURL(imageFile)} alt="Uploaded" className="displayed-image" />
        </div>
      )}
    </div>
  );
}

export default App;
