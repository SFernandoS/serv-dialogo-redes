import React, { useEffect, useRef } from "react";
import io from "socket.io-client";
import SimplePeer from "simple-peer";

const socket = io("http://localhost:8000/ws");

const Chat = () => {
    const localVideoRef = useRef();
    const remoteVideoRef = useRef();
    let peer;
    let localStream;

    useEffect(() => {
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

    return (
        <div className="chat-container">
            <h1 className="title">Video Chat</h1>
            <video ref={localVideoRef} autoPlay muted></video>
            <video ref={remoteVideoRef} autoPlay></video>
            <button onClick={startVideoChat}>Start Video Chat</button>
            <button onClick={stopVideoChat}>Stop Video Chat</button>
        </div>
    );
}

export default Chat;
