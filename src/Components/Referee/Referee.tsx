import { useEffect, useRef, useState } from "react";
import { Piece, Position } from "../../models";
import { Board } from "../../models/Board";
import { Pawn } from "../../models/Pawn";
import { PieceType, TeamType } from "../../Types";
import { initialBoard } from "../../Constents";
import Chessboard from "../PlayBoard/PlayBoard";
import "./Referee.css"

export default function Referee({ gameID }: { gameID: string }) {

    const [board, setBoard] = useState<Board>(initialBoard.clone());
    const [promotionPawn, setPromotionPawn] = useState<Piece>();
    const modalRef = useRef<HTMLDivElement>(null);
    const checkmateModalRef = useRef<HTMLDivElement>(null);
    // Establish WebSocket connection
    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/${gameID}`);

    useEffect(() => {

        const handleWebSocketMessage = (event: MessageEvent) => {
            // Handle message received from the server
            const message = JSON.parse(event.data);
            // Update the game state based on the message received
            // Might need to define a protocol for the message
            // For example, { type: 'move', payload: { playedPiece, destination } }

            if (message.type === 'move') {
                const { playedPiece, destination } = message.payload;
                playMove(playedPiece, destination);
            }

            // event listener for WebSocket messages
            socket.addEventListener('message', handleWebSocketMessage);

            //Cleanup function
            return () => {
                socket.removeEventListener('message', handleWebSocketMessage);
                socket.close(); // close the socket connection
            };
        };

    }, [gameID]);


    // function playMove(playedPiece: Piece, destination: Position): boolean {

    //     // If the playing piece doesn't have any moves return
    //     if (playedPiece.possibleMoves === undefined) return false;


    //     // Setting turn logic.
    //     // Prevent the inactive team from playing
    //     if (playedPiece.team === TeamType.TEAMMATE
    //         && board.totalTurns % 2 !== 1) return false;
    //     if (playedPiece.team === TeamType.OPPONENT
    //         && board.totalTurns % 2 !== 0) return false;

    //     let playedMoveIsValid = false;

    //     const validMove = playedPiece.possibleMoves?.some(m => m.samePosition(destination));

    //     if (!validMove) return false;

    //     const enPassantMove = isEnPassantMove(
    //         playedPiece.position,
    //         destination,
    //         playedPiece.type,
    //         playedPiece.team
    //     );

    //     // playMove modifies the board thus we
    //     // need to call setBoard
    //     setBoard(() => {
    //         const clonedBoard = board.clone();
    //         clonedBoard.totalTurns += 1;
    //         // Playing the move
    //         playedMoveIsValid = clonedBoard.playMove(enPassantMove,
    //             validMove, playedPiece,
    //             destination);

    //         if (clonedBoard.winningTeam !== undefined) {
    //             checkmateModalRef.current?.classList.remove("hidden");
    //         }

    //         return clonedBoard;
    //     });



    //     //  promoting a pawn
    //     let promotionRow = (playedPiece.team === TeamType.TEAMMATE) ? 7 : 0;

    //     if (destination.y === promotionRow && playedPiece.isPawn) {
    //         modalRef.current?.classList.remove("hidden");
    //         setPromotionPawn(() => {
    //             const clonedPlayedPiece = playedPiece.clone();
    //             clonedPlayedPiece.position = destination.clone();
    //             return clonedPlayedPiece;
    //         });
    //     }
    //     // Send the move to the server via WebSocket
    //     const message = JSON.stringify({ type: 'move', payload: { playedPiece, destination } });
    //     socket.send(message);

    //     return playedMoveIsValid;
    // };

    async function playMove(playedPiece: Piece, destination: Position): Promise<boolean> {

        // If the playing piece doesn't have any moves, return false
        if (playedPiece.possibleMoves === undefined) return false;

        // Setting turn logic. Prevent the inactive team from playing
        if (
            (playedPiece.team === TeamType.TEAMMATE && board.totalTurns % 2 !== 1) ||
            (playedPiece.team === TeamType.OPPONENT && board.totalTurns % 2 !== 0)
        ) {
            return false;
        }

        const validMove = playedPiece.possibleMoves?.some(m => m.samePosition(destination));

        if (!validMove) return false;

        const enPassantMove = isEnPassantMove(
            playedPiece.position,
            destination,
            playedPiece.type,
            playedPiece.team
        );

        // playMove modifies the board, thus we need to call setBoard
        const clonedBoard = board.clone();
        clonedBoard.totalTurns += 1;

        // Playing the move
        let playedMoveIsValid = clonedBoard.playMove(enPassantMove, validMove, playedPiece, destination);

        if (clonedBoard.winningTeam !== undefined) {
            checkmateModalRef.current?.classList.remove("hidden");
        }

        setBoard(() => clonedBoard);

        // Promoting a pawn
        const promotionRow = (playedPiece.team === TeamType.TEAMMATE) ? 7 : 0;

        if (destination.y === promotionRow && playedPiece.isPawn) {
            modalRef.current?.classList.remove("hidden");
            setPromotionPawn(() => {
                const clonedPlayedPiece = playedPiece.clone();
                clonedPlayedPiece.position = destination.clone();
                return clonedPlayedPiece;
            });
        }

        // Send the move to the server via WebSocket
        const message = JSON.stringify({ type: 'move', payload: { playedPiece, destination, clonedBoard } });
        socket.send(message);

        // Send a request to the server for move validation
        const validationResponse = await validateMoveOnServer(playedPiece, destination, clonedBoard);
        if (validationResponse) { // if this is true, the server validate the move.
            return playedMoveIsValid;  // if this is true, the front validate the move.
        }

        return false; // move is not valid.
    };


    // Function to send a request to the server for move validation
    // async function validateMoveOnServer(playedPiece: Piece, destination: Position): Promise<boolean> {
    async function validateMoveOnServer(playedPiece: Piece, destination: Position, clonedBoard: Board) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/make_move/${gameID}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    payload: {
                        playedPiece,
                        destination: { x: destination.x, y: destination.y },
                        clonedBoard
                    }
                }),
            });

            const result = await response.json();

            return Boolean(result.isValidMove);
        } catch (error) {
            console.error('Error validating move on server:', error);
            return false;
        }
    };



    function isEnPassantMove(
        initialPosition: Position,
        desiredPosition: Position,
        type: PieceType,
        team: TeamType
    ) {
        const pawnDirection = team === TeamType.TEAMMATE ? 1 : -1;

        if (type === PieceType.PAWN) {
            if (
                (desiredPosition.x - initialPosition.x === -1 ||
                    desiredPosition.x - initialPosition.x === 1) &&
                desiredPosition.y - initialPosition.y === pawnDirection
            ) {
                const piece = board.pieces.find(
                    (p) =>
                        p.position.x === desiredPosition.x &&
                        p.position.y === desiredPosition.y - pawnDirection &&
                        p.isPawn &&
                        (p as Pawn).enPassant
                );
                if (piece) {
                    return true;
                }
            }
        }

        return false;
    };


    function promotePawn(pieceType: PieceType) {
        if (promotionPawn === undefined) {
            return;
        }

        setBoard(() => {
            const clonedBoard = board.clone();
            clonedBoard.pieces = clonedBoard.pieces.reduce((results, piece) => {
                if (piece.samePiecePosition(promotionPawn)) {
                    results.push(new Piece(piece.position.clone(), pieceType,
                        piece.team, true));
                } else {
                    results.push(piece);
                }
                return results;
            }, [] as Piece[]);

            clonedBoard.calculateAllMoves();

            return clonedBoard;
        })

        modalRef.current?.classList.add("hidden");
    };

    function promotionTeamType() {
        return (promotionPawn?.team === TeamType.TEAMMATE) ? "w" : "b";
    };

    function restartGame() {
        checkmateModalRef.current?.classList.add("hidden");
        setBoard(initialBoard.clone());
    };

    return (
        <>
            <p style={{ color: "white", fontSize: "24px", textAlign: "center" }}>Total turns: {board.totalTurns}</p>
            <div className="modal hidden" ref={modalRef}>
                <div className="modal-body">
                    <img onClick={() => promotePawn(PieceType.ROOK)} src={`/assets/images/rook_${promotionTeamType()}.png`} />
                    <img onClick={() => promotePawn(PieceType.BISHOP)} src={`/assets/images/bishop_${promotionTeamType()}.png`} />
                    <img onClick={() => promotePawn(PieceType.KNIGHT)} src={`/assets/images/knight_${promotionTeamType()}.png`} />
                    <img onClick={() => promotePawn(PieceType.QUEEN)} src={`/assets/images/queen_${promotionTeamType()}.png`} />
                </div>
            </div>
            <div className="modal hidden" ref={checkmateModalRef}>
                <div className="modal-body">
                    <div className="checkmate-body">
                        {board.winningTeam && (<span>The winning team is {board.winningTeam === TeamType.TEAMMATE ? "white" : "black"}!</span>)}
                        <button onClick={restartGame}>Play again</button>
                    </div>
                </div>
            </div>
            <Chessboard playMove={playMove}
                pieces={board.pieces} />
        </>
    )
};