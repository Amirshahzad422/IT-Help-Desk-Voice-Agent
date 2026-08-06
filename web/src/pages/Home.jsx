import Navbar from "../components/layout/Navbar";
import Hero from "../components/home/Hero";

function Home({ onStart }) {
  return (
    <>
      <Navbar onStart={onStart} />
      <Hero onStart={onStart} />
    </>
  );
}

export default Home;