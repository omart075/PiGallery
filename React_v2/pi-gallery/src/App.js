import './App.css';
import ImageSwapper from './image_handler';
import CustomParticles from './particle_handler'
import React, { useEffect, useState } from "react";

function App() {
  const [viewGallery, setViewGallery] = useState(true);
  
  return (
    <div className="App" onClick={() => setViewGallery(prev => !prev)}>
      <header className="App-header">
        { viewGallery && <ImageSwapper/> }
        { !viewGallery && <CustomParticles/> }
      </header>
    </div>
  );
}

export default App;
