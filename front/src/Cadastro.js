// Cadastro.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Importa o hook useNavigate
import './Cadastro.css';

const Cadastro = () => {
    const [nome, setNome] = useState('');
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const navigate = useNavigate(); // Obtém a função de navegação

    const handleCadastro = () => {
        // Aqui você pode adicionar lógica para lidar com os dados do formulário
        console.log('Nome:', nome);
        console.log('Email:', email);
        console.log('Senha:', senha);
    };

    const redirectToLogin = () => {
        // Redireciona para a tela de login
        navigate('/login');
    };

    return (
        <div className="container">
            <h2>Tela de Cadastro</h2>
            <form>
                <label>
                    Nome:
                    <input type="text" value={nome} onChange={(e) => setNome(e.target.value)} />
                </label>
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
