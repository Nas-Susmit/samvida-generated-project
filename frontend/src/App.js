import React from "react";
import logo from "./samvida-logo.png";

function App() {
    return (
        <div style={{
            height: "100vh",
            width: "100vw",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "#f0f0f0"      // optional background color
        }}>
            <img src={logo} alt="SAMVIDA Logo" style={{
                maxWidth: "90%",
                maxHeight: "90%",
                objectFit: "contain"
            }} />
        </div>
    );
}

export default App;