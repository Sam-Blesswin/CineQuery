import { useState } from "react";
import InputBox from "./InputBox";
import OutputBox from "./OutputBox";

const ChatBox = () => {
  const [outputMessage, setOutputMessage] = useState("");

  const handleSend = (data: string) => {
    setOutputMessage(data); // Update the state with the response data
  };

  return (
    <div>
      <InputBox onSend={handleSend}></InputBox>
      <OutputBox outputMessage={outputMessage}></OutputBox>
    </div>
  );
};

export default ChatBox;
