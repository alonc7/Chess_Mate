// App.js
import React, { useState } from 'react';
import './App.css'
import MainMenu from './Client/Components/MainMenu/MainMenu';
import GameContainer from './Client/Components/GameContainer/GameContainer';
const App: React.FC = () => {
  const [gameId, setGameId] = useState<string>('');

  const handleGameCreated = (newGameId: string) => {
    setGameId(newGameId);
  };

  return (
    <div>
      {!gameId ? (
        <MainMenu onGameCreated={handleGameCreated} />
      ) : (
        <GameContainer gameId={gameId} />
      )}
    </div>
  );
};

export default App;
