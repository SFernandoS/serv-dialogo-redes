// Login.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';
import { set } from 'mongoose';
import { useState, useEffect } from 'react';


const Home = () => {
    // get all chats from backend
    const [users, setUsers] = useState([]);
    const [userName, setUserName] = useState('');
    const navigate = useNavigate();

    const getChats = async () => {
        try {
            const response = await fetch('http://localhost:8000/users/users/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                console.log('Users retrieved successfully');
                const data = await response.json();
                console.log(data);
                setUsers(data);
            } else {
                const data = await response.json();
                console.error('Users retrieval failed:', data.error);
            }
        } catch (error) {
            console.error('Error during users retrieval:', error);
        }
    }
        useEffect(() => {
            getChats();
        }, []);

        const redirectToChat = () => {
            navigate('/chat');
        }

     // create simple chats home screen with a list of chats and the selected chat opened

        return (
            <div className="chat-container">
                <h2 className="titulo">Chats</h2>
                <div className="chat-list">
                    {/* list of chats */}
                    {users.map(user => {
                        return (
                            <div key={user.id} className={"chat-item"} onClick={redirectToChat}>
                                <div className="chat-item-img">
                                    <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" className='img' />
                                </div>
                                <div className="chat-item-info">
                                    <div className="chat-item-info-header">
                                        <h4>{user.email}</h4>
                                    </div>
                                    <div className="chat-item-info-body">
                                        <p>Olá, tudo bem?</p>
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
