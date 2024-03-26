// GameContainer.tsx
import React, { useState } from 'react';
import './GameContainer.css'; // Import the CSS file
import WebSocketComponent from '../WebSocket/WebSocketComponent';
import Referee from '../Referee/Referee';
import Camera from '../Camera/Camera';

interface GameContainerProps {
    // gameId: string;
    // joinCode:string;
    currentGame: {
        gameId: string,
        joinCode: string
    }
}

const GameContainer: React.FC<GameContainerProps> = ({ currentGame }) => {
    const [allowCamera, setAllowCamera] = useState<boolean>(false);
    // const [gameState, setGameState] = useState<any>({}); // Update with your actual game state type

    const toggleCamera = () => {
        setAllowCamera((prev) => !prev);
    };

    return (
        <div className="game-container">
            <div className="game-content">
                <Referee gameID={currentGame.gameId} />
            </div>
            <WebSocketComponent gameID={currentGame.gameId} onMessage={(message) => console.log(message)} />
            {allowCamera && (
                <div className="camera-container">
                    <Camera />
                    <button className="camera-btn" onClick={toggleCamera}>
                        Turn off camera
                    </button>
                </div>
            )}

            {!allowCamera && (
                <button className="camera-btn" onClick={toggleCamera}>
                    Turn on camera
                </button>
            )}

            <p className="game-id">Game ID: {currentGame.gameId}</p>
            <p className="join-code">Join Code: {currentGame.joinCode}</p>
        </div>
    );
};

export default GameContainer;
