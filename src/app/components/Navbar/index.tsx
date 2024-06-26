import Link from "next/link";
import React from "react";

const Navbar = () => {
  return (
      <nav className="p-4 flex justify-between">
        <div className="logo">
            <p className="font-bold lg:text-xl sm: text-lg">SimpleDownloader</p>
        </div>
        <div className="menu">
            <ul className="list-none flex gap-x-5 font-medium lg:text-lg sm: text-sm pt-1">
                <li><Link href={"/youtube"}>Youtube</Link></li>
                <li><Link href={"/"}>Instagram</Link></li>
            </ul>
        </div>
      </nav>
  );
};

export default Navbar;
