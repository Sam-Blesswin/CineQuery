import axios from "axios";
import { useState } from "react";

type InputBoxProps = {
  onSend: (message: string) => void;
};

const InputBox = (props: InputBoxProps) => {
  const [message, setMessage] = useState("");

  const sendHandler = async () => {
    props.onSend("");

    const response = await axios.post("http://127.0.0.1:3000/api/v1/chat/", {
      message,
    });

    console.log(response.data);

    props.onSend(response.data["outputMessage"]);
  };

  return (
    <div className="flex justify-center p-4">
      <div className="w-1/2 flex">
        <input
          className="w-full p-2 border-2 border-white rounded-l-lg text-white bg-black placeholder-gray-400"
          placeholder="Ask me about any movie"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        ></input>
        <button
          className="p-2 rounded-r-lg text-black bg-yellow-500"
          onClick={sendHandler}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default InputBox;
