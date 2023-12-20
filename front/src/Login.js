// Login.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './Login.css';

const Login = () => {
    const navigate = useNavigate();
    const [username, setEmail] = useState('');
    const [password, setSenha] = useState('');

    const handleLogin = async (username, password) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        const response = await fetch('http://localhost:8000/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });
    
        if (response.ok) {
            const data = await response.json();
            const accessToken = data.access_token;
            // Save the access token in a secure way (e.g., localStorage) for future requests.
            localStorage.setItem('accessToken', accessToken);
            // Redirect the user to the home page.
            navigate('/home');
        } else {
            // Handle authentication error
            console.error(response.body);
        }
        
    };

    const redirectToCadastro = () => {
        // Redirecionamento para a tela de cadastro
        navigate('/cadastro');
    };

    return (
        <div className="container">
            <h2 className="titulo">Tela de Login</h2>
            <form>
                <label>
                    Email:
                    <input type="email" value={username} onChange={(e) => setEmail(e.target.value)} />
                </label>
                <label> 
                    Senha:
                    <input type="password" value={password} onChange={(e) => setSenha(e.target.value)} />
                </label>
                <button type="button" onClick={handleLogin(username, password)}>
                    Login
                </button>
            </form>
            <div className="cadastro-link">
                Não possui uma conta?{' '}
                <button onClick={redirectToCadastro}>
                    Cadastre-se
                </button>
            </div>
        </div>
    );
};

export default Login;
