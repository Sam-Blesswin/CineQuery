import { useState } from "react";
import InputBox from "./InputBox";
import OutputBox from "./OutputBox";
import InfoBox from "./InfoBox";

const ChatBox = () => {
  const [outputMessage, setOutputMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = (data: string) => {
    setOutputMessage(data);
    setErrorMessage("");
  };

  const handleSendError = (error: string) => {
    setErrorMessage(error);
    setOutputMessage("");
  };

  const handleLoading = (isLoading: boolean) => {
    setIsLoading(isLoading);
  };

  return (
    <div>
      <InfoBox></InfoBox>
      <InputBox
        onSend={handleSend}
        onSendError={handleSendError}
        onSendRequest={handleLoading}
      ></InputBox>
      <OutputBox
        outputMessage={outputMessage}
        errorMessage={errorMessage}
        isLoading={isLoading}
      ></OutputBox>
    </div>
  );
};

export default ChatBox;
