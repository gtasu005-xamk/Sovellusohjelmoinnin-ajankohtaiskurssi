import {Link} from "react-router-dom";

type HeaderSpecs = {
    displayName: string;
    email: string;
    onLogout: () => void;
};

function Header({displayName, email, onLogout}: HeaderSpecs) {
    return (

        <header>
            <Link to="/">Etusivu</Link>
            <Link to="/sessions">Sessiot</Link>
            <span>{displayName} ({email})</span>
            <button type="button" 
                    onClick={onLogout}>
                    Kirjaudu ulos
            </button>
        </header>

    );
}

export default Header;
