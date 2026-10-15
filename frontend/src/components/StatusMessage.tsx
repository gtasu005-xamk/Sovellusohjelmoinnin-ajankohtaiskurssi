import {Link} from "react-router-dom";

type EmptyStateProps = {
    title: string;
    text?: string;
    linkTo?: string;
    linkText?: string;
};

export function EmptyState({title, text, linkTo, linkText}: EmptyStateProps) {
    return (
        <div className="empty-state">
            <strong>{title}</strong>
            {text && <p>{text}</p>}
            {linkTo && linkText && <Link to={linkTo}>{linkText}</Link>}
        </div>
    );
}

export function ErrorBanner({message}: {message: string}) {
    return (
        <div className="error-banner" role="alert">
            {message}
        </div>
    );
}
