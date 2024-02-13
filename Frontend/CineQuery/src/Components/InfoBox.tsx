const InfoBox = () => {
  return (
    <div className="text-center p-4 bg-black rounded-lg shadow-lg">
      <h1 className="text-lg lg:text-2xl font-bold text-yellow-400">
        🎬 For Stellar Movie Insights: Please Specify Your Prompt 🌟
      </h1>
      <p className="text-md text-white mt-2">
        Are you inquiring about a{" "}
        <span className="font-semibold text-yellow-500">Movie</span>,{" "}
        <span className="font-semibold text-yellow-500">TV Show</span>, or a{" "}
        <span className="font-semibold text-yellow-500">Celebrity</span>? Let us
        know for a tailored response!
      </p>
      <div className="text-sm text-gray-300 mt-4">
        <p>For example, you can ask:</p>
        <ul className="list-disc list-inside">
          <li>
            "What are some interesting facts about 'Stranger Things' TV show?"
          </li>
          <li>"Provide insights on Leonardo DiCaprio's acting career."</li>
          <li>
            "Can you recommend around 5 top-rated comedy movies from the 2020?"
          </li>
          <li>
            "What are the most awarded films directed by Christopher Nolan?"
          </li>
        </ul>
      </div>
    </div>
  );
};

export default InfoBox;
