// Login.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = () => {
    const navigate = useNavigate();

    const handleLogin = () => {
        // Lógica de login aqui
        console.log('Realizando login...');
    };

    const redirectToCadastro = () => {
        // Redirecionamento para a tela de cadastro
        navigate('/cadastro');
    };

    return (
        <div className="container">
            <h2 className="titulo">Tela de Login</h2>
            <form>
                <label htmlFor="email">E-mail:</label>
                <input type="email" id="email" name="email" />

                <label htmlFor="password">Senha:</label>
                <input type="password" id="password" name="password" />

                <button type="button" onClick={handleLogin}>
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
