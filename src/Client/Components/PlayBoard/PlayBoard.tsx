import { useRef, useState, useEffect } from "react";
import "./PlayBoard.css";

import Tile from "../Tile/Tile";
import { Piece, Position } from "../../models";
import { GRID_SIZE, HORIZONTAL_AXIS, VERTICAL_AXIS } from "../../../Constents";

interface Props {
  playMove: (piece: Piece, position: Position) => Promise<boolean>;
  pieces: Piece[];
  opponentMoves: { playedPiece: Piece; destination: Position }[];
}

export default function PlayBoard({ playMove, pieces, opponentMoves }: Props) {
  const [activePiece, setActivePiece] = useState<HTMLElement | null>(null);
  const [grabPosition, setGrabPosition] = useState<Position>(new Position(-1, -1));
  const chessboardRef = useRef<HTMLDivElement>(null);

  function grabPiece(e: React.MouseEvent) {
    const element = e.target as HTMLElement;
    const chessboard = chessboardRef.current;
    if (element.classList.contains("chess-piece") && chessboard) {
      const grabX = Math.floor((e.clientX - chessboard.offsetLeft) / GRID_SIZE);
      const grabY = Math.abs(Math.ceil((e.clientY - chessboard.offsetTop - 800) / GRID_SIZE));
      setGrabPosition(new Position(grabX, grabY));

      const x = e.clientX - GRID_SIZE / 2;
      const y = e.clientY - GRID_SIZE / 2;

      element.style.position = "absolute";
      element.style.left = `${x}px`;
      element.style.top = `${y}px`;

      setActivePiece(element);
    }
  }

  function movePiece(e: React.MouseEvent) {
    const chessboard = chessboardRef.current;
    if (activePiece && chessboard) {
      const minX = chessboard.offsetLeft - 25;
      const minY = chessboard.offsetTop - 25;
      const maxX = chessboard.offsetLeft + chessboard.clientWidth - 75;
      const maxY = chessboard.offsetTop + chessboard.clientHeight - 75;
      const x = e.clientX - 50;
      const y = e.clientY - 50;
      activePiece.style.position = "absolute";

      if (x < minX) {
        activePiece.style.left = `${minX}px`;
      } else if (x > maxX) {
        activePiece.style.left = `${maxX}px`;
      } else {
        activePiece.style.left = `${x}px`;
      }

      if (y < minY) {
        activePiece.style.top = `${minY}px`;
      } else if (y > maxY) {
        activePiece.style.top = `${maxY}px`;
      } else {
        activePiece.style.top = `${y}px`;
      }
    }
  }
  // Function to request the latest game state from the server
  async function requestLatestGameState() {
    try {
      // Send a request to the server to fetch the latest game state
      const response = await fetch('/get_latest_game_state');
      if (!response.ok) {
        throw new Error('Failed to fetch latest game state');
      }

      // Parse the response
      const gameState = await response.json();
      updateGameState(gameState);
      // Update the local game state with the received data
      // For example, update the 'pieces' and 'opponentMoves' state variables
    } catch (error) {
      console.error('Error fetching latest game state:', error);
    }
  }
  async function dropPiece(e: React.MouseEvent) {
    const chessboard = chessboardRef.current;
    if (activePiece && chessboard) {
      const x = Math.floor((e.clientX - chessboard.offsetLeft) / GRID_SIZE);
      const y = Math.abs(Math.ceil((e.clientY - chessboard.offsetTop - 800) / GRID_SIZE));

      const currentPiece = pieces.find((p) => p.samePosition(grabPosition));

      if (currentPiece) {
        const success = await playMove(currentPiece.clone(), new Position(x, y));

        if (!success) {
          activePiece.style.position = "relative";
          activePiece.style.removeProperty("top");
          activePiece.style.removeProperty("left");
        }

        if (success) {
          // Request the latest game state from the server after a successful move
          await requestLatestGameState();
        }
      }
      setActivePiece(null);
    }
  }




  let board = [];

  for (let j = VERTICAL_AXIS.length - 1; j >= 0; j--) {
    for (let i = 0; i < HORIZONTAL_AXIS.length; i++) {
      const number = j + i + 2;
      const piece = pieces.find((p) => p.samePosition(new Position(i, j)));

      let image = piece ? (`/${piece.image}`) : undefined;

      let currentPiece =
        activePiece != null
          ? pieces.find((p) => p.samePosition(grabPosition))
          : undefined;
      let highlight = currentPiece?.possibleMoves
        ? currentPiece.possibleMoves.some((p) => p.samePosition(new Position(i, j)))
        : false;

      const opponentMove = opponentMoves.find(
        (move) => move.destination.x === i && move.destination.y === j
      );

      if (opponentMove) {
        highlight = true;
        image = opponentMove.playedPiece.image;
      }

      board.push(
        <Tile
          key={`${j},${i}`}
          image={image}
          number={number}
          highlight={highlight}
        />
      );
    }
  }

  useEffect(() => {
    console.log('Opponent Moves:', opponentMoves);
  }, [opponentMoves]);

  return (
    <>
      <div
        onMouseMove={(e) => movePiece(e)}
        onMouseDown={(e) => grabPiece(e)}
        onMouseUp={(e) => dropPiece(e)}
        id="chessboard"
        ref={chessboardRef}
      >
        {board}
      </div>
    </>
  );
}


function updateGameState(gameState: any) {
  throw new Error("Function not implemented.");
}

