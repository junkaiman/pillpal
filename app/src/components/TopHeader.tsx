import React from "react";

const Header: React.FC = () => {
  return (
    <div className="bg-[#7252FE] w-full p-10 text-white rounded-bl-3xl rounded-br-3xl h-[25vh]">
      <div className="text-md mb-3">{"Welcome Back!"}</div>
      <div className="text-3xl">{"Let's find your medication."}</div>
    </div>
  );
};

export default Header;
