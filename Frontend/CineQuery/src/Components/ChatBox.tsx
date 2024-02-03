const ChatBox = () => {
  return (
    <div className="flex justify-center p-4">
      <input
        className="w-1/2 p-2 border-2 border-white rounded-lg text-white bg-black placeholder-gray-400"
        placeholder="Ask me about any movie"
      ></input>
    </div>
  );
};

export default ChatBox;
