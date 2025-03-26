/** Import necessary modules. */
import React from "react";

/** Header component. */
const Header = ({ toggled, setToggled }) => {
  return (
    <div className="chat-header">
      <h1>Gemma 🤖</h1>
      <span className="toggle-text">Stream</span>
      <button
        className={`toggle-btn ${toggled ? "toggled" : ""}`}
        onClick={() => setToggled(!toggled)}
      >
        <div className="toggle-hover">
          <div className="thumb"></div>
          {toggled === false ? (
            <span className="toggle-hover-text">Streaming response Off</span>
          ) : (
            <span className="toggle-hover-text">Streaming response On</span>
          )}
        </div>
      </button>
    </div>
  );
};

export default Header;
