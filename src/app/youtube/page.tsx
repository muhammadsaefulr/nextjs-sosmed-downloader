"use client";

import React, { useEffect, useState } from "react";
import { ToastAlert } from "../components/ToastAlert";

interface ResponseRes {
  dataDetail: [
    {
      urlLinks: string;
      videoRes: string;
      videoResId: string;
    },
    {
      videoChannel: string;
      videoChannelId: string;
      videoDesc: string;
      videoTitle: string;
    }
  ];
}

const initialDataDetail: ResponseRes = {
  dataDetail: [
    {
      urlLinks: "",
      videoRes: "",
      videoResId: "",
    },
    {
      videoChannel: "",
      videoChannelId: "",
      videoDesc: "",
      videoTitle: "",
    },
  ],
};

const Youtube = () => {
  const [dataLinks, setDataLinks] = useState({ links: "", res: "" || "360p" });
  const [responseRes, setResponseRes] = useState<ResponseRes>();
  const [isLoading, setIsloading] = useState(false);

  const handleSubmit = (e: React.FormEvent<EventTarget>) => {
    e.preventDefault();
    if (dataLinks.links !== "") {
      setIsloading(true);
      console.log(dataLinks);
      fetch(`/api/v1/youtube?url=${dataLinks.links}&res=${dataLinks.res}`).then(
        async (res) => {
          setIsloading(false);
          if (res.status === 200) {
            setResponseRes(await res.json());
            console.log(responseRes);
          } else {
            return <ToastAlert message={`${res.status} An Error Accoured !`} />;
          }
        }
      );
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[100dvh] bg-background px-4 md:px-6">
      <div className="space-y-6 text-center">
        <h1 className="text-3xl font-bold text-center tracking-tighter md:text-5xl">
          Youtube Downloader
        </h1>

        <p className="pt-4 text-center lg:text-lg sm: text-sm">
          Download your favorite YouTube videos with ease. Simply paste the
          video URL and click the download button.
        </p>
      </div>
      <div className="flex gap-x-2 justify-center pt-4 mx-auto">
        <form onSubmit={handleSubmit}>
          <input
            onChange={(e) =>
              setDataLinks({ ...dataLinks, links: e.target.value })
            }
            className="p-2 rounded-md text-black outline-none"
            placeholder="Paste Text Link In here"
          ></input>
          <button type="submit" className="p-2 mx-4 bg-blue-500 rounded-md">
            {isLoading ? "Loading.." : "Submit"}
          </button>
        </form>
      </div>

      <div
        className={`${
          responseRes ? "visible" : "hidden"
        } w-full flex justify-center pt-8`}
      >
        <div className="">
          <iframe src={responseRes?.dataDetail[0]?.urlLinks} />
          <a href={responseRes?.dataDetail[0].urlLinks}>
            <button className="p-2 mt-4 bg-blue-500 rounded-md">
              Download
            </button>
          </a>
        </div>
      </div>

      <div className="mt-12 max-w-2xl space-y-8">
        <h2 className="text-2xl font-bold">How to Use</h2>
        <ol className="space-y-2 text-muted-foreground">
          <li className="flex items-start gap-2">
            <div className="mt-1 rounded-full text-black bg-white px-2 py-1 text-xs font-medium ">1</div>
            <div>Copy the URL of the YouTube video you want to download.</div>
          </li>
          <li className="flex items-start gap-2">
            <div className="mt-1 rounded-full text-black bg-white px-2 py-1 text-xs font-medium ">2</div>
            <div>Paste the URL into the input field on this page and click the "Download" button.</div>
          </li>
          <li className="flex items-start gap-2">
            <div className="mt-1 rounded-full text-black bg-white px-2 py-1 text-xs font-medium ">3</div>
            <div>Your video will start downloading automatically. Enjoy your video!</div>
          </li>
        </ol>
      </div>
      
    </div>
  );
};

export default Youtube;
