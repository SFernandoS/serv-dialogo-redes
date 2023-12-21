import React, { useEffect, useRef, useState } from "react";
import io from "socket.io-client";
import SimplePeer from "simple-peer";
import { useParams } from "react-router-dom";

const Chat = () => {
    const userId = useParams().userId;
    const topicId = useParams().topicId;
    const socket = io(`http://localhost:8000/ws/topic/${userId}/${topicId}}`);
    const localVideoRef = useRef();
    const remoteVideoRef = useRef();
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');
    const [peer, setPeer] = useState(null);
    const [localStream, setLocalStream] = useState(null);
    const [remoteStream, setRemoteStream] = useState(null);

    useEffect(() => {
        const handleResponse = (data) => {
            console.log(socket.id);
            setResponse(data);
        };

        socket.on("response", handleResponse);

        return () => {
            if (peer) {
                peer.destroy();
            }
            if (localStream) {
                localStream.getTracks().forEach((track) => track.stop());
            }
            // Remove the event listener when the component unmounts
            socket.off("response", handleResponse);
        };
    }, [peer, localStream]); // Add 'response' to the dependencies if needed

    const startVideoChat = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            setLocalStream(stream);
            localVideoRef.current.srcObject = stream;

            const newPeer = new SimplePeer({ initiator: false, stream });

            newPeer.on("signal", (data) => {
                socket.emit("video_answer", data);
            });

            newPeer.on("stream", (remoteStream) => {
                setRemoteStream(remoteStream);
                remoteVideoRef.current.srcObject = remoteStream;
            });

            socket.on("video_offer", (data) => {
                newPeer.signal(data);
            });

            socket.on("ice_candidate", (data) => {
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

    const sendChatMessage = (message) => {
        // send chat message
        socket.emit("chat_message", message);
    };

    return (
        <div className="chat-container">
            <h1 className="title">Video Chat</h1>
            <video ref={localVideoRef} autoPlay muted></video>
            <video ref={remoteVideoRef} autoPlay></video>
            <button onClick={startVideoChat}>Start Video Chat</button>
            <button onClick={stopVideoChat}>Stop Video Chat</button>
            <div className="text-chat">
                <h1 className="title">Text Chat</h1>
                <div className="chat-box">
                    <div className="chat-messages"></div>
                    <form
                        className="chat-form"
                        onSubmit={(e) => {
                            e.preventDefault();
                            sendChatMessage(message);
                            setMessage('');
                        }}
                    >
                        <input type="text" placeholder="Type your message..." value={message} onChange={(e) => setMessage(e.target.value)} />
                        <button type="submit">Send</button>
                    </form>
                    <div className="chat-messages">
                        <p className="chat-message">{response}</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Chat;
