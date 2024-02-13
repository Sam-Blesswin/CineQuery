import axios from "axios";
import { useState } from "react";

type InputBoxProps = {
  onSend: (message: string) => void;
  onSendError: (message: string) => void;
  onSendRequest: (status: boolean) => void;
};

interface ErrorResponse {
  response: {
    data: {
      error: string;
    };
  };
}

const InputBox = (props: InputBoxProps) => {
  const [message, setMessage] = useState("");

  const sendHandler = async () => {
    if (message.trim() === "") {
      return;
    }

    try {
      props.onSendRequest(true);

      const response = await axios.post("http://127.0.0.1:3000/api/v1/chat/", {
        message,
      });

      if (response.status === 200) {
        console.log(response.data);
        props.onSend(response.data["outputMessage"]);
      }
    } catch (err: unknown) {
      console.error("Error occurred during the API call:", err);

      if (err instanceof Error && "response" in err) {
        const errorResponse = err as ErrorResponse;
        const serverMessage =
          errorResponse.response.data["error"] ||
          "Something went wrong on the server.";
        props.onSendError(`${serverMessage}`);
      } else {
        props.onSendError("Cannot reach server! Please try again later");
      }
    } finally {
      props.onSendRequest(false);
    }
  };

  return (
    <div className="flex justify-center p-4">
      <div className="w-1/2 flex">
        <input
          className="w-full p-2 border-2 border-yellow-500 rounded-l-lg text-white bg-black placeholder-gray-400"
          placeholder="Ask me about any movie or series"
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
