import React, { useEffect, useRef, useState } from "react";
import io from "socket.io-client";
import SimplePeer from "simple-peer";
import { set } from "mongoose";

const socket = io("http://localhost:8000/ws");

const Chat = () => {
    const localVideoRef = useRef();
    const remoteVideoRef = useRef();
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');
    let peer;
    let localStream;

    useEffect(() => {
        socket.on("response", () => {
            console.log(socket.id);
            setResponse(response);
        });
        return () => {
            if (peer) {
                peer.destroy();
            }
            if (localStream) {
                localStream.getTracks().forEach((track) => track.stop());
            }
        };
    }, []);

    const startVideoChat = async () => {
        try {
            localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            localVideoRef.current.srcObject = localStream;

            peer = new SimplePeer({ initiator: false, stream: localStream });

            peer.on("signal", (data) => {
                socket.emit("video_answer", data);
            });

            peer.on("stream", (remoteStream) => {
                remoteVideoRef.current.srcObject = remoteStream;
            });

            socket.on("video_offer", (data) => {
                peer.signal(data);
            });

            socket.on("ice_candidate", (data) => {
                peer.signal(data);
            });
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
        localVideoRef.current.srcObject = null;
        remoteVideoRef.current.srcObject = null;
    };

    const sendChatMessage = (message) => {
        // send chat message
        socket.emit("chat_message", message);
    }

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
                    <form className="chat-form">
                        <input type="text" placeholder="Type your message..." value={message} onChange={(e) => setMessage(e.target.value)}/>
                        <button type="submit" onClick={sendChatMessage(message)}>Send</button>
                    </form>
                    <div className="chat-messages">
                        <p className="chat-message">{response}</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Chat;
