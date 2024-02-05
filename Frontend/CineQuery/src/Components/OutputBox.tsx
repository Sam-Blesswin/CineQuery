type OutputBoxProps = {
  outputMessage: string;
};

const OutputBox = (props: OutputBoxProps) => {
  return (
    <div className="flex justify-center p-4">
      <div className="w-1/2 border-2 p-4 border-white rounded-lg">
        <h1 className="text-white whitespace-pre-wrap">
          {props.outputMessage}
        </h1>
      </div>
    </div>
  );
};

export default OutputBox;
