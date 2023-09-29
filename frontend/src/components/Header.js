import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
// import { AuthContext } from './context/AuthContext';

const Header = () => {
//   const { isAuthenticated, username } = useContext(AuthContext);

  return (
    <header className="header">
      <div className="logo">
        <Link to="/">
          <img className='logo-pic' src={require('../assets/taipex_logo.png')} alt="Taipex Logo" />
        </Link>
      </div>
      {/* <nav className="nav">
        <ul>
        {isAuthenticated ? (
          <>
            <li>
              <span>{username}</span>
            </li>
            <li>
              <Link to="/logout">Logout</Link>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/register">Register</Link>
            </li>
          </>
        )}
        </ul>
      </nav> */}
    </header>
  );
};

export default Header;