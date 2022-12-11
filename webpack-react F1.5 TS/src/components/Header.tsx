import * as React from "react";

import "../styles/Header.css";

function Header(props) {
    console.log(props);
    let [count, setNewCount] = React.useState(0);

    const handleClick = () => {
        setNewCount(count + 1);
    };

    return (
        <header>This is header
            <button className={ "some-button" } onClick={ handleClick }>
                {props.buttonName}, clicked: {count} times
            </button >
        </header>
    )
}

export default Header;