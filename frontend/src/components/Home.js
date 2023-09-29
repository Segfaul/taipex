import React from 'react';

const Home = () => {
  return (
    <div className='home-preview'>
      <p className='home-description'>
        A microservice for managing tasks 
        and ensuring efficient communication through the data bus. 
        TaskFlow has background processing of tasks and also has automatic 
        deletion and prioritization system.
      </p>
      <img className='home-pic' src={require('../assets/taipex_logo.png')} alt="Taipex Logo" />
    </div>
  );
};

export default Home;