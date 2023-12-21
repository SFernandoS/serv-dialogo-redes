// Login.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';
import { useState, useEffect } from 'react';


const Home = () => {
    // get all chats from backend
    const [topics, setTopics] = useState([]);
    const [userName, setUserName] = useState('');
    const navigate = useNavigate();

    const getChats = async () => {
        try {
            const response = await fetch('http://localhost:8000/topics/topics/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                console.log('topics retrieved successfully');
                const data = await response.json();
                console.log(data);
                setTopics(data);
            } else {
                const data = await response.json();
                console.error('topics retrieval failed:', data.error);
            }
        } catch (error) {
            console.error('Error during topics retrieval:', error);
        }
    }
        useEffect(() => {
            getChats();
        }, []);

        const redirectToChat = (userId, topicId) => {
            navigate(`/chat/${userId}/${topicId}`);
        }

     // create simple chats home screen with a list of chats and the selected chat opened

        return (
            <div className="chat-container">
                <h2 className="titulo">Chats</h2>
                <div className="chat-list">
                    {/* list of chats */}
                    {topics.map(topic => {
                        return (
                            <div key={topic.id} className={"chat-item"} onClick={() => {redirectToChat(userId, topicId)}}>
                                <div className="chat-item-img">
                                    <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" className='img' />
                                </div>
                                <div className="chat-item-info">
                                    <div className="chat-item-info-header">
                                        <h4>{topic.name}</h4>
                                    </div>
                                    <div className="chat-item-info-body">
                                        <p>{topics.length}</p>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    };


export default Home;
