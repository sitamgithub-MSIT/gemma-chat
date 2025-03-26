/** Import necessary modules. */
import React from "react";
import Markdown from "react-markdown";
import userIcon from "../assets/user-icon.png";
import chatbotIcon from "../assets/chatbot-icon.png";

/** ChatArea component. */
const ChatArea = ({ data, streamdiv, answer }) => {
  return (
    <div className="chat-area">
      {data?.length <= 0 ? (
        <div className="welcome-area">
          <p className="welcome-1">Hi👋🏻,</p>
          <p className="welcome-2">How can I help you today?</p>
        </div>
      ) : (
        <div className="welcome-area" style={{ display: "none" }}></div>
      )}

      {data.map((element, index) => (
        <div key={index} className={element.role}>
          <img
            src={element.role === "user" ? userIcon : chatbotIcon}
            alt="Icon"
          />
          <p>
            <Markdown children={element.parts[0].text} />
          </p>
        </div>
      ))}

      {streamdiv && (
        <div className="tempResponse">
          <img src={chatbotIcon} alt="Icon" />
          {answer && (
            <p>
              <Markdown children={answer} />
            </p>
          )}
        </div>
      )}

      <span id="checkpoint"></span>
    </div>
  );
};

export default ChatArea;
