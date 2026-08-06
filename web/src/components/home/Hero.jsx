import { ArrowRight } from "lucide-react";

function Hero({ onStart }) {
  return (
    <section className="min-h-[85vh] flex items-center justify-center px-6">
      <div className="max-w-5xl text-center">

        <h1 className="text-6xl font-extrabold text-gray-900 leading-tight">
          AI Powered
          <br />
          IT Help Desk
        </h1>

        <p className="mt-6 text-lg text-gray-600 max-w-2xl mx-auto">
          Get instant technical support through a real-time voice assistant
          powered by AI and LiveKit.
        </p>

        <button
          onClick={onStart}
          className="mt-10 bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-2xl flex items-center gap-3 mx-auto text-lg transition"
        >
          Start Support
          <ArrowRight size={20}/>
        </button>

      </div>
    </section>
  );
}

export default Hero;