import React, { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import SimplePeer from "simple-peer";

const Chat = () => {
    const { userId, topicId } = useParams();
    const websocket = useRef(null);
    const localVideoRef = useRef();
    const remoteVideoRef = useRef();
    const [message, setMessage] = useState('');
    const [chatLog, setChatLog] = useState([]);
    const [peer, setPeer] = useState(null);
    const [localStream, setLocalStream] = useState(null);
    const [remoteStream, setRemoteStream] = useState(null);

    const openDialog = () => {
        setShowDialog(true);
    };
    
    const closeDialog = () => {
        setShowDialog(false);
    };

    useEffect(() => {
        websocket.current = new WebSocket(`ws://localhost:8000/ws/topic/${userId}/${topicId}`);
        websocket.current.onmessage = event => {
            try {
                const data = JSON.parse(event.data);
                setChatLog(prevLog => [...prevLog, `Recebido: ${data.message}`]);
            } catch (error) {
                console.error("Erro ao analisar a mensagem do WebSocket:", error);
            }
        };
        return () => {
            if (websocket.current) websocket.current.close();
        };
    }, [userId, topicId]);

    const sendChatMessage = () => {
        if (websocket.current && message.trim()) {
            const messageData = JSON.stringify({ message });
            websocket.current.send(messageData);
            setChatLog(prevLog => [...prevLog, `Você: ${message}`]);
            setMessage('');
        }
    };

    const startVideoChat = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            setLocalStream(stream);
            localVideoRef.current.srcObject = stream;

            const newPeer = new SimplePeer({ initiator: false, stream });

            newPeer.on("signal", (data) => {
                websocket.current.emit("video_answer", data);
            });

            newPeer.on("stream", (remoteStream) => {
                setRemoteStream(remoteStream);
                remoteVideoRef.current.srcObject = remoteStream;
            });

            websocket.current.on("video_offer", (data) => {
                newPeer.signal(data);
            });

            websocket.current.on("ice_candidate", (data) => {
                newPeer.signal(data);
            });

            setPeer(newPeer);
        } catch (error) {
            console.error("Error accessing media devices:", error);
        }
    };

    const stopVideoChat = () => {
        if (peer) {
            peer.destroy();
        }
        if (localStream) {
            localStream.getTracks().forEach((track) => track.stop());
        }
        setLocalStream(null);
        setRemoteStream(null);
        localVideoRef.current.srcObject = null;
        remoteVideoRef.current.srcObject = null;
    };

    return (
        <div className="chat-container">
            {/* Área de Vídeo */}
            <div className="video-chat">
                <video ref={localVideoRef} autoPlay muted></video>
                <video ref={remoteVideoRef} autoPlay></video>
                <button onClick={startVideoChat}>Start Video Chat</button>
                <button onClick={stopVideoChat}>Stop Video Chat</button>
            </div>

            {/* Área de Chat de Texto */}
            <div className="text-chat">
                <h2>Text Chat</h2>
                <div className="chat-messages-box">
                    {chatLog.map((msg, index) => (
                        <p key={index} className="chat-message">{msg}</p>
                    ))}
                </div>
                <form className="chat-form" onSubmit={e => {
                    e.preventDefault();
                    sendChatMessage();
                }}>
                    <input
                        type="text"
                        placeholder="Type your message..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                    />
                    <button type="submit">Send</button>
                </form>
            </div>

            {showDialog && (
                <div className="dialog-box">
                    <p>Mensagem enviada com sucesso!</p>
                    <button onClick={closeDialog}>Fechar</button>
                </div>
            )}
        </div>
    );
};

export default Chat;