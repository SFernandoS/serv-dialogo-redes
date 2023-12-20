// Cadastro.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Cadastro.css';

const Cadastro = () => {
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const navigate = useNavigate();

    const handleCadastro = async () => {
        try {
            const response = await fetch('http://localhost:8000/users/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    dialog_capability: "both",
                    status: "online",
                    password: senha
                }),
            });

            if (response.ok) {
                console.log('Registration successful');
                navigate('/login');
            } else {
                const data = await response.json();
                console.error('Registration failed:', data.error);
            }
        } catch (error) {
            console.error('Error during registration:', error);
        }
    };

    const redirectToLogin = () => {
        navigate('/login');
    };

    return (
        <div className="container">
            <h2>Tela de Cadastro</h2>
            <form>
                <label>
                    Email:
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </label>
                <label>
                    Senha:
                    <input type="password" value={senha} onChange={(e) => setSenha(e.target.value)} />
                </label>
                <button type="button" onClick={handleCadastro}>
                    Cadastrar
                </button>
            </form>
            <div className="login-link">
                Já possui uma conta?{' '}
                <button onClick={redirectToLogin}>
                    Login
                </button>
            </div>
        </div>
    );
};

export default Cadastro;
