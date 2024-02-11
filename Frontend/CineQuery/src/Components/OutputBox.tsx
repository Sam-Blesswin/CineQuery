type OutputBoxProps = {
  outputMessage: string;
  errorMessage: string;
  isLoading: boolean;
};

const OutputBox = (props: OutputBoxProps) => {
  let messageDiv;

  if (props.isLoading) {
    messageDiv = (
      <div className="text-center">
        <div className="flex justify-center items-center h-24">
          <div className="w-5 h-5 bg-yellow-400 rounded-full mx-1 animate-pulse"></div>
          <div
            className="w-5 h-5 bg-yellow-400 rounded-full mx-1 animate-pulse"
            style={{ animationDelay: "0.2s" }}
          ></div>
          <div
            className="w-5 h-5 bg-yellow-400 rounded-full mx-1 animate-pulse"
            style={{ animationDelay: "0.4s" }}
          ></div>
        </div>
      </div>
    );
  } else if (props.errorMessage != "") {
    messageDiv = (
      <h1 className="text-red-500 whitespace-pre-wrap text-center">
        {props.errorMessage}
      </h1>
    );
  } else {
    messageDiv = (
      <h1 className="text-white whitespace-pre-wrap">{props.outputMessage}</h1>
    );
  }
  return (
    <div className="flex justify-center p-4">
      <div className="w-1/2 p-4">{messageDiv}</div>
    </div>
  );
};

export default OutputBox;
