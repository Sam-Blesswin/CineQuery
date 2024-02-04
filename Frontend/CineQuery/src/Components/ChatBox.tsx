import axios from "axios";
import { useState } from "react";

const ChatBox = () => {
  const [message, setMessage] = useState("");

  const sendHandler = async () => {
    const response = await axios.post("http://127.0.0.1:3000/api/v1/chat/", {
      message,
    });
    console.log(response);
  };

  return (
    <div className="flex justify-center p-4">
      <input
        className="w-1/2 p-2 border-2 border-white rounded-lg text-white bg-black placeholder-gray-400"
        placeholder="Ask me about any movie"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      ></input>
      <button
        className="p-2 ml-2 bg-white rounded-lg text-black"
        onClick={sendHandler}
      >
        Send
      </button>
    </div>
  );
};

export default ChatBox;
