// App.tsx
import React, { useState } from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainMenu from './Client/Components/MainMenu/MainMenu';
import GameContainer from './Client/Components/GameContainer/GameContainer';

const App: React.FC = () => {
  const [currentGame, setCurrentGame] = useState({
    gameId: '',
    joinCode: '',
  });

  const handleGameCreated = (gameId: string, joinCode: string) => {
    setCurrentGame({
      gameId,
      joinCode,
    });
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainMenu onGameCreated={handleGameCreated} />} />
        <Route path="/game/:gameId" element={<GameContainer currentGame={currentGame} />} />
      </Routes>
    </Router>
  );
};

export default App;
