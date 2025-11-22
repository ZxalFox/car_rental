import { Link, navigate } from "gatsby";
import React, { useCallback } from "react";
import { useAuth } from "../context/AuthContext";
import "../styles/global.css";

const Layout = ({ children }) => {
  const { user, logout, loading } = useAuth();

  const handleLogout = useCallback(async () => {
    try {
      await logout();
      navigate("/login");
    } catch (err) {
      console.error("Erro ao sair", err);
    }
  }, [logout]);

  return (
    <div className="app">
      <header className="app__header">
        <div className="app__header-left">
          <Link to="/" className="app__brand">
            Car Rental
          </Link>
          {!loading && user && (
            <span className="app__greeting">
              Olá, {user.full_name || user.username}!
            </span>
          )}
        </div>
        <nav className="app__nav">
          <ul>
            {!loading && user ? (
              <>
                <li>
                  <Link to="/rentals/nova/" className="app__link">
                    Nova reserva
                  </Link>
                </li>
                <li>
                  <button
                    type="button"
                    className="app__link app__link--button"
                    onClick={handleLogout}
                  >
                    Sair
                  </button>
                </li>
              </>
            ) : (
              <li>
                <Link to="/login/" className="app__link">
                  Entrar
                </Link>
              </li>
            )}
          </ul>
        </nav>
      </header>
      <main className="app__content">{children}</main>
      <footer className="app__footer">
        &copy; {new Date().getFullYear()} Car Rental
      </footer>
    </div>
  );
};

export default Layout;
