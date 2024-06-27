"use client";
import { useState } from "react";
import { ToastAlert } from "./components/ToastAlert";

interface ResponseRes {
  dataDetail: [
    {
      postUrl: string[];
    }
  ];
}

export default function Component() {
  const [dataLinks, setDataLinks] = useState({ links: "", res: "" || "360p" });
  const [isLoading, setIsloading] = useState(false);

  const handleSubmit = (e: React.FormEvent<EventTarget>) => {
    e.preventDefault();
    if (dataLinks.links !== "") {
      setIsloading(true);
      console.log(dataLinks);
      fetch(`/api/instagram?url=${dataLinks.links}`).then(async (res) => {
        setIsloading(false);
        if (res.status === 200) {
          const dataResp: ResponseRes = await res.json();

          const link = document.createElement("a");
          link.href = dataResp?.dataDetail[0].postUrl[0];
          document.body.appendChild(link);
          
          link.click();
          document.body.removeChild(link);
        } else {
          return <ToastAlert message={`${res.status} An Error Accoured !`} />;
        }
      });
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[100dvh] bg-background px-4 md:px-6">
      <div className="max-w-2xl space-y-6 text-center">
        <h1 className="text-3xl font-bold tracking-tighter md:text-5xl">
          Instagram Downloader
        </h1>
        <p className="text-muted-foreground md:text-xl">
          Download your favorite Instagram Reel with ease. Simply paste the
          video URL and click the download button.
        </p>
        <form onSubmit={handleSubmit}>
          <input
            onChange={(e) =>
              setDataLinks({ ...dataLinks, links: e.target.value })
            }
            className="p-2 rounded-md text-black outline-none"
            placeholder="Paste Text Link In here"
          ></input>
          <button
            type="submit"
            className="p-2 mt-4 mx-4 bg-blue-500 rounded-md"
          >
            {isLoading ? "Loading.." : "Submit"}
          </button>
        </form>
      </div>

      <div className="mt-12 max-w-2xl space-y-4">
        <h2 className="text-2xl font-bold">How to Use</h2>
        <ol className="space-y-2 text-muted-foreground">
          <li className="flex items-start gap-2">
            <div className="mt-1 rounded-full text-black bg-white px-2 py-1 text-xs font-medium ">
              1
            </div>
            <div>Copy the URL of the YouTube video you want to download.</div>
          </li>
          <li className="flex items-start gap-2">
            <div className="mt-1 rounded-full text-black bg-white px-2 py-1 text-xs font-medium ">
              2
            </div>
            <div>
              Paste the URL into the input field on this page and click the
              "Download" button.
            </div>
          </li>
          <li className="flex items-start gap-2">
            <div className="mt-1 rounded-full text-black bg-white px-2 py-1 text-xs font-medium ">
              3
            </div>
            <div>
              Your video will start downloading automatically. Enjoy your video!
            </div>
          </li>
        </ol>
      </div>
    </div>
  );
}
