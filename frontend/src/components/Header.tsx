type HeaderSpecs = {
    displayName: string;
    email: string;
    onLogout: () => void;
};

function Header({displayName, email, onLogout}: HeaderSpecs) {
    return (

        <header>
            <span>{displayName} ({email})</span>
            <button type="button" 
                    onClick={onLogout}>
                    Kirjaudu ulos
            </button>
        </header>

    );
}

export default Header;
